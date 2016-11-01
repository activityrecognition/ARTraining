#!/usr/bin/env python
import requests, os, sys, ast
import boto, math
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = 'AKIAIH6U3BHRJNGZE54Q'     # enter your access key id
AWS_SECRET_ACCESS_KEY = 'Aga7Q9FXMLQvtpvNpzc10ju+2MQYHDWKaWtDZtVV' # enter y$
bucket_name = 'thermset'

# connect to the bucket
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
                AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket(bucket_name)

key_name="thermset_v1.tar"
file_path="../ARThermal/thermix_dataset_v1.tar"
v1 = bucket.new_key(key_name)
mp = bucket.initiate_multipart_upload(key_name)

source_size = os.stat(file_path).st_size
bytes_per_chunk = 256*1024*1024
chunks_count = int(math.ceil(source_size / float(bytes_per_chunk)))

for i in range(chunks_count):
    offset = i * bytes_per_chunk
    remaining_bytes = source_size - offset
    bytes = min([bytes_per_chunk, remaining_bytes])
    part_num = i + 1

    print "uploading part " + str(part_num) + " of " + str(chunks_count)

    with open(file_path, 'r') as fp:
            fp.seek(offset)
            mp.upload_part_from_file(fp=fp, part_num=part_num, size=bytes)

if len(mp.get_all_parts()) == chunks_count:
    mp.complete_upload()
    print "upload_file done"
else:
    mp.cancel_upload()
    print "upload_file failed"
#v1.set_contents_from_filename("../ARThermal/thermix_dataset_v1.tar")