import queue
import threading


class MediaController:
    """
    Pauses/resumes Spotify through the API (explicit commands, never a toggle).
    Calls run in a background thread so the camera loop never freezes.
    """

    def __init__(self, sp):
        self.sp = sp
        self.paused_by_app = False
        self.device_id = None
        self._q = queue.Queue()
        threading.Thread(target=self._worker, daemon=True).start()

    def push(self, event):
        self._q.put(event)

    def _worker(self):
        while True:
            event = self._q.get()
            try:
                if event == "left":
                    self._pause()
                elif event == "returned":
                    self._resume()
            except Exception as e:
                print(f"[media] error on '{event}': {e}")

    def _pause(self):
        pb = self.sp.current_playback()
        if pb and pb.get("device"):
            self.device_id = pb["device"]["id"]
        if pb and pb.get("is_playing"):
            self.sp.pause_playback(device_id=self.device_id)
            self.paused_by_app = True      # only set after the pause succeeded
            print("[media] left -> paused")
        else:
            print("[media] left -> nothing was playing, nothing to do")

    def _resume(self):
        if self.paused_by_app:
            self.sp.start_playback(device_id=self.device_id)
            self.paused_by_app = False     # only cleared after the resume succeeded
            print("[media] returned -> resumed")
        else:
            print("[media] returned -> we hadn't paused, leaving it alone")
