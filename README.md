# Open Opus
A lightweight Python package that provides a stable interface to the [Open Opus API](https://openopus.org/).

This project exists to decouple application code from the Open Opus API's raw response formats and availability characteristics.

---

## Requirements
- Python >= 3.10

---

## Installation
Library only:
```bash
pip install openopus
```

---

## Quick Start
```python
from openopus import OpenOpus

svc = OpenOpus()

# List all composers
composers = svc.composers()

# Search by name (partial match)
results = svc.composers_by_name("Bach")

# Fetch a single composer
bach = svc.composer(196)

# Get all works by a composer
works = svc.works(196)

# Get works filtered by genre
keyboard_works = svc.works(196, genre="Keyboard")

# Get detailed info for a single work
work = svc.work_detail(1234)

# Get all valid period names
periods = svc.periods()

# Get composers from a specific period
baroque = svc.composers_by_period("Baroque")

# Pick a random composer or work
surprise = svc.random_composer()
surprise_work = svc.random_work(196)
```

---

## API Reference

### `OpenOpus(cache=None)`
Main service class. Accepts an optional cache instance (defaults to an in-memory `TTLCache` with a 1-hour TTL).

#### Composer methods

| Method | Description |
|---|---|
| `composers()` | Return all composers |
| `composer(composer_id)` | Return a single `Composer` by ID |
| `composers_by_name(name)` | Partial-match search by name |
| `composers_by_period(period)` | Filter by classical period |
| `random_composer()` | Return a randomly selected composer |
| `periods()` | Return the set of valid period strings |

#### Work methods

| Method | Description |
|---|---|
| `works(composer_id, genre="all")` | Return works by a composer, optionally filtered by genre |
| `work_detail(work_id)` | Return detailed info for a single work |
| `random_work(composer_id)` | Return a randomly selected work by a composer |

---

## Models

### `Composer`
| Field | Type | Description |
|---|---|---|
| `id` | `int` | Unique composer ID |
| `name` | `str` | Full name |
| `birth` | `str \| None` | Birth year/date |
| `death` | `str \| None` | Death year/date |
| `epoch` | `str` | Musical period |
| `portrait` | `str \| None` | Portrait image URL |

### `Work`
| Field | Type | Description |
|---|---|---|
| `id` | `int` | Unique work ID |
| `title` | `str` | Work title |
| `genre` | `str` | Genre (e.g. "Keyboard", "Orchestral") |
| `subtitle` | `str \| None` | Subtitle or nickname |

---

## Caching

All responses are cached automatically. The default cache is `TTLCache(ttl_seconds=3600)`. You can supply your own compatible object (anything with `get(key)` and `set(key, value)` methods), or use the built-in cache control methods:

```python
from openopus.cache import TTLCache

cache = TTLCache(3600)
svc = OpenOpus(cache=cache)

# Remove a single entry
cache.invalidate("composers")

# Wipe everything
cache.clear()
```

---

## Error Handling

| Exception | When raised |
|---|---|
| `openopus.errors.OpenOpusError` | Non-200 HTTP response from the API, or invalid argument (e.g. unknown period) |
| `openopus.errors.UpstreamUnavailable` | Network timeout or connection failure |

```python
from openopus.errors import OpenOpusError, UpstreamUnavailable

try:
    works = svc.works(196)
except UpstreamUnavailable:
    print("API unreachable, try again later")
except OpenOpusError as e:
    print(f"API error: {e}")
```

---

## Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```
