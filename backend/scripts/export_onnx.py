import sys
from ultralytics import YOLO
m = YOLO(sys.argv[1] if len(sys.argv) > 1 else "yolov8n.pt")
m.export(format="onnx", imgsz=640, opset=17, simplify=True)
# TensorRT engine (NVIDIA GPU + TensorRT installed):
# m.export(format="engine", half=True, imgsz=640)
