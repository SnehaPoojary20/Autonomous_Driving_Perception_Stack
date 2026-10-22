# Autonomous Driving Perception Stack

A modular computer vision project for autonomous-driving perception experiments. The goal is to detect vehicles and pedestrians, identify lane boundaries, track objects across video frames, estimate relative depth, and visualize results in a driving simulator.

**Status:** Initial frontend and backend setup. Perception models and simulator integration are planned.

## Overview

The project aims to combine multiple perception components into a unified pipeline:

- **Object detection:** Identify vehicles, pedestrians, and other road users using YOLO.
- **Multi-object tracking:** Maintain object identities across frames using ByteTrack or DeepSORT.
- **Lane detection:** Detect lane boundaries using OpenCV and evaluate a segmentation-based alternative.
- **Depth estimation:** Estimate relative scene depth using MiDaS.
- **Simulation:** Stream virtual camera frames from CARLA, with ROS 2 integration as a planned extension.
- **Performance optimization:** Benchmark inference latency and FPS, with ONNX and TensorRT as optimization options.

## Technology Stack

| Component | Technology |
|---|---|
| Backend API | Python, FastAPI, Uvicorn |
| Frontend | React, Vite, JavaScript |
| Computer vision | OpenCV, NumPy |
| Object detection | YOLO / Ultralytics (planned) |
| Object tracking | ByteTrack or DeepSORT (planned) |
| Lane perception | OpenCV, segmentation models (planned) |
| Depth estimation | MiDaS (planned) |
| Simulation | CARLA, ROS 2 (planned) |
| Optimization | ONNX, TensorRT (planned) |
| Testing | pytest, HTTPX |
| Version control | Git, GitHub |

## Architecture

```text
React Frontend
      |
      | HTTP / REST API
      v
FastAPI Backend
      |
      v
Perception Pipeline
  |       |       |
 YOLO   Tracking  Lane Detection
      |
      v
Depth Estimation
      |
      v
Annotated Frames and Metrics
```

The current starter backend exposes a health-check endpoint. The perception pipeline will be integrated incrementally.

## Project Structure

```text
Autonomous_Driving_Perception_Stack/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── perception/
│   │   ├── utils/
│   │   ├── __init__.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── index.html
├── docs/
├── tests/
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.12 recommended for the initial environment.
- Node.js compatible with the installed Vite version.
- npm and Git.
- VS Code or another code editor.

CARLA, ROS 2, and a compatible GPU are not required to run the initial frontend and backend.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/SnehaPoojary20/Autonomous_Driving_Perception_Stack.git
cd Autonomous_Driving_Perception_Stack
```

### 2. Set up the backend

Create and activate a virtual environment in PowerShell:

```powershell
py -3.12 -m venv backend\.venv
.\backend\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

Start the API from the project root:

```powershell
python -m uvicorn app.main:app --reload --app-dir backend
```

Backend URLs:

- API home: http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/api/health
- Interactive API docs: http://127.0.0.1:8000/docs

### 3. Set up the frontend

Open a second terminal:

```powershell
cd frontend
npm install
```

Create a `frontend/.env` file:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the development server:

```powershell
npm run dev
```

Open the URL printed in the terminal, usually http://localhost:5173.

Keep both development servers running while using the application.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API information |
| GET | `/api/health` | Check backend availability |
| GET | `/docs` | Explore API documentation |

Additional endpoints for media upload, perception inference, and processing metrics will be added as the pipeline is implemented.

## Dataset and Model Plan

Potential datasets:

- [KITTI Vision Benchmark Suite](https://www.cvlibs.net/datasets/kitti/)
- [BDD100K](https://bdd-data.berkeley.edu/)

Planned workflow:

1. Inspect dataset labels, annotation formats, and class distribution.
2. Prepare training and evaluation data.
3. Fine-tune an object detector and evaluate detection quality.
4. Add tracking, lane detection, and depth estimation.
5. Integrate camera frames from CARLA.
6. Measure FPS, inference latency, and model quality.
7. Evaluate ONNX or TensorRT optimization where supported.

Dataset access, model weights, dependencies, and hardware requirements may vary.

## Testing

Install the test dependencies from `backend/requirements.txt`.

Run tests from the project root after adding test cases:

```powershell
python -m pytest backend/tests
```

The initial testing plan includes API health checks, invalid-input handling, image-processing tests, and perception pipeline tests.

## Evaluation Metrics

Report only measurements obtained from actual experiments.

- Detection: precision, recall, and mAP.
- Tracking: identity consistency and suitable tracking metrics.
- Lane detection: segmentation metrics or lane-specific evaluation.
- Runtime: FPS and per-frame inference latency.
- Robustness: behavior with missing frames, invalid media, and difficult lighting.

Record the dataset split, hardware, model configuration, and evaluation procedure alongside results.

## Limitations and Safety

This project is an educational prototype and is not designed or validated for real-world vehicle control.

Monocular depth estimates are not automatically accurate distances in meters. Real-world deployment would require appropriate calibration, validation, safety engineering, and testing.

## Future Work

- Integrate object detection and multi-object tracking.
- Add lane segmentation and relative depth visualization.
- Build a media-processing API and annotated-frame viewer.
- Connect CARLA and ROS 2.
- Benchmark model optimization.
- Document experiments, limitations, and reproducible results.

## Author

**Sneha Poojary**

GitHub: [SnehaPoojary20](https://github.com/SnehaPoojary20)

Project repository: [Autonomous_Driving_Perception_Stack](https://github.com/SnehaPoojary20/Autonomous_Driving_Perception_Stack)
