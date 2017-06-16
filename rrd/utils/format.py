#!/bin/env python
# Copyright 2017 Xiaomi, Inc.
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



import re

old_pattern = re.compile(r'%\w')
new_pattern = re.compile(r'\{(\w+(\.\w+|\[\w+\])?)\}')

__formaters = {}

def format(text, *a, **kw):
    f = __formaters.get(text)
    if f is None:
        f = formater(text)
        __formaters[text] = f
    return f(*a, **kw)
    #return formater(text)(*a, **kw)

def formater(text):
    """
    >>> format('%s %s', 3, 2, 7, a=7, id=8)
    '3 2'
    >>> format('%(a)d %(id)s', 3, 2, 7, a=7, id=8)
    '7 8'
    >>> format('{1} {id}', 3, 2, a=7, id=8)
    '2 8'
    >>> class Obj: id = 3
    >>> format('{obj.id} {0.id}', Obj(), obj=Obj())
    '3 3'
    """
#    def arg(k,a,kw):
#        if k.isdigit():
#            return a[int(k)]
#        return kw[k]
    def translator(k):
        if '.' in k:
            name,attr = k.split('.')
            if name.isdigit():
                k = int(name)
                return lambda *a, **kw: getattr(a[k], attr)
            return lambda *a, **kw: getattr(kw[name], attr)
#        elif '[' in k and k.endswith(']'):
#            name,index = k[:k.index('[')],k[k.index('[')+1:-1]
#            def _(*a, **kw):
#                if index.isdigit():
#                    return arg(name,a,kw)[int(index)]
#                return arg(name,a,kw)[index]
#            return _
        else:
            if k.isdigit():
                return lambda *a, **kw: a[int(k)]
            return lambda *a, **kw: kw[k]
    args = [translator(k) for k,_1 in new_pattern.findall(text)]
    if args:
        if old_pattern.findall(text):
            raise Exception('mixed format is not allowed')
        f = new_pattern.sub('%s', text)
        def _(*a, **kw):
            return f % tuple([k(*a,**kw) for k in args])
        return _
    elif '%(' in text:
        return lambda *a, **kw: text % kw 
    else:
        n = len(old_pattern.findall(text))
        return lambda *a, **kw: text % tuple(a[:n])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
