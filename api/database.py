import tarantool

class TarantoolDB:
    def __init__(self):
        self.connection = tarantool.connect('tarantool', 3301)

    def write_batch(self, data):
        for key, value in data.items():
            try:
                existing_record = self.connection.select('kv', key)
                if existing_record:
                    self.connection.update('kv', key, [('=', 1, value)])
                else:
                    self.connection.insert('kv', (key, value))
            except Exception as e:
                raise tarantool.error.DatabaseError(f"Error writing data: {e}")

    def read_batch(self, keys):
        result = {}
        for key in keys:
            try:
                res = self.connection.select('kv', key)
                if res:
                    result[key] = res[0][1]
            except Exception as e:
                raise tarantool.error.DatabaseError(f"Error reading data for key {key}: {e}")
        return result