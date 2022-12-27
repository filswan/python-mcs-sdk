import os
from mcs.api.bucket_api import BucketAPI

if __name__ == '__main__':
    p = 'ceca19d41bb719f947626b798045b92487c36b50f35dc11989eb8d819adead42'
    w = '0xb63a00541747302DA1fF8784Ad633fF10A4EfB63'
    b = BucketAPI('http://192.168.88.41:8889')
    b.get_jwt_token(w, p, 'polygon.mumbai')
    b.create_bucket('new_bucket')
    print(b.get_buckets())
    #b.upload_to_bucket('3b882a36-0e96-407c-b346-4aad6d074109', 'README.md')