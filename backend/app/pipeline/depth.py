import torch, cv2

class Depth:
    """MiDaS monocular depth (relative inverse depth)."""
    def __init__(self, name="MiDaS_small"):
        self.dev = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = torch.hub.load("intel-isl/MiDaS", name).to(self.dev).eval()
        t = torch.hub.load("intel-isl/MiDaS", "transforms")
        self.tf = t.small_transform if "small" in name else t.dpt_transform

    @torch.no_grad()
    def __call__(self, frame):
        x = self.tf(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).to(self.dev)
        d = self.model(x).unsqueeze(1)
        d = torch.nn.functional.interpolate(d, size=frame.shape[:2], mode="bicubic").squeeze()
        return d.cpu().numpy()
