import cv2, numpy as np

def detect_lanes(frame):
    """Classical lane detection: Canny -> ROI mask -> Hough -> averaged left/right lines."""
    h, w = frame.shape[:2]
    edges = cv2.Canny(cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (5, 5), 0), 50, 150)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, [np.array([[(0, h), (int(w * .45), int(h * .6)), (int(w * .55), int(h * .6)), (w, h)]], np.int32)], 255)
    lines = cv2.HoughLinesP(cv2.bitwise_and(edges, mask), 1, np.pi / 180, 40, minLineLength=40, maxLineGap=100)
    sides = {"l": [], "r": []}
    for l in (lines if lines is not None else []):
        x1, y1, x2, y2 = l[0]
        if x2 == x1: continue
        m = (y2 - y1) / (x2 - x1)
        if abs(m) < 0.4: continue
        sides["l" if m < 0 else "r"].append((m, y1 - m * x1))
    out = []
    for k in sides:
        if sides[k]:
            m, b = np.mean(sides[k], axis=0)
            out.append([int((h - b) / m), h, int((h * .62 - b) / m), int(h * .62)])
    return out
