import sys
import struct
import random

import redis

from settings import POST_CARDINALITY
from settings import USER_CARDINALITY


client = redis.StrictRedis()


def uid_to_str(uid):
    return struct.pack('l', uid)

def str_to_uid(string):
    return struct.unpack('l', string)[0]

for key in xrange(POST_CARDINALITY):
    num_uids = int(random.random() * USER_CARDINALITY)
    for uid_number in xrange(num_uids):
        while not client.sadd(str(key), uid_to_str(random.randint(1, int(10*USER_CARDINALITY)))):
            pass
    sys.stderr.write('.')

