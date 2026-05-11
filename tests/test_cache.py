import time
from openopus.cache import TTLCache


def test_cache_set_get():
    cache = TTLCache(ttl_seconds=1)
    cache.set("key", "67")
    assert cache.get("key") == "67"


def test_cache_expiry():
    cache = TTLCache(ttl_seconds=0.1)
    cache.set("key", "67")
    time.sleep(0.2)
    assert cache.get("key") is None


def test_cache_invalidate():
    cache = TTLCache(ttl_seconds=60)
    cache.set("key", "value")
    cache.invalidate("key")
    assert cache.get("key") is None


def test_cache_invalidate_missing_key_is_noop():
    cache = TTLCache(ttl_seconds=60)
    cache.invalidate("nonexistent")  # must not raise


def test_cache_clear():
    cache = TTLCache(ttl_seconds=60)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.clear()
    assert cache.get("a") is None
    assert cache.get("b") is None
