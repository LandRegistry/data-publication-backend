import os
from typing import Dict, Union

aws_access_key = os.environ['AWS_ACCESS_KEY']
aws_secret_key = os.environ['AWS_SECRET_KEY']
aws_region_name = os.environ['AWS_REGION_NAME']
aws_bucket_name = os.environ['AWS_BUCKET_NAME']
aws_link_duration = int(os.environ['AWS_LINK_DURATION'])

CONFIG_DICT = {
    'DEBUG': False,
    'LOGGING': True,
    'AWS_ACCESS_KEY': aws_access_key,
    'AWS_SECRET_KEY': aws_secret_key,
    'AWS_REGION_NAME': aws_region_name,
    'AWS_BUCKET_NAME': aws_bucket_name,
    'AWS_LINK_DURATION': aws_link_duration,
}  # type: Dict[str, Union[bool, str, int]]

settings = os.environ.get('SETTINGS')

if settings == 'dev':
    CONFIG_DICT['DEBUG'] = True
elif settings == 'test':
    CONFIG_DICT['LOGGING'] = False
    CONFIG_DICT['DEBUG'] = True
