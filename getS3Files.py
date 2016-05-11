import s3

bucket_name = 'your-bucket'
local_directory = '/Users/user/Desktop/directory/'

connection = s3.S3Connection(access_key_id='', secret_access_key='', region='us-west-2', endpoint='s3-us-west-2.amazonaws.com', default_bucket=bucket_name)
storage = s3.Storage(connection)

for bucket in storage.bucket_list():
  print bucket.name, bucket.creation_date

for key in storage.bucket_list_keys(bucket_name):
  remote_name = s3.S3Name(key.key, bucket=bucket_name)
  try: storage.read(remote_name, local_directory + key.key)
  except: print "error: " + key.key
