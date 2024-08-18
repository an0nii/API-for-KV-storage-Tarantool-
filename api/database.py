import tarantool

class TarantoolDB:
    def __init__(self):
        self.connection = tarantool.connect('tarantool', 3301)

    def write_batch(self, data):
        for key, value in data.items():
            self.connection.insert('kv', (key, value))

    def read_batch(self, keys):
        result = {}
        for key in keys:
            res = self.connection.select('kv', key)
            if res:
                result[key] = res[0][1]
        return result