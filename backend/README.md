# Perception Stack – Backend

FastAPI + YOLO/ByteTrack + OpenCV lanes + MiDaS depth + ONNX/TensorRT + CARLA/ROS2.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# GPU: install torch from https://pytorch.org first (match your CUDA)
uvicorn app.main:app --reload --port 8000           # http://localhost:8000/docs
```
Env: `YOLO_WEIGHTS=runs/bdd/weights/best.pt`, `USE_DEPTH=0` to skip MiDaS on weak machines.

## Workflow
1. `python scripts/bdd_to_yolo.py bdd100k_labels_images_train.json datasets/bdd100k_yolo/labels/train` (prints class balance)
2. `wandb login` then `python scripts/train_yolo.py`
3. `python scripts/export_onnx.py runs/bdd/weights/best.pt`
4. `python scripts/benchmark.py best.pt best.onnx best.engine` -> results/benchmark.json (shown in frontend)
5. CARLA + ROS2 (Ubuntu 22.04, ROS2 Humble): run `./CarlaUE4.sh`, then
   `python scripts/carla_camera_node.py` and `python scripts/perception_node.py` in two terminals.

## API
- `POST /api/perceive` multipart: file, lanes, depth, conf -> annotated image, objects (id, cls, bbox, distance_m), lanes, latency_ms, fps
- `WS /ws/stream` send JPEG bytes, receive the same JSON
- `GET /api/benchmark`, `GET /api/health`
