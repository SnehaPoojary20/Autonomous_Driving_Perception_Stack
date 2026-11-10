import base64, json, os, cv2, numpy as np
from fastapi import FastAPI, File, UploadFile, WebSocket, Form
from fastapi.middleware.cors import CORSMiddleware
from .pipeline.perception import Perception

app = FastAPI(title="Perception Stack API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
_p = None

def pipe():
    global _p
    if _p is None:
        _p = Perception(os.getenv("YOLO_WEIGHTS", "yolov8n.pt"), use_depth=os.getenv("USE_DEPTH", "1") == "1")
    return _p

def enc(img):
    return "data:image/jpeg;base64," + base64.b64encode(cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 80])[1]).decode()

@app.get("/api/health")
def health(): return {"status": "ok"}

@app.post("/api/perceive")
async def perceive(file: UploadFile = File(...), lanes: bool = Form(True), depth: bool = Form(True), conf: float = Form(0.35)):
    frame = cv2.imdecode(np.frombuffer(await file.read(), np.uint8), cv2.IMREAD_COLOR)
    img, meta = pipe().run(frame, lanes, depth, conf)
    return {"image": enc(img), **meta}

@app.websocket("/ws/stream")
async def stream(ws: WebSocket):
    """Send JPEG bytes (webcam / CARLA bridge); receive annotated frame + metadata."""
    await ws.accept()
    try:
        while True:
            frame = cv2.imdecode(np.frombuffer(await ws.receive_bytes(), np.uint8), cv2.IMREAD_COLOR)
            img, meta = pipe().run(frame)
            await ws.send_text(json.dumps({"image": enc(img), **meta}))
    except Exception:
        pass

@app.get("/api/benchmark")
def benchmark():
    p = "results/benchmark.json"
    return json.load(open(p)) if os.path.exists(p) else {"results": []}
