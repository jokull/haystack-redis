import os
from cStringIO import StringIO
from threading import Lock

from redis import from_url as redis

from whoosh.index import _DEF_INDEX_NAME, EmptyIndexError
from whoosh.qparser import QueryParser
from whoosh.filedb.structfile import StructFile
from whoosh.filedb.filestore import Storage, create_index, open_index

from haystack.backends.whoosh_backend import WhooshSearchBackend, WhooshEngine

redis_url = os.environ.get('REDISTOGO_URL', 'redis://localhost:6379')


class RedisSearchBackend(WhooshSearchBackend):

    def setup(self):
        """
        Defers loading until needed.
        """
        from haystack import connections

        self.storage = RedisStorage(self.path)

        self.content_field_name, self.schema = self.build_schema(connections[self.connection_alias].get_unified_index().all_searchfields())
        self.parser = QueryParser(self.content_field_name, schema=self.schema)

        try:
            self.index = self.storage.open_index(schema=self.schema)
        except EmptyIndexError:
            self.index = self.storage.create_index(self.schema)

        self.setup_complete = True


class RedisEngine(WhooshEngine):
    backend = RedisSearchBackend


class RedisStorage(Storage):
    """Storage object that keeps the index in redis.
    """
    supports_mmap = False

    def __file(self, name):
        return self.redis.hget("RedisStore:%s" % self.folder, name)

    def __init__(self, namespace='whoosh'):
        self.folder = namespace
        self.redis = redis(redis_url)
        self.locks = {}

    def create_index(self, schema, indexname=_DEF_INDEX_NAME):
        return create_index(self, schema, indexname)

    def file_modified(self, name):
        return -1

    def open_index(self, indexname=_DEF_INDEX_NAME, schema=None):
        return open_index(self, schema, indexname)

    def list(self):
        return self.redis.hkeys("RedisStore:%s" % self.folder)

    def clean(self):
        self.redis.delete("RedisStore:%s" % self.folder)

    def total_size(self):
        return sum(self.file_length(f) for f in self.list())

    def file_exists(self, name):
        return self.redis.hexists("RedisStore:%s" % self.folder, name)

    def file_length(self, name):
        if not self.file_exists(name):
            raise NameError
        return len(self.__file(name))

    def delete_file(self, name):
        if not self.file_exists(name):
            raise NameError
        self.redis.hdel("RedisStore:%s" % self.folder, name)

    def rename_file(self, name, newname, safe=False):
        if not self.file_exists(name):
            raise NameError("File %r does not exist" % name)
        if safe and self.file_exists(newname):
            raise NameError("File %r exists" % newname)

        content = self.__file(name)
        pl = self.redis.pipeline()
        pl.hdel("RedisStore:%s" % self.folder, name)
        pl.hset("RedisStore:%s" % self.folder, newname, content)
        pl.execute()

    def create_file(self, name, **kwargs):
        def onclose_fn(sfile):
            self.redis.hset("RedisStore:%s" % self.folder, name, sfile.file.getvalue())
        f = StructFile(StringIO(), name=name, onclose=onclose_fn)
        return f

    def open_file(self, name, *args, **kwargs):
        if not self.file_exists(name):
            raise NameError("No such file %r" % name)
        def onclose_fn(sfile):
            self.redis.hset("RedisStore:%s" % self.folder, name, sfile.file.getvalue())
        #print "Opened file %s %s " % (name, self.__file(name))
        return StructFile(StringIO(self.__file(name)), name=name, onclose=onclose_fn, *args, **kwargs)

    def lock(self, name):
        if name not in self.locks:
            self.locks[name] = Lock()
        return self.locks[name]

