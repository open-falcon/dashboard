#-*- coding:utf-8 -*-
import random
import string

def randbytes(bytes_):
    return ''.join(random.sample(string.ascii_letters + string.digits, bytes_))

def random_string (length):
    return ''.join(random.choice(string.letters) for ii in range (length + 1))

