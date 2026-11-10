import numpy as np
# Typical real-world heights (m) for the pinhole estimate d = f * H / h_px
HEIGHTS = {"car": 1.5, "truck": 3.0, "bus": 3.2, "person": 1.7, "rider": 1.7, "bike": 1.5, "motor": 1.4}

def pinhole(box, cls, focal_px):
    return focal_px * HEIGHTS.get(cls, 1.5) / max(box[3] - box[1], 1)

def fuse(objs, depth_map, focal_px):
    """Scale MiDaS inverse depth to metres using pinhole estimates, then average both."""
    inv = []
    for o in objs:
        x1, y1, x2, y2 = [int(v) for v in o["bbox"]]
        patch = depth_map[max(y1, 0):y2, max(x1, 0):x2]
        inv.append(float(np.median(patch)) if patch.size else 1e-3)
        o["distance_m"] = pinhole(o["bbox"], o["cls"], focal_px)
    k = np.median([o["distance_m"] * i for o, i in zip(objs, inv)])
    for o, i in zip(objs, inv):
        o["distance_m"] = round(0.5 * o["distance_m"] + 0.5 * k / max(i, 1e-3), 1)
    return objs
