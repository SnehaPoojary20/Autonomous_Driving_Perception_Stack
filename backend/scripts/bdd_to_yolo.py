"""Convert BDD100K detection JSON -> YOLO txt. Usage: python scripts/bdd_to_yolo.py labels.json out_labels_dir"""
import json, sys, os
NAMES = ["car", "truck", "bus", "person", "rider", "bike", "motor", "traffic light", "traffic sign"]
W, H = 1280, 720
data = json.load(open(sys.argv[1])); os.makedirs(sys.argv[2], exist_ok=True)
count = {n: 0 for n in NAMES}
for item in data:
    lines = []
    for l in item.get("labels", []):
        if l["category"] in NAMES and "box2d" in l:
            b = l["box2d"]; count[l["category"]] += 1
            lines.append(f'{NAMES.index(l["category"])} {(b["x1"]+b["x2"])/2/W:.6f} {(b["y1"]+b["y2"])/2/H:.6f} {(b["x2"]-b["x1"])/W:.6f} {(b["y2"]-b["y1"])/H:.6f}')
    open(os.path.join(sys.argv[2], item["name"].rsplit(".", 1)[0] + ".txt"), "w").write("\n".join(lines))
print("Class balance:", count)
