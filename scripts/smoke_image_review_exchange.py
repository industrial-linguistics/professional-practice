#!/usr/bin/env python3
"""Test real scoped S3 credentials and isolated remote import; never register a live candidate."""
import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import shlex
import sqlite3
import subprocess
import tempfile
from uuid import uuid4

import image_review_exchange as ex
from image_review_register import SCHEMA


@contextmanager
def credentials(path):
    values = dict(line.split('=',1) for line in path.read_text().splitlines() if '=' in line)
    values = {k:shlex.split(v)[0] for k,v in values.items()}
    old = {k:os.environ.get(k) for k in values}
    os.environ.update(values)
    try: yield values
    finally:
        for key,value in old.items():
            if value is None: os.environ.pop(key,None)
            else: os.environ[key]=value


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cloud-env',type=Path,default=Path('state/secrets/image-review-cloud.env'))
    p.add_argument('--bridge-env',type=Path,default=Path('state/secrets/image-review-bridge.env'))
    p.add_argument('--remote',default='professionalpractice@merah')
    a=p.parse_args()
    token='migration-'+uuid4().hex
    with credentials(a.cloud_env) as cfg:
        worker=ex.S3Store(cfg['IMAGE_REVIEW_S3_URI'])
        cloud=ex.S3Store(cfg['IMAGE_REVIEW_S3_URI']+'/smoke/'+token)
    with credentials(a.bridge_env) as cfg:
        server=ex.S3Store(cfg['IMAGE_REVIEW_S3_URI']+'/smoke/'+token)
    # Probe denial using identical bytes, so a policy mistake cannot corrupt state.
    original=worker.get('latest.json')
    try: worker.put('latest.json',original,immutable=False)
    except Exception as error:
        if getattr(error,'response',{}).get('Error',{}).get('Code') not in ('AccessDenied','403'): raise
    else: raise RuntimeError('Cloud credentials unexpectedly can replace authoritative snapshots')
    live_before=ex.remote_run(a.remote,['sha256',ex.DEFAULT_DB]).strip()
    with tempfile.TemporaryDirectory() as temporary:
        root=Path(temporary)
        live=root/'fixture.sqlite'
        with sqlite3.connect(live) as conn:
            conn.executescript(SCHEMA)
            conn.execute("INSERT INTO candidates(id,target_path,status,candidate_url,current_slide_url,proposed_slide_url,review_comment) VALUES ('original','content/part-01/smoke/images/original.png','approved','','','','keep this decision')")
        export=root/'export'
        ex.authority_export(live,root/'original-assets',export)
        ex.publish_snapshot(server,export)
        state=root/'worker'
        ex.fetch_snapshot(cloud,state)
        cid='isolated-cloud-smoke'
        prompt='Composition decision\nHTML fixture.\nContent preservation\nFixture only.\nLayout QA\nSynthetic transport test; never published as course content.'
        row={'id':cid,'batch_id':'migration-smoke','target_path':'content/part-01/smoke/images/test.png','topic_path':'content/part-01/smoke','slide_ref':'slide 1','brief':'Isolated migration test','prompt':prompt}
        with sqlite3.connect(state/'image-review.sqlite') as conn:
            conn.execute('INSERT INTO candidates ('+','.join(ex.FIELDS)+",candidate_url,current_slide_url,proposed_slide_url) VALUES ("+','.join('?' for _ in range(len(ex.FIELDS)+3))+')',[row[k] for k in ex.FIELDS]+['','',''])
        directory=state/'candidates'/cid
        directory.mkdir(parents=True)
        # Transport validation uses the existing test PNG fixture, with no image API calls.
        import sys
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
        from test_image_review_exchange import png
        for name in ex.REQUIRED[:3]: (directory/name).write_bytes(png())
        (directory/'prompt.txt').write_text(prompt)
        (directory/'candidate-source.html').write_text('<section>Isolated test only</section>')
        bundle=ex.create_submission(state,[cid],token,'html',True)
        ex.submit(cloud,bundle,token)
        delivered=server.get('submissions/'+token+'/bundle.zip')
        assert delivered==bundle
        remote_root='/home/professionalpractice/image-review-exchange/smoke/'+token
        ex.remote_run(a.remote,['mkdir','-p',remote_root])
        (root/'bundle.zip').write_bytes(delivered)
        for path in (live,root/'bundle.zip'):
            subprocess.run(['scp','-q',str(path),a.remote+':'+remote_root+'/'+path.name],check=True)
        args=['python3',ex.DEFAULT_REMOTE_SCRIPT,'authority-import','--db',remote_root+'/fixture.sqlite','--candidates-dir',remote_root+'/assets','--bundle',remote_root+'/bundle.zip']
        first=json.loads(ex.remote_run(a.remote,args))
        repeat=json.loads(ex.remote_run(a.remote,args))
        assert first['status']=='accepted' and repeat['already_imported'] is True
        server.put('receipts/'+token+'.json',ex.json_bytes(first))
        assert json.loads(cloud.get('receipts/'+token+'.json'))['status']=='accepted'
        output=ex.remote_run(a.remote,['sqlite3',remote_root+'/fixture.sqlite',"select status || ':' || review_comment from candidates where id='original'; select count(*) from review_events;"])
        assert output.splitlines()==['approved:keep this decision','1'],output
    live_after=ex.remote_run(a.remote,['sha256',ex.DEFAULT_DB]).strip()
    assert live_before==live_after,'Production database changed during isolated test'
    result={'run_id':token,'status':'passed','worker_snapshot_write':'denied','snapshot_fetch':'verified','bundle_s3_roundtrip':'verified','remote_import':'accepted','repeated_import':'idempotent','original_review':'preserved','production_database':'byte-unchanged','evidence_s3_prefix':server.prefix}
    evidence=Path('state/image-review-migration/smoke-result.json')
    ex.atomic_write(evidence,ex.json_bytes(result))
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__': main()
