from unittest.mock import Mock, patch

import requests
from django.core.cache import cache
from django.test import TestCase, override_settings


@override_settings(GITHUB_USERNAME="test-owner", GITHUB_CACHE_SECONDS=0)
class GitHubRepositoryCacheTests(TestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_stale_repositories_are_returned_after_fresh_cache_expires(self):
        github_response = Mock()
        github_response.json.return_value = [{
            "name": "portfolio",
            "html_url": "https://github.com/test-owner/portfolio",
        }]
        github_response.raise_for_status.return_value = None

        with patch("apps.integrations.views.requests.get", return_value=github_response):
            fresh_response = self.client.get("/api/v1/github/repositories/")

        self.assertEqual(fresh_response.status_code, 200)
        self.assertEqual(fresh_response.json()["source"], "github_api")

        with patch(
            "apps.integrations.views.requests.get",
            side_effect=requests.ConnectionError,
        ):
            stale_response = self.client.get("/api/v1/github/repositories/")

        self.assertEqual(stale_response.status_code, 200)
        self.assertEqual(stale_response.json()["source"], "stale_cache")
        self.assertEqual(stale_response.json()["repositories"][0]["name"], "portfolio")
