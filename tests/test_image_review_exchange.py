"""Exercise state preservation and corrupt/untrusted cloud deliveries."""
from __future__ import annotations
import json
from pathlib import Path
import sqlite3
import struct
import sys
import tempfile
import time
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import image_review_exchange as exchange
from image_review_register import SCHEMA


class Store:
    def __init__(self): self.data = {}
    def get(self, key): return self.data[key]
    def maybe_get(self, key): return self.data.get(key)
    def put(self, key, data, immutable=True):
        if immutable and key in self.data and self.data[key] != data:
            raise exchange.InvalidBundle('Immutable object changed')
        self.data[key] = data
    def keys(self, prefix): return [key for key in self.data if key.startswith(prefix)]


def png():
    def chunk(kind, data):
        return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data))
    raw = (b'\0' + b'\xff\xff\xff' * 800) * 450
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!IIBBBBB', 800, 450, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')


class ExchangeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.live = self.root / 'live.sqlite'
        self.assets = self.root / 'live-assets'
        self.worker = self.root / 'worker'
        self.store = Store()
        with sqlite3.connect(self.live) as conn:
            conn.executescript(SCHEMA)
            conn.execute("INSERT INTO candidates(id,target_path,status,reviewed_at,candidate_url,current_slide_url,proposed_slide_url) VALUES ('old','content/part-01/old/images/old.png','rejected','2026-08-31 01:00:00','','','')")
            conn.execute("INSERT INTO review_events(candidate_id,actor,action,comment) VALUES ('old','reviewer','reject','original')")
        self.export = self.root / 'export'
        exchange.authority_export(self.live, self.assets, self.export)
        self.meta = exchange.publish_snapshot(self.store, self.export)
        exchange.fetch_snapshot(self.store, self.worker)

    def tearDown(self): self.temp.cleanup()

    def candidate(self, cid='new', target=None):
        row = {'id': cid, 'batch_id': '2026-10-27', 'topic_path': 'content/part-01/topic',
               'target_path': target or f'content/part-01/topic/images/{cid}.png',
               'slide_ref': 'slide 2', 'brief': 'An editable candidate',
               'prompt': 'Composition decision\nNative HTML.\nContent preservation\nAll claims retained.\nLayout QA\nRendered and passed all geometry checks.'}
        with sqlite3.connect(self.worker / 'image-review.sqlite') as conn:
            conn.execute('INSERT INTO candidates (' + ','.join(exchange.FIELDS) + ",candidate_url,current_slide_url,proposed_slide_url) VALUES (" + ','.join('?' for _ in range(len(exchange.FIELDS)+3)) + ')', [row[k] for k in exchange.FIELDS]+['','',''])
        directory = self.worker / 'candidates' / cid
        directory.mkdir(parents=True)
        for name in exchange.REQUIRED[:3]: (directory / name).write_bytes(png())
        (directory / 'prompt.txt').write_text(row['prompt'])
        (directory / 'candidate-source.html').write_text('<section>Editable</section>')
        return row

    def submission(self, cid='new', run_id='run-1'):
        return exchange.create_submission(self.worker, [cid], run_id, 'html', True)

    def live_row(self, cid):
        with sqlite3.connect(self.live) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute('SELECT * FROM candidates WHERE id=?', (cid,)).fetchone()
            return dict(row) if row else None

    def test_snapshot_roundtrip_and_history(self):
        self.assertEqual(exchange.check_db(self.worker / 'image-review.sqlite')['review_events'], 1)
        self.assertEqual(json.loads((self.worker / 'snapshot.json').read_bytes())['known_candidate_ids'], ['old'])

    def test_snapshot_reuses_immutable_objects(self):
        before = [key for key in self.store.data if key.startswith('snapshots/')]
        exchange.publish_snapshot(self.store, self.export)
        self.assertEqual(before, [key for key in self.store.data if key.startswith('snapshots/')])

    def test_stale_snapshot_fails_before_touching_local_state(self):
        metadata = json.loads(self.store.data['latest.json'])
        metadata['checked_at'] = int(time.time()) - 100000
        self.store.data['latest.json'] = exchange.json_bytes(metadata)
        before = (self.worker / 'image-review.sqlite').read_bytes()
        with self.assertRaises(exchange.InvalidBundle): exchange.fetch_snapshot(self.store, self.worker)
        self.assertEqual(before, (self.worker / 'image-review.sqlite').read_bytes())

    def test_corrupt_snapshot_rejected(self):
        self.store.data[f"snapshots/{self.meta['version']}/image-review.sqlite"] += b'bad'
        with self.assertRaises(exchange.InvalidBundle): exchange.fetch_snapshot(self.store, self.worker)

    def test_fetch_preserves_unsubmitted_candidate(self):
        self.candidate()
        with self.assertRaisesRegex(exchange.InvalidBundle, 'have not reached'):
            exchange.fetch_snapshot(self.store, self.worker)
        with sqlite3.connect(self.worker / 'image-review.sqlite') as conn:
            self.assertEqual(conn.execute("SELECT count(*) FROM candidates WHERE id='new'").fetchone()[0], 1)

    def test_live_review_after_snapshot_survives_import(self):
        self.candidate()
        with sqlite3.connect(self.live) as conn:
            conn.execute("UPDATE candidates SET status='approved',review_comment='new decision' WHERE id='old'")
            conn.execute("INSERT INTO review_events(candidate_id,actor,action,comment) VALUES ('old','reviewer','approve','new decision')")
        result = exchange.authority_import(self.live, self.assets, self.submission())
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(self.live_row('old')['review_comment'], 'new decision')
        self.assertEqual(self.live_row('old')['status'], 'approved')
        self.assertEqual(self.live_row('new')['status'], 'pending')
        self.assertEqual(exchange.check_db(self.live)['review_events'], 3)

    def test_repeated_delivery_preserves_later_approval(self):
        self.candidate()
        bundle = self.submission()
        exchange.authority_import(self.live, self.assets, bundle)
        with sqlite3.connect(self.live) as conn: conn.execute("UPDATE candidates SET status='approved' WHERE id='new'")
        result = exchange.authority_import(self.live, self.assets, bundle)
        self.assertTrue(result['already_imported'])
        self.assertEqual(self.live_row('new')['status'], 'approved')
        self.assertEqual(exchange.check_db(self.live)['review_events'], 2)

    def test_existing_id_under_new_run_rejected(self):
        self.candidate()
        exchange.authority_import(self.live, self.assets, self.submission())
        with self.assertRaisesRegex(exchange.InvalidBundle, 'already exists'):
            exchange.authority_import(self.live, self.assets, self.submission(run_id='run-2'))

    def test_run_id_cannot_be_reused_for_other_content(self):
        self.candidate()
        exchange.authority_import(self.live, self.assets, self.submission())
        self.candidate('another')
        with self.assertRaisesRegex(exchange.InvalidBundle, 'different content'):
            exchange.authority_import(self.live, self.assets, self.submission('another'))
        self.assertIsNone(self.live_row('another'))

    def test_target_already_pending_rejected(self):
        first = self.candidate()
        exchange.authority_import(self.live, self.assets, self.submission())
        self.candidate('another', target=first['target_path'])
        with self.assertRaisesRegex(exchange.InvalidBundle, 'active candidate'):
            exchange.authority_import(self.live, self.assets, self.submission('another', 'run-2'))

    def test_corrupt_bundle_cannot_change_database(self):
        self.candidate()
        members = exchange.read_zip(self.submission())
        members['candidates/new/candidate-source.html'] = b'changed'
        with self.assertRaisesRegex(exchange.InvalidBundle, 'checksum'):
            exchange.authority_import(self.live, self.assets, exchange.make_zip(members))
        self.assertIsNone(self.live_row('new'))
        self.assertFalse(self.assets.exists())

    def test_traversal_archive_rejected(self):
        import io, zipfile
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive: archive.writestr('../outside', 'bad')
        with self.assertRaises(exchange.InvalidBundle): exchange.read_zip(stream.getvalue())
        self.assertFalse((self.root / 'outside').exists())

    def test_bundle_requires_content_and_geometry_evidence(self):
        self.candidate()
        with self.assertRaises(exchange.InvalidBundle):
            exchange.create_submission(self.worker, ['new'], 'run', 'html', False)
        (self.worker / 'candidates/new/candidate-source.html').unlink()
        with self.assertRaisesRegex(exchange.InvalidBundle, 'editable source'): self.submission()

    def test_submit_is_immutable_and_ready_is_last(self):
        self.candidate()
        data = self.submission()
        exchange.submit(self.store, data, 'run-1')
        self.assertEqual(list(self.store.data)[-1], 'submissions/run-1/ready.json')
        exchange.submit(self.store, data, 'run-1')
        with self.assertRaises(exchange.InvalidBundle): exchange.submit(self.store, b'different', 'run-1')

    def test_cloud_bundle_does_not_include_database_or_old_reviews(self):
        self.candidate()
        members = exchange.read_zip(self.submission())
        self.assertNotIn('image-review.sqlite', members)
        manifest, _ = exchange.unpack_submission(self.submission())
        self.assertEqual([row['id'] for row in manifest['candidates']], ['new'])
        self.assertNotIn('status', manifest['candidates'][0])

    def test_unsafe_candidate_target_rejected(self):
        self.candidate(target='content/part-01/topic/images/../../other.png')
        with self.assertRaises(exchange.InvalidBundle): self.submission()

    def test_unknown_extra_file_rejected(self):
        self.candidate()
        members = exchange.read_zip(self.submission())
        members['outside.txt'] = b'bad'
        with self.assertRaisesRegex(exchange.InvalidBundle, 'Unexpected files'):
            exchange.authority_import(self.live, self.assets, exchange.make_zip(members))

    def test_processor_acknowledges_matching_decision_once(self):
        with sqlite3.connect(self.live) as conn:
            conn.execute("UPDATE candidates SET status='approved' WHERE id='old'")
        processed = self.root / 'processed.sqlite'
        __import__('shutil').copy2(self.live, processed)
        with sqlite3.connect(processed) as conn:
            conn.execute("UPDATE candidates SET status='processed',processed_at='2026-10-27 01:00:00' WHERE id='old'")
        self.assertEqual(exchange.authority_ack(self.live, processed)['acknowledged'], 1)
        self.assertEqual(self.live_row('old')['status'], 'processed')
        self.assertEqual(exchange.authority_ack(self.live, processed)['acknowledged'], 0)

    def test_processor_preserves_decision_changed_during_delivery(self):
        processed = self.root / 'processed.sqlite'
        __import__('shutil').copy2(self.live, processed)
        with sqlite3.connect(processed) as conn:
            conn.execute("UPDATE candidates SET status='processed',processed_at='2026-10-27 01:00:00' WHERE id='old'")
        with sqlite3.connect(self.live) as conn:
            conn.execute("UPDATE candidates SET status='rejected',review_comment='newer review' WHERE id='old'")
        result = exchange.authority_ack(self.live, processed)
        self.assertEqual(result['acknowledged'], 0)
        self.assertEqual(result['stale_decisions_preserved'], 1)
        self.assertEqual(self.live_row('old')['review_comment'], 'newer review')


if __name__ == '__main__': unittest.main()
