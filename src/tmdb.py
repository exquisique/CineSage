import os
import requests
from typing import List, Dict, Any

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# Genre Mapping for "Moods"
MOOD_GENRES = {
    "chill": [35, 10751], # Comedy, Family
    "intense": [28, 53, 27], # Action, Thriller, Horror
    "emotional": [18, 10749], # Drama, Romance
    "educational": [99, 36], # Documentary, History
    "scifi": [878, 14], # Sci-Fi, Fantasy
    "neutral": []
}

def _get(endpoint: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY environment variable is not set.")
    
    params["api_key"] = TMDB_API_KEY
    url = f"{BASE_URL}{endpoint}"
    
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def search_content(query: str) -> List[Dict[str, Any]]:
    """Search for movies and TV shows."""
    data = _get("/search/multi", {"query": query})
    results = data.get("results", [])
    # Filter out people, only keep movie/tv
    return [r for r in results if r["media_type"] in ["movie", "tv"]]

def get_details(media_type: str, tmdb_id: int) -> Dict[str, Any]:
    """Get detailed info including runtime."""
    return _get(f"/{media_type}/{tmdb_id}")

def get_recommendations(tmdb_id: int) -> List[Dict[str, Any]]:
    """Get recommendations based on a specific movie ID."""
    data = _get(f"/movie/{tmdb_id}/recommendations")
    return data.get("results", [])

def get_watch_providers(media_type: str, tmdb_id: int, region: str = "IN") -> List[str]:
    """Get streaming providers for a specific movie/show."""
    data = _get(f"/{media_type}/{tmdb_id}/watch/providers")
    results = data.get("results", {})
    
    if region in results:
        # Get 'flatrate' (subscription) providers
        providers = results[region].get("flatrate", [])
        return [p["provider_name"] for p in providers]
    
    return []

def discover_by_mood(mood: str = "neutral", min_rating: float = 0) -> List[Dict[str, Any]]:
    """Discover movies based on mood (mapped to genres)."""
    genres = MOOD_GENRES.get(mood.lower(), [])
    
    params = {
        "sort_by": "popularity.desc",
        "vote_average.gte": min_rating,
        "vote_count.gte": 100 # Ensure meaningful ratings
    }
    
    if genres:
        # Join genres with pipe for OR logic
        params["with_genres"] = "|".join(map(str, genres))
    elif min_rating == 0:
        # If no mood and no rating, just return trending
        return get_trending()
    
    data = _get("/discover/movie", params)
    return data.get("results", [])

def get_trending() -> List[Dict[str, Any]]:
    data = _get("/trending/all/week")
    return data.get("results", [])

def format_result(item: Dict[str, Any]) -> str:
    title = item.get("title") or item.get("name")
    date = item.get("release_date") or item.get("first_air_date") or "Unknown"
    overview = item.get("overview", "")[:150] + "..."
    rating = item.get("vote_average", "N/A")
    return f"**{title}** ({date[:4]}) - Rating: {rating}/10\n> {overview}\n"
