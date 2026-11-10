# Perception Console – Frontend (React + Vite)

## Setup
Requires Node.js 18+.
```bash
npm install
npm run dev        # http://localhost:5173
```
Backend URL lives in `.env` (`VITE_API=http://localhost:8000`). Production build: `npm run build`.

Packages: react, react-dom, lucide-react, vite, @vitejs/plugin-react.
Features: image upload, live camera stream over WebSocket, lane/depth toggles, tracked objects with distance, ONNX/TensorRT benchmark bars.
