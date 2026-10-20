from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SCOPES = "user-read-playback-state user-modify-playback-state"


def make_client():
    load_dotenv()
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope=SCOPES, cache_path=".spotify_cache")
    )
