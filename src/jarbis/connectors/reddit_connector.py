from datetime import datetime
from functools import cached_property
from typing import List, Optional

import requests

from jarbis.models import RedditSourceModel


class RedditConnector:
    BASE_URL = "https://www.reddit.com"
    USER_AGENT = "Mozilla/5.0 (Python:RedditConnector:1.0)"
    DEFAULT_LIMIT = 50
    MAX_LIMIT = 100
    MAX_ITERATIONS = 20

    @cached_property
    def _session(self) -> requests.Session:
        """Crea una sessione HTTP riutilizzabile."""
        session = requests.Session()
        session.headers.update({"User-Agent": self.USER_AGENT})
        return session

    def get_new_subreddit_posts(
        self, subreddit_name: str, limit: int = DEFAULT_LIMIT
    ) -> List[RedditSourceModel]:
        """Recupera i post più recenti da un subreddit."""
        subreddit_name = self._sanitize_subreddit(subreddit_name)
        url = f"{self.BASE_URL}/{subreddit_name}/new.json"

        response = self._session.get(url, params={"limit": limit})
        response.raise_for_status()

        posts = response.json().get("data", {}).get("children", [])
        return [self._extract_post_model(post) for post in posts]

    def get_subreddit_posts_by_date(
        self,
        subreddit_name: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
    ) -> List[RedditSourceModel]:
        """Recupera i post di un subreddit in un range temporale."""
        subreddit_name = self._sanitize_subreddit(subreddit_name)
        start_ts = start_date.timestamp()
        end_ts = end_date.timestamp() if end_date else datetime.now().timestamp()

        results = []
        after = None

        for _ in range(self.MAX_ITERATIONS):
            posts, after = self._fetch_page(subreddit_name, after)

            if not posts:
                break

            # Filtra i post nel range temporale
            filtered_posts = [
                self._extract_post_model(post)
                for post in posts
                if start_ts <= post["data"].get("created_utc", 0) <= end_ts
            ]
            results.extend(filtered_posts)

            # Interrompi se l'ultimo post è precedente alla data di inizio
            last_post_ts = posts[-1]["data"].get("created_utc", 0)
            if last_post_ts < start_ts or not after:
                break

        return results

    def _fetch_page(
        self, subreddit_name: str, after: Optional[str] = None
    ) -> tuple[List[dict], Optional[str]]:
        """Recupera una singola pagina di post."""
        url = f"{self.BASE_URL}/{subreddit_name}/new.json"
        params = {"limit": self.MAX_LIMIT}

        if after:
            params["after"] = after

        response = self._session.get(url, params=params)
        response.raise_for_status()

        data = response.json().get("data", {})
        posts = data.get("children", [])
        next_after = data.get("after")

        return posts, next_after

    @staticmethod
    def _extract_post_model(post: dict) -> RedditSourceModel:
        """Estrae un RedditSourceModel da un post JSON."""
        post_data = post["data"]
        return RedditSourceModel(
            title=post_data.get("title", ""), text=post_data.get("selftext", "")
        )

    @staticmethod
    def _sanitize_subreddit(subreddit_name: str) -> str:
        """Normalizza il nome del subreddit nel formato 'r/nome'."""
        subreddit_name = subreddit_name.strip()

        if subreddit_name.startswith("r/"):
            return subreddit_name

        if subreddit_name.startswith("/"):
            return f"r{subreddit_name}"

        return f"r/{subreddit_name}"


reddit_connector = RedditConnector()