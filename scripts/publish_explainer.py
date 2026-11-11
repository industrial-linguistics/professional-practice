#!/usr/bin/env python3
"""Record a rendered explainer and store its master in S3.

    python3 scripts/publish_explainer.py error-budget            # write release.json, show the plan
    python3 scripts/publish_explainer.py error-budget --upload   # also store the film in S3
    python3 scripts/publish_explainer.py error-budget --fetch    # get the recorded film back, verified

explainers/<name>/release.json is the tracking record, kept in git: the film's hash, size and
duration, a hash of the scene files it was rendered from, the narration take, and where the
master is stored. Stored files are named by content, so nothing in the bucket is ever replaced
and a record always points at exactly one film.

The bucket is COURSE_MEDIA_BUCKET, or industrial-linguistics-course-media-<account id>. With
--create-bucket a missing bucket is created private, versioned and encrypted, in
AWS_DEFAULT_REGION or ap-southeast-2. Requires boto3, ffprobe and ordinary AWS credentials.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
REGION=os.environ.get('AWS_DEFAULT_REGION','ap-southeast-2')
TYPES={'.mp4':'video/mp4','.vtt':'text/vtt','.mp3':'audio/mpeg','.json':'application/json'}
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()
def repo_name():
    url=subprocess.run(['git','-C',str(ROOT),'remote','get-url','origin'],capture_output=True,text=True).stdout.strip()
    return (url.rstrip('/').rsplit('/',1)[-1].removesuffix('.git') if url else '') or ROOT.name
def probe(path):
    out=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height:format=duration','-of','json',str(path)],capture_output=True,text=True,check=True).stdout
    data=json.loads(out);return round(float(data['format']['duration']),3),data['streams'][0]['width'],data['streams'][0]['height']
def inputs_hash(home):
    """One hash over the files a render reads, so the record names its exact source."""
    h=hashlib.sha256()
    for f in sorted(home.iterdir()):
        if f.is_file() and f.name not in ('release.json','README.md'):h.update(f.name.encode()+b'\0'+bytes.fromhex(sha(f)))
    return h.hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('name');p.add_argument('--upload',action='store_true');p.add_argument('--fetch',action='store_true')
    p.add_argument('--create-bucket',action='store_true');p.add_argument('--captions',help='caption file, relative to the repository')
    p.add_argument('--narration',help='JSON record of the narration take (with audio_sha256), relative to the repository')
    p.add_argument('--youtube',help='record a YouTube URL for this film');a=p.parse_args()
    home=ROOT/'explainers'/a.name;record_path=home/'release.json';old=json.loads(record_path.read_text()) if record_path.exists() else {}
    repo=repo_name();prefix=f'{repo}/{a.name}/'
    if a.fetch:
        if not old.get('storage',{}).get('bucket'):raise SystemExit('release.json records no stored film yet')
        import boto3
        target=ROOT/'output/explainers'/old['film']['file'];target.parent.mkdir(parents=True,exist_ok=True)
        boto3.client('s3',region_name=REGION).download_file(old['storage']['bucket'],prefix+old['film']['file'],str(target))
        if sha(target)!=old['film']['sha256']:raise SystemExit(f'{target} does not match the recorded hash')
        print(target);return
    film=ROOT/'output/explainers'/f'{a.name}.mp4'
    if not film.exists():raise SystemExit(f'Render first: {film} is missing')
    digest=sha(film);tag=digest[:12];duration,width,height=probe(film)
    captions=a.captions or old.get('captions') or (f'explainers/{a.name}/captions.vtt' if (home/'captions.vtt').exists() else None)
    narration_record=a.narration or old.get('narration_record') or (f'explainers/{a.name}/narration.json' if (home/'narration.json').exists() else None)
    take=json.loads((ROOT/narration_record).read_text()).get('audio_sha256') if narration_record else None
    same=old.get('film',{}).get('sha256')==digest
    record={'name':a.name,'repository':repo,
        'film':{'file':f'{a.name}-{tag}.mp4','sha256':digest,'bytes':film.stat().st_size,'duration_seconds':duration,'width':width,'height':height},
        'inputs_sha256':inputs_hash(home),'narration_record':narration_record,'narration_sha256':take,'captions':captions,
        'storage':old.get('storage',{'bucket':None,'prefix':prefix,'uploaded':None}) if same else {'bucket':None,'prefix':prefix,'uploaded':None},
        'youtube':a.youtube or (old.get('youtube') if same else None)}
    uploads=[(film,prefix+record['film']['file'])]
    if captions:uploads.append((ROOT/captions,prefix+f'{a.name}-{tag}.vtt'))
    takes=ROOT/'output/explainers'/f'{a.name}-takes'
    if takes.is_dir() and take:uploads+=[(f,f'{prefix}takes/{take[:12]}/{f.name}') for f in sorted(takes.iterdir()) if f.suffix in ('.mp3','.json')]
    if a.upload:
        import boto3
        from botocore.exceptions import ClientError
        account=boto3.client('sts',region_name=REGION).get_caller_identity()['Account']
        bucket=os.environ.get('COURSE_MEDIA_BUCKET') or f'industrial-linguistics-course-media-{account}';s3=boto3.client('s3',region_name=REGION)
        try:s3.head_bucket(Bucket=bucket)
        except ClientError as error:
            if error.response['Error']['Code'] not in ('404','NoSuchBucket') or not a.create_bucket:
                raise SystemExit(f'Bucket {bucket} is not available ({error.response["Error"]["Code"]}). Pass --create-bucket to create it.')
            s3.create_bucket(Bucket=bucket,CreateBucketConfiguration={'LocationConstraint':REGION})
            s3.put_public_access_block(Bucket=bucket,PublicAccessBlockConfiguration={'BlockPublicAcls':True,'IgnorePublicAcls':True,'BlockPublicPolicy':True,'RestrictPublicBuckets':True})
            s3.put_bucket_versioning(Bucket=bucket,VersioningConfiguration={'Status':'Enabled'})
            s3.put_bucket_encryption(Bucket=bucket,ServerSideEncryptionConfiguration={'Rules':[{'ApplyServerSideEncryptionByDefault':{'SSEAlgorithm':'AES256'}}]})
            print(f'Created private, versioned, encrypted bucket {bucket} in {REGION}')
        for path,key in uploads:
            try:
                if s3.head_object(Bucket=bucket,Key=key)['ContentLength']==path.stat().st_size:print('already stored',key);continue
            except ClientError:pass
            s3.upload_file(str(path),bucket,key,ExtraArgs={'ContentType':TYPES.get(path.suffix,'application/octet-stream')});print('stored',key)
        record['storage']={'bucket':bucket,'prefix':prefix,'uploaded':datetime.date.today().isoformat()}
        s3.put_object(Bucket=bucket,Key=prefix+f'{a.name}-{tag}.json',Body=json.dumps(record,indent=1).encode(),ContentType='application/json')
    record_path.write_text(json.dumps(record,indent=1)+'\n')
    print(f'{record_path.relative_to(ROOT)}: {record["film"]["file"]}, {record["film"]["bytes"]/1e6:.1f} MB, {duration:.1f} s')
    if not a.upload:
        print('Not uploaded. With --upload these would be stored under s3://<bucket>/'+prefix)
        for path,key in uploads:print('  ',key)
if __name__=='__main__':main()
