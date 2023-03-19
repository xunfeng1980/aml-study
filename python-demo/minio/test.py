# -*- coding: utf-8 -*-
# MinIO Python Library for Amazon S3 Compatible Cloud Storage,
# (C) 2015 MinIO, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Note: YOUR-ACCESSKEYID, YOUR-SECRETACCESSKEY, my-bucketname and my-prefixname
# are dummy values, please replace them with original values.

from minio import Minio

client = Minio('127.0.0.1:59002',
               access_key='admin',
               secret_key='12345678',
               secure=False)

# List all object paths in bucket that begin with my-prefixname.
objects = client.list_objects('myjfs', prefix='/',
                              recursive=True)
for obj in objects:
    print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
          obj.etag, obj.size, obj.content_type)

# List all object paths in bucket that begin with my-prefixname using
# V2 listing API.
# objects = client.list_objects_v2('myjfs', prefix='/',
#                                  recursive=False)
# for obj in objects:
#     print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
#           obj.etag, obj.size, obj.content_type)