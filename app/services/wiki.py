from __future__ import annotations

from typing import Optional
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

WIKI_TITLES = {
    "setosa": "Iris_setosa",
    "versicolor": "Iris_versicolor",
    "virginica": "Iris_virginica",
}

def build_session(user_agent: str) -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})

    retry = Retry(
        total=2,
        backoff_factor=0.3,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

class WikiThumbnailService:
    def __init__(self, session: requests.Session, timeout_sec: float, enabled: bool = True):
        self.session = session
        self.timeout_sec = timeout_sec
        self.enabled = enabled
        self._cache: dict[str, Optional[str]] = {}

    def get_thumbnail(self, class_name: str) -> Optional[str]:
        if not self.enabled:
            return None

        title = WIKI_TITLES.get(class_name)
        if not title:
            return None

        if title in self._cache:
            return self._cache[title]

        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
        try:
            r = self.session.get(url, timeout=self.timeout_sec)
            if r.status_code != 200:
                self._cache[title] = None
                return None
            data = r.json()
            thumb = (data.get("thumbnail") or {}).get("source")
            self._cache[title] = thumb
            return thumb
        except requests.RequestException:
            self._cache[title] = None
            return None
