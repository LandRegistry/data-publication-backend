from boto3.session import Session

from service import app

AWS_ACCESS_KEY = app.config['AWS_ACCESS_KEY']
AWS_SECRET_KEY = app.config['AWS_SECRET_KEY']
AWS_REGION_NAME = app.config['AWS_REGION_NAME']
AWS_BUCKET_NAME = app.config['AWS_BUCKET_NAME']
AWS_LINK_DURATION = app.config['AWS_LINK_DURATION']

session = Session(aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_KEY,
                  region_name=AWS_REGION_NAME)

s3 = session.client('s3')


def get_file_list(prefix):
    return s3.list_objects(Bucket=AWS_BUCKET_NAME, Prefix=prefix)


def get_download_url(key):
    parameters = {'Bucket': AWS_BUCKET_NAME, 'Key': key}
    return s3.generate_presigned_url('get_object', Params=parameters, ExpiresIn=AWS_LINK_DURATION)
