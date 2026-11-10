"""Latency/FPS: PyTorch vs ONNX vs TensorRT. Usage: python scripts/benchmark.py a.pt a.onnx [a.engine]"""
import sys, time, json, numpy as np
from ultralytics import YOLO
img = (np.random.rand(640, 640, 3) * 255).astype("uint8"); res = []
for w in sys.argv[1:]:
    m = YOLO(w, task="detect")
    for _ in range(10): m.predict(img, verbose=False)
    t = []
    for _ in range(100):
        s = time.perf_counter(); m.predict(img, verbose=False); t.append((time.perf_counter() - s) * 1000)
    res.append({"model": w, "latency_ms": round(float(np.mean(t)), 2), "p95_ms": round(float(np.percentile(t, 95)), 2), "fps": round(1000 / float(np.mean(t)), 1)})
    print(res[-1])
json.dump({"results": res}, open("results/benchmark.json", "w"), indent=2)
