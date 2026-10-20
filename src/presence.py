import time


class PresenceTracker:

    def __init__(self, absent_after_s=10.0, present_after_s=0.6):
        self.absent_after_s = absent_after_s
        self.present_after_s = present_after_s
        self.present = True
        self._last_seen = time.monotonic()
        self._seen_since = None

    def update(self, face_detected):
        now = time.monotonic()

        if face_detected:
            self._last_seen = now
            if self._seen_since is None:
                self._seen_since = now
            if not self.present and now - self._seen_since >= self.present_after_s:
                self.present = True
                return "returned"
        else:
            self._seen_since = None
            if self.present and now - self._last_seen >= self.absent_after_s:
                self.present = False
                return "left"

        return None
