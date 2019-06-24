from redis.connection import BlockingConnectionPool
import redis
import random

class DBclient(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.__conn = redis.Redis(connection_pool=BlockingConnectionPool(**kwargs))

    def get(self, proxy):
            data = self.__conn.hget(name=self.name, key=proxy)
            if data:
                return data.decode('utf-8')
            else:
                return None
                
    def find(self):
        proxies = self.__conn.hkeys(self.name)
        # if proxies:
            # proxy = random.choice(proxies)
            # value = self.__conn.hget(self.name, proxy)
            # return {'proxy': proxy.decode('utf-8'),
                    # 'value': value.decode('utf-8')}
        # return None
        if proxies:
            proxy = random.choice(proxies)
            return proxy.decode('utf-8')
        return None      

    def put(self, proxy, num=1):
        data = self.__conn.hset(self.name, proxy, num)
        return data

    def delete(self, key):
        self.__conn.hdel(self.name, key)

    def update(self, key, value):
        self.__conn.hincrby(self.name, key, value)

    def pop(self):
        proxies = self.__conn.hkeys(self.name)
        if proxies:
            proxy = random.choice(proxies)
            value = self.__conn.hget(self.name, proxy)
            self.delete(proxy)
            return {'proxy': proxy.decode('utf-8'),
                    'value': value.decode('utf-8')}
        return None

    def exists(self, key):
        return self.__conn.hexists(self.name, key)

    def getAll(self):
        item_dict = self.__conn.hgetall(self.name)
        return {key.decode('utf8'): value.decode('utf8') for key, value in item_dict.items()}

    def getNumber(self):
        return self.__conn.hlen(self.name)

    def changeTable(self, name):
        self.name = name
        
if __name__ == '__main__':
    c = DBclient(name='useful_proxy', host='127.0.0.1', port=6379, password=None)
    print(c.find())        