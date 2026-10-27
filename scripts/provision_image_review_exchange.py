#!/usr/bin/env python3
"""Provision the small private review exchange; keep credentials out of stdout/Git."""
import argparse
import json
import os
from pathlib import Path
import shlex

import boto3
from botocore.exceptions import ClientError

BUCKET = 'professional-practice-image-review-141101760219'
REGION = 'ap-southeast-2'


def policy(role):
    root = f'arn:aws:s3:::{BUCKET}'
    reads = ['latest.json', 'snapshots/*', 'submissions/*', 'receipts/*', 'source-reworks/*', 'smoke/*']
    writes = ['submissions/*', 'source-reworks/*', 'smoke/*'] if role == 'cloud' else ['latest.json', 'snapshots/*', 'receipts/*', 'smoke/*']
    return {'Version': '2012-10-17', 'Statement': [
        {'Effect': 'Allow', 'Action': 's3:ListBucket', 'Resource': root,
         'Condition': {'StringLike': {'s3:prefix': ['exchange/submissions/*', 'exchange/receipts/*', 'exchange/smoke/*']}}},
        {'Effect': 'Allow', 'Action': 's3:GetObject', 'Resource': [root+'/exchange/'+p for p in reads]},
        {'Effect': 'Allow', 'Action': 's3:PutObject', 'Resource': [root+'/exchange/'+p for p in writes]},
        {'Effect': 'Allow', 'Action': 's3:DeleteObject', 'Resource': root+'/exchange/smoke/*'}]}


def provision(profile, directory):
    session = boto3.Session(profile_name=profile, region_name=REGION)
    identity = session.client('sts').get_caller_identity()
    if identity['Account'] != '141101760219':
        raise RuntimeError('Select the industrial-linguistics AWS account')
    s3, iam = session.client('s3'), session.client('iam')
    try: s3.head_bucket(Bucket=BUCKET)
    except ClientError as exc:
        if exc.response['Error']['Code'] not in ('404', 'NoSuchBucket'): raise
        s3.create_bucket(Bucket=BUCKET, CreateBucketConfiguration={'LocationConstraint': REGION})
    s3.put_public_access_block(Bucket=BUCKET, PublicAccessBlockConfiguration={
        'BlockPublicAcls': True, 'IgnorePublicAcls': True, 'BlockPublicPolicy': True, 'RestrictPublicBuckets': True})
    s3.put_bucket_versioning(Bucket=BUCKET, VersioningConfiguration={'Status': 'Enabled'})
    s3.put_bucket_encryption(Bucket=BUCKET, ServerSideEncryptionConfiguration={
        'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]})
    s3.put_bucket_policy(Bucket=BUCKET, Policy=json.dumps({'Version':'2012-10-17','Statement':[
        {'Sid':'RequireTLS','Effect':'Deny','Principal':'*','Action':'s3:*',
         'Resource':[f'arn:aws:s3:::{BUCKET}',f'arn:aws:s3:::{BUCKET}/*'],
         'Condition':{'Bool':{'aws:SecureTransport':'false'}}}]}))
    directory.mkdir(parents=True, exist_ok=True)
    directory.chmod(0o700)
    for role in ('cloud', 'bridge'):
        name = 'professional-practice-image-review-' + role
        try: iam.get_user(UserName=name)
        except iam.exceptions.NoSuchEntityException:
            iam.create_user(UserName=name, Tags=[{'Key':'project','Value':'professional-practice'},{'Key':'purpose','Value':'image-review-exchange'}])
        iam.put_user_policy(UserName=name, PolicyName='image-review-exchange', PolicyDocument=json.dumps(policy(role)))
        target = directory / f'image-review-{role}.env'
        keys = iam.list_access_keys(UserName=name)['AccessKeyMetadata']
        if target.exists():
            if target.stat().st_mode & 0o077: raise RuntimeError(f'Unsafe permissions: {target}')
            saved = dict(line.split('=',1) for line in target.read_text().splitlines() if '=' in line)
            if not any(k['AccessKeyId'] == shlex.split(saved['AWS_ACCESS_KEY_ID'])[0] and k['Status']=='Active' for k in keys):
                raise RuntimeError(f'Saved credential is not active: {target}')
        else:
            if keys: raise RuntimeError(f'{name} already has a key; refusing to create duplicate credentials')
            key = iam.create_access_key(UserName=name)['AccessKey']
            values = {'AWS_ACCESS_KEY_ID':key['AccessKeyId'], 'AWS_SECRET_ACCESS_KEY':key['SecretAccessKey'],
                      'AWS_DEFAULT_REGION':REGION, 'IMAGE_REVIEW_S3_URI':f's3://{BUCKET}/exchange'}
            fd = os.open(target, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
            with os.fdopen(fd,'w') as handle:
                handle.write(''.join(k+'='+shlex.quote(v)+'\n' for k,v in values.items()))
        print(f'{role}: scoped credentials saved to {target} (0600); values withheld')
    print(f'Private, versioned, encrypted exchange: s3://{BUCKET}/exchange')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--profile',default='industrial-linguistics')
    p.add_argument('--secret-dir',type=Path,default=Path('state/secrets'))
    a=p.parse_args();provision(a.profile,a.secret_dir)
