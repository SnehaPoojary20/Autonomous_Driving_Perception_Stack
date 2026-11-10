from ultralytics import YOLO

class Detector:
    """YOLO detection + ByteTrack tracking (state kept across calls via persist=True)."""
    def __init__(self, weights="yolov8n.pt"):
        self.model = YOLO(weights)

    def track(self, frame, conf=0.35):
        r = self.model.track(frame, persist=True, tracker="bytetrack.yaml", conf=conf, verbose=False)[0]
        out = []
        if r.boxes is None or len(r.boxes) == 0:
            return out
        ids = r.boxes.id.int().tolist() if r.boxes.id is not None else [-1] * len(r.boxes)
        for b, tid in zip(r.boxes, ids):
            x1, y1, x2, y2 = [float(v) for v in b.xyxy[0]]
            out.append({"id": tid, "cls": self.model.names[int(b.cls)], "conf": round(float(b.conf), 3),
                        "bbox": [x1, y1, x2, y2]})
        return out
