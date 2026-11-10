import time, math, cv2
from .detector import Detector
from .lanes import detect_lanes
from .distance import fuse, pinhole

class Perception:
    def __init__(self, weights="yolov8n.pt", use_depth=True, hfov_deg=90):
        self.det = Detector(weights)
        self.depth = None
        if use_depth:
            from .depth import Depth
            self.depth = Depth()
        self.hfov = hfov_deg

    def run(self, frame, lanes=True, depth=True, conf=0.35):
        t0 = time.perf_counter()
        h, w = frame.shape[:2]
        focal = (w / 2) / math.tan(math.radians(self.hfov / 2))
        objs = self.det.track(frame, conf)
        if depth and self.depth and objs:
            objs = fuse(objs, self.depth(frame), focal)
        else:
            for o in objs: o["distance_m"] = round(pinhole(o["bbox"], o["cls"], focal), 1)
        ln = detect_lanes(frame) if lanes else []
        out = frame.copy()
        for l in ln: cv2.line(out, (l[0], l[1]), (l[2], l[3]), (80, 220, 120), 5)
        for o in objs:
            x1, y1, x2, y2 = [int(v) for v in o["bbox"]]
            col = (0, 170, 255) if o["cls"] in ("person", "rider") else (255, 120, 40)
            cv2.rectangle(out, (x1, y1), (x2, y2), col, 2)
            cv2.putText(out, f'#{o["id"]} {o["cls"]} {o["distance_m"]}m', (x1, max(y1 - 6, 12)),
                        cv2.FONT_HERSHEY_SIMPLEX, .55, col, 2)
        ms = (time.perf_counter() - t0) * 1000
        return out, {"objects": objs, "lanes": ln, "latency_ms": round(ms, 1), "fps": round(1000 / ms, 1)}
