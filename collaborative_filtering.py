import json
import uuid
import sys

import redis

from settings import  POST_CARDINALITY

client = redis.StrictRedis()

def compare(post_a_id, post_b_id, pipe=None):
    intersection_key = uuid.uuid4()
    union_key = uuid.uuid4()
    pipe.sinterstore(intersection_key, post_a_id, post_b_id)
    pipe.sunionstore(union_key, post_a_id, post_b_id)
    pipe.delete(intersection_key)
    pipe.delete(union_key)

results = []
with open('results.dat', 'a+') as fp:
    for post_a_id in xrange(POST_CARDINALITY):
        pipe = client.pipeline()
        for post_b_id in xrange(post_a_id+1, POST_CARDINALITY):
            compare(post_a_id, post_b_id, pipe=pipe) 
            sys.stderr.write('.')
        pipe.execute()

