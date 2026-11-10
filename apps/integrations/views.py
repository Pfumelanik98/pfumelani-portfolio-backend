import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

STALE_CACHE_SECONDS = 24 * 60 * 60

class GitHubRepositoriesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        username = settings.GITHUB_USERNAME
        cache_key = f"github_public_repos_v1_{username}"
        stale_cache_key = f"{cache_key}_stale"
        cached = cache.get(cache_key)
        if cached is not None:
            return Response({"source": "cache", "username": username, "repositories": cached})
        try:
            response = requests.get(
                f"{settings.GITHUB_API_BASE_URL}/users/{username}/repos",
                params={"sort": "updated", "per_page": 12, "type": "owner"},
                headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"},
                timeout=8,
            )
            response.raise_for_status()
            repos = [{"name": r["name"], "description": r.get("description"), "html_url": r["html_url"],
                      "language": r.get("language"), "stargazers_count": r.get("stargazers_count", 0),
                      "updated_at": r.get("updated_at"), "fork": r.get("fork", False)} for r in response.json()]
            cache.set(cache_key, repos, timeout=settings.GITHUB_CACHE_SECONDS)
            cache.set(stale_cache_key, repos, timeout=STALE_CACHE_SECONDS)
            return Response({"source": "github_api", "username": username, "repositories": repos})
        except requests.RequestException:
            stale = cache.get(stale_cache_key)
            if stale is not None:
                return Response({"source": "stale_cache", "username": username, "repositories": stale})
            return Response({"detail": "GitHub repository information is temporarily unavailable."}, status=503)
