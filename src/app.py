import cv2
import mediapipe as mp

from spotify_client import make_client
from presence import PresenceTracker
from media import MediaController

SHOW_PREVIEW = True  # False = run with no window
CAMERA_INDEX = 1


def main():
    media = MediaController(make_client())
    presence = PresenceTracker(absent_after_s=2.0, present_after_s=0.5)

    face_det = mp.solutions.face_detection.FaceDetection(
        model_selection=0,  # 0 = close range, 1 = long range
        min_detection_confidence=0.5,
    )

    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("Could not open the webcam")

    print("Running. Press 'q' in the preview window (or Ctrl+C) to quit.")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_found = bool(face_det.process(rgb).detections)

            event = presence.update(face_found)
            if event:
                print(f"[presence] {event}")
                media.push(event)

            if SHOW_PREVIEW:
                label = "PRESENT" if presence.present else "AWAY"
                color = (0, 200, 0) if face_found else (0, 0, 255)
                cv2.putText(frame, f"{label}  face={face_found}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                cv2.imshow("Presence", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        face_det.close()


if __name__ == "__main__":
    main()
