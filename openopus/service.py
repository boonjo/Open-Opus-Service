import random

from .client import OpenOpusClient
from .cache import TTLCache
from .models import Composer, Work


def _parse_composer(c: dict) -> Composer:
    return Composer(
        id=int(c["id"]),
        name=c.get("complete_name") or c.get("name", ""),
        birth=c["birth"] if c.get("birth") else None,
        death=c["death"] if c.get("death") else None,
        epoch=c["epoch"],
        portrait=c["portrait"] if c.get("portrait") else None,
    )


def _parse_work(w: dict) -> Work:
    return Work(
        id=w["id"],
        title=w["title"],
        genre=w["genre"],
        subtitle=w.get("subtitle") or None,
    )


class OpenOpus:
    """
    Open Opus Service

    :param cache: TTLCache instance, defaults to None
    :type cache: TTLCache, optional
    """
    def __init__(self, cache=None):
        """Constructor method"""
        self.client = OpenOpusClient()
        self.cache = cache or TTLCache(3600)

    def composers(self) -> list[Composer]:
        """
        Returns all composers

        :return: A list of Composer objects
        :rtype: list[Composer]
        """
        key = "composers"
        cached = self.cache.get(key)
        if cached: return cached

        data = self.client.list_composers()
        composers = [_parse_composer(c) for c in data["composers"]]

        self.cache.set(key, composers)
        return composers

    def composer(self, composer_id: int) -> Composer:
        """
        Returns a single Composer by ID

        :param composer_id: Composer ID
        :return: Composer object
        """
        key = f"composer:{composer_id}"
        cached = self.cache.get(key)
        if cached: return cached

        data = self.client.get_composer(composer_id)
        composer = _parse_composer(data["composers"])
        self.cache.set(key, composer)
        return composer

    def composers_by_name(self, name: str) -> list[Composer]:
        """
        Returns all composers matching the given name, a partial match search

        :param name: Name of composer
        :return: List of Composer objects
        """
        key = f"composers:name:{name}"
        cached = self.cache.get(key)
        if cached: return cached

        data = self.client.search_composers(name)
        composers = [_parse_composer(c) for c in data["composers"]]

        self.cache.set(key, composers)
        return composers

    def composers_by_period(self, period: str) -> list[Composer]:
        """
        Returns composers matching the specific classical period

        Use periods() to receive all valid periods

        :param period: Period of classical music
        :return: List of Composer objects
        """
        key = f"composers:period:{period}"
        cached = self.cache.get(key)
        if cached: return cached

        data = self.client.composers_by_period(period)
        composers = [_parse_composer(c) for c in data["composers"]]

        self.cache.set(key, composers)
        return composers

    def works(self, composer_id: int, genre: str = "all") -> list[Work]:
        """
        Returns works by a composer, optionally filtered by genre

        :param composer_id: Composer ID
        :param genre: Genre filter (e.g. "Keyboard", "Orchestral"); defaults to "all"
        :return: List of Work objects
        """
        key = f"works:{composer_id}:{genre}"
        cached = self.cache.get(key)
        if cached: return cached

        data = self.client.works_by_composer(composer_id, genre=genre)
        works = [_parse_work(w) for w in data["works"]]

        self.cache.set(key, works)
        return works

    def work_detail(self, work_id: int) -> Work:
        """
        Returns detailed information for a single work

        :param work_id: Work ID
        :return: Work object
        """
        key = f"work:{work_id}"
        cached = self.cache.get(key)
        if cached: return cached

        data = self.client.work_detail(work_id)
        work = _parse_work(data["work"])
        self.cache.set(key, work)
        return work

    def random_composer(self) -> Composer:
        """
        Returns a randomly selected composer from the full catalogue

        :return: Composer object
        """
        return random.choice(self.composers())

    def random_work(self, composer_id: int) -> Work:
        """
        Returns a randomly selected work by the given composer

        :param composer_id: Composer ID
        :return: Work object
        """
        return random.choice(self.works(composer_id))

    def periods(self) -> set[str]:
        """
        Returns all valid classical music periods

        :return: Set of valid periods
        """
        return self.client.get_periods()
