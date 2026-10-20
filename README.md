# Face Detection Spotify Control

Real time computer vision application that detects human presence from the webcam and controls spotify music, It combines MediaPipe face detection with a presence state machine, then pause/resume music using Spotify Web API.

**All video is proccessed locally, nothing is stored or uploaded.**

## Tech Stack
- Python
- OpenCV
- MediaPipe
- Spotify Web API.

## Features
- **Face-based presence detection** with MediaPipe Face Detection, runs locally on your webcam.
- **Automatic pause when you leave the frame** and **automatic resume when you return in the frame**.
- **pause/resume commands** through the Spotify API (never a blind play/pause toggle), so the app can't get "inverted" from the real playback state.
- **Respects manual control**: if you paused the music yourself before leaving, it will not start playing when you return.
- **Debounced presence logic**: brief detection drops (looking down, turning your head) don't trigger a pause.
- **Non-blocking**: Spotify network calls run in a background thread, so the camera preview never freezes.
- **Private**: video frames are processed in memory. Nothing is saved or sent anywhere.

## Requirements

- Python **3.9 to 3.12** (`mediapipe==0.10.21` does not support newer versions)
- A webcam
- **Spotify Premium** (the Web API playback controls require it)
- The Spotify app open on a device, so there is an active playback device
- A free Spotify Developer app (see setup below)


## Setup

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Create a Spotify Developer app

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and create an app.
2. Add this Redirect URI to the app settings: `http://127.0.0.1:8888/callback`
3. Copy the **Client ID** and **Client Secret**.

### 3. Configure your credentials

Copy `.env.example` to `.env` and fill in your values:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

The redirect URI in `.env` must match the one in the dashboard exactly.

### 4. Run

```bash
python src/app.py
```

On the first run a browser tab opens asking you to log in to Spotify and approve access. After that the login is cached locally in `.spotify_cache`.

Press `q` in the preview window (or `Ctrl+C` in the terminal) to quit.


## Configuration

| Setting | File | Default | What it does |
|---|---|---|---|
| `absent_after_s` | `src/app.py` | `2.0` | Seconds without a detected face before you count as "left" and music pauses. Raise it if it pauses while you're still at your desk. |
| `present_after_s` | `src/app.py` | `0.5` | Seconds a face must be seen continuously before you count as "returned" and music resumes. Raise it if it resumes when you only walk past. |
| `CAMERA_INDEX` | `src/app.py` | `1` | Which camera to use. Try `0`, `2`, ... if you have virtual cameras or an external webcam. |
| `SHOW_PREVIEW` | `src/app.py` | `True` | Show the camera window with the current status. Set to `False` to run without a window. |
| `model_selection` | `src/app.py` | `0` | `0` = close-range face model (about 2 m), `1` = longer range. |


## Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| `module 'mediapipe' has no attribute 'solutions'` | Newer MediaPipe versions removed this API. Install the pinned version: `pip install mediapipe==0.10.21`. Also make sure no file in your project is named `mediapipe.py`. |
| Music doesn't pause or resume, and `[media] error` appears in the terminal | No active Spotify device. Open Spotify and start playing something once. Also check that your account is Premium. |
| Spotify login fails or asks again | The redirect URI in `.env` doesn't match the dashboard exactly, or `.spotify_cache` is stale. Delete it and log in again. |
| Pauses while you're still sitting there | Face detection loses you when you look down or turn away. Increase `absent_after_s`. |
| Wrong or black camera image | Change `CAMERA_INDEX`, and close any other program that is using the camera. |


## Limitations

- Presence is based on face detection, so it can briefly lose you if your face is turned away or hidden.
- Works with the first person MediaPipe finds in the frame; it does not identify who it is.
- Controls Spotify only.

## Future Goals
- MacOS
- Hand gestures (open palm to play/pause, pinch-and-drag for volume, thumbs up to like a track)
- Configurable settings via a config file or command-line flags
- System tray icon to start and stop the app