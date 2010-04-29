from __future__ import with_statement

import unittest2 as unittest

from redish import client
from redish.tests import config


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(**config.connection)
        self.client.clear()

    def tearDown(self):
        self.client.clear()



class test_Client(ClientTestCase):

    def test_id(self):
        for i in range(1, 10):
            self.assertEqual(self.client.id("Something"), "Something:%s" % i)

    def test_set_get_delete_object(self):
        object = {"foo": "bar", "baz": 1, "xuzzy": 3.14}
        self.client["test:set_object"] = object
        self.assertDictEqual(object, self.client["test:set_object"])

        del(self.client["test:set_object"])
        with self.assertRaises(KeyError):
            self.client["test:set_object"]

    def test_clear(self):
        self.client["test:clear"] = [1, 2, 3]
        self.client.clear()
        with self.assertRaises(KeyError):
            self.client["test:clear"]

    def test_update(self):
        keys = {"test:update:1": 1,
                "test:update:2": 2,
                "test:update:3": 3}
        self.client.update(keys)
        for key, value in keys.items():
            self.assertEqual(self.client[key], value)
        self.client.clear()

    def test_rename(self):
        self.client["test:rename:first"] = "some-value"
        self.client.rename("test:rename:first", "test:rename:second")
        self.assertEqual(self.client["test:rename:second"], "some-value")
        with self.assertRaises(KeyError):
            self.client["test:rename:first"]
        self.client.clear()

    def test_iterkeys(self):
        keys = {"test:iterkeys:1": 1,
                "test:iterkeys:2": 2,
                "test:iterkeys:3": 3,
                "test:iterkeys:4": 4}
        self.client.update(keys)
        self.assertItemsEqual(list(self.client.keys("test:iterkeys:*")),
                keys.keys())
        self.client.clear()

    def test_iteritems(self):
        keys = {"test:iteritems:1": 1,
                "test:iteritems:2": 2,
                "test:iteritems:3": 3,
                "test:iteritems:4": 4}
        self.client.update(keys)
        items = dict(self.client.iteritems("test:iteritems:*"))
        self.assertDictContainsSubset(keys, items)
        self.client.clear()

    def test_itervalues(self):
        keys = {"test:itervalues:1": 1,
                "test:itervalues:2": 2,
                "test:itervalues:3": 3,
                "test:itervalues:4": 4}
        self.client.update(keys)
        values = list(self.client.itervalues("test:itervalues:*"))
        self.assertItemsEqual(values, keys.values())
        self.client.clear()

    def test_pop(self):
        self.client["test:pop"] = "the quick brown fox..."
        item = self.client.pop("test:pop")
        self.assertEqual(item, "the quick brown fox...")
        with self.assertRaises(KeyError):
            self.client["test:pop"]

    def test_get(self):
        self.client["test:get:exists"] = "George Constanza"
        self.assertEqual(self.client.get("test:get:exists"),
                         "George Constanza")
        self.assertIsNone(self.client.get("test:get:nonexistent"))
        self.assertEqual(self.client.get("test:get:nonexistent", 12345),
                         12345)
        self.client.clear()

    def test__len__(self):
        self.client.clear()
        self.assertEqual(len(self.client), 0)
        keys = dict(("test:__len__:%s" % i, i)
                        for i in range(100))
        self.client.update(keys)
        self.assertEqual(len(self.client), 100)
        self.client.clear()
        self.assertEqual(len(self.client), 0)

    def test__contains__(self):
        self.client["test:__contains__:exists"] = "Elaine Marie Benes"
        self.assertIn("test:__contains__:exists", self.client)
        self.assertNotIn("test:__contains__:nonexistent", self.client)
        self.client.clear()

    def test__repr__(self):
        self.assertTrue(repr(self.client))




