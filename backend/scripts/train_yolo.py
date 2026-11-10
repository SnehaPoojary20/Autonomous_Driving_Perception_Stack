from ultralytics import YOLO, settings
settings.update({"wandb": True})   # Ultralytics logs to Weights & Biases after `wandb login`
m = YOLO("yolov8n.pt")
m.train(data="configs/bdd100k.yaml", epochs=30, imgsz=640, batch=16, project="av-perception", name="yolov8n-bdd100k", plots=True)
print(m.val())
