import torch
from ultralytics import YOLO
import ultralytics.nn.tasks

# Allowlist DetectionModel global
with torch.serialization.safe_globals([ultralytics.nn.tasks.DetectionModel]):
    model = YOLO("fire_smoke_yolov8_densenet.pt")  # full model
