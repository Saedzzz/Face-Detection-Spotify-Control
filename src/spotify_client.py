from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Only what we need now: read playback state, pause/resume
SCOPES = "user-read-playback-state user-modify-playback-state"


def make_client():
    # Reads SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI from .env
    load_dotenv()
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope=SCOPES, cache_path=".spotify_cache")
    )
