from uuid import uuid4

from day5.util.myutil import myuuid

s = {"128位uuid": {'k1': 'v1', 'k2': 'v2'},
     "128位uuid2": {'k1': 'v3', 'k2': 'v4'}}


class Session:
    def __init__(self, handler):
        self.handler = handler

    def __getitem__(self, key):
        print('getitem方法被触发,key', key)
        # 找到‘凭证’的值
        c = self.handler.get_cookie('uid')
        if c:
            d = s.get(c, None)
            if d:
                v = d.get(key,None)
                return v
            else:
                return None
        else:
            return None

    def __setitem__(self, key, value):
        print('setitem方法被触发key', key, 'value', value)
        c = self.handler.get_cookie('uid')
        if c:
            d = s.get(c, None)
            if d:
                d[key] = value
            else:
                d = {}
                d[key] = value
                s[c] = d
        else:
            u = myuuid(uuid4())
            d={}
            d[key] = value
            s[u] = d
            self.handler.set_cookie('uid', u, expires_days=10)


