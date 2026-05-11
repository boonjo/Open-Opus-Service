import pytest
from unittest.mock import Mock
from openopus.service import OpenOpus
from openopus.models import Composer, Work


class DummyCache:
    """Very small cache used only for unit‑tests"""

    def __init__(self):
        self._store = {}

    def get(self, key):
        return self._store.get(key)

    def set(self, key, value):
        self._store[key] = value

    def invalidate(self, key):
        self._store.pop(key, None)

    def clear(self):
        self._store.clear()


_BACH = {"id": "1", "complete_name": "Johann Sebastian Bach", "birth": "1685",
         "death": "1750", "epoch": "Baroque", "portrait": ""}
_GOLDBERG = {"id": "10", "title": "Goldberg Variations, BWV.988", "genre": "Keyboard", "subtitle": None}


@pytest.fixture
def mock_client(monkeypatch):
    mock = Mock(name="OpenOpusClientMock")
    monkeypatch.setattr("openopus.service.OpenOpusClient", lambda *a, **kw: mock)
    return mock


def test_list_composers_cache(mock_client):
    mock_client.list_composers.return_value = {"composers": [_BACH]}
    svc = OpenOpus(cache=DummyCache())
    composers1 = svc.composers()
    composers2 = svc.composers()  # should use cache

    assert composers1[0].name == "Johann Sebastian Bach"
    assert composers1 == composers2
    assert mock_client.list_composers.call_count == 1


def test_works_for_composer(mock_client):
    mock_client.works_by_composer.return_value = {"works": [_GOLDBERG]}
    svc = OpenOpus(cache=DummyCache())
    works = svc.works(1)
    assert works[0].title == "Goldberg Variations, BWV.988"
    mock_client.works_by_composer.assert_called_once_with(1, genre="all")


def test_works_by_genre(mock_client):
    mock_client.works_by_composer.return_value = {"works": [_GOLDBERG]}
    svc = OpenOpus(cache=DummyCache())
    works = svc.works(1, genre="Keyboard")
    assert works[0].genre == "Keyboard"
    mock_client.works_by_composer.assert_called_once_with(1, genre="Keyboard")


def test_works_genre_cache_key_is_isolated(mock_client):
    mock_client.works_by_composer.return_value = {"works": [_GOLDBERG]}
    svc = OpenOpus(cache=DummyCache())
    svc.works(1, genre="all")
    svc.works(1, genre="Keyboard")
    assert mock_client.works_by_composer.call_count == 2


def test_work_detail(mock_client):
    mock_client.work_detail.return_value = {
        "work": {"id": "10", "title": "Goldberg Variations, BWV.988", "genre": "Keyboard", "subtitle": ""}
    }
    svc = OpenOpus(cache=DummyCache())
    work = svc.work_detail(10)
    assert work.title == "Goldberg Variations, BWV.988"
    assert work.subtitle is None


def test_work_detail_cached(mock_client):
    mock_client.work_detail.return_value = {
        "work": {"id": "10", "title": "Goldberg Variations, BWV.988", "genre": "Keyboard", "subtitle": None}
    }
    svc = OpenOpus(cache=DummyCache())
    svc.work_detail(10)
    svc.work_detail(10)
    assert mock_client.work_detail.call_count == 1


def test_random_composer(mock_client):
    mock_client.list_composers.return_value = {"composers": [_BACH]}
    svc = OpenOpus(cache=DummyCache())
    c = svc.random_composer()
    assert isinstance(c, Composer)


def test_random_work(mock_client):
    mock_client.works_by_composer.return_value = {"works": [_GOLDBERG]}
    svc = OpenOpus(cache=DummyCache())
    w = svc.random_work(1)
    assert isinstance(w, Work)
