import { useRef, useState, useEffect } from "react";
import { Upload, Video, Gauge, Route, Ruler, Square } from "lucide-react";

const API = import.meta.env.VITE_API || "http://localhost:8000";
const WS = API.replace("http", "ws") + "/ws/stream";

export default function App() {
  const [tab, setTab] = useState("image");
  const [res, setRes] = useState(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const [opts, setOpts] = useState({ lanes: true, depth: true, conf: 0.35 });
  const [bench, setBench] = useState([]);
  const [live, setLive] = useState(false);
  const video = useRef(); const ws = useRef(); const timer = useRef();

  useEffect(() => { fetch(API + "/api/benchmark").then(r => r.json()).then(d => setBench(d.results || [])).catch(() => {}); }, []);

  async function upload(file) {
    if (!file) return;
    setBusy(true); setErr("");
    const fd = new FormData();
    fd.append("file", file); fd.append("lanes", opts.lanes); fd.append("depth", opts.depth); fd.append("conf", opts.conf);
    try {
      const r = await fetch(API + "/api/perceive", { method: "POST", body: fd });
      if (!r.ok) throw new Error(r.statusText);
      setRes(await r.json());
    } catch (e) { setErr("Can't reach the backend at " + API + ". Start it with: uvicorn app.main:app --port 8000"); }
    setBusy(false);
  }

  async function startLive() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 360 } });
      video.current.srcObject = stream; await video.current.play();
      ws.current = new WebSocket(WS);
      ws.current.onmessage = e => setRes(JSON.parse(e.data));
      ws.current.onerror = () => { setErr("Live stream failed. Is the backend running?"); stopLive(); };
      const c = document.createElement("canvas"); c.width = 640; c.height = 360;
      timer.current = setInterval(() => {
        if (ws.current?.readyState !== 1) return;
        c.getContext("2d").drawImage(video.current, 0, 0, 640, 360);
        c.toBlob(b => b && ws.current.send(b), "image/jpeg", 0.7);
      }, 150);
      setLive(true); setErr("");
    } catch { setErr("Camera access was blocked. Allow it in your browser and try again."); }
  }
  function stopLive() {
    clearInterval(timer.current); ws.current?.close();
    video.current?.srcObject?.getTracks().forEach(t => t.stop());
    setLive(false);
  }

  const objs = res?.objects || [];
  const nearest = objs.length ? Math.min(...objs.map(o => o.distance_m)) : null;

  return (
    <div className="app">
      <header>
        <h1>Perception Console</h1>
        <nav>
          <button className={tab === "image" ? "on" : ""} onClick={() => { stopLive(); setTab("image"); }}><Upload size={16}/> Image</button>
          <button className={tab === "live" ? "on" : ""} onClick={() => setTab("live")}><Video size={16}/> Live camera</button>
        </nav>
      </header>

      <main>
        <section className="stage">
          {tab === "image" ? (
            <label className="drop">
              <input type="file" accept="image/*" hidden onChange={e => upload(e.target.files[0])}/>
              {res ? <img src={res.image} alt="Annotated driving frame"/> :
                <div className="empty"><Upload size={28}/><p>Drop a driving frame here, or click to choose one.</p></div>}
              {busy && <div className="busy">Running pipeline…</div>}
            </label>
          ) : (
            <div className="drop">
              <video ref={video} muted playsInline hidden={!!res && live}/>
              {live && res && <img src={res.image} alt="Live annotated feed"/>}
              {!live && <div className="empty"><Video size={28}/><p>Stream your camera, or pipe CARLA frames to the same socket.</p></div>}
              <button className="primary" onClick={live ? stopLive : startLive}>{live ? <><Square size={14}/> Stop</> : "Start stream"}</button>
            </div>
          )}
          {err && <p className="error" role="alert">{err}</p>}
        </section>

        <aside>
          <div className="stats">
            <Stat icon={<Gauge size={16}/>} label="FPS" value={res?.fps ?? "–"}/>
            <Stat icon={<Gauge size={16}/>} label="Latency" value={res ? res.latency_ms + " ms" : "–"}/>
            <Stat icon={<Ruler size={16}/>} label="Nearest" value={nearest ? nearest + " m" : "–"} warn={nearest && nearest < 8}/>
            <Stat icon={<Route size={16}/>} label="Lanes" value={res ? res.lanes.length : "–"}/>
          </div>

          <div className="card">
            <h2>Pipeline</h2>
            <label className="row"><input type="checkbox" checked={opts.lanes} onChange={e => setOpts({ ...opts, lanes: e.target.checked })}/> Lane detection</label>
            <label className="row"><input type="checkbox" checked={opts.depth} onChange={e => setOpts({ ...opts, depth: e.target.checked })}/> Depth (MiDaS)</label>
            <label className="row col">Confidence {opts.conf.toFixed(2)}
              <input type="range" min="0.1" max="0.9" step="0.05" value={opts.conf} onChange={e => setOpts({ ...opts, conf: +e.target.value })}/></label>
          </div>

          <div className="card">
            <h2>Tracked objects</h2>
            {objs.length === 0 ? <p className="muted">Nothing detected yet.</p> :
              <table><thead><tr><th>ID</th><th>Class</th><th>Conf</th><th>Distance</th></tr></thead>
                <tbody>{objs.map(o => <tr key={o.id + o.cls}><td>#{o.id}</td><td>{o.cls}</td><td>{o.conf}</td><td className={o.distance_m < 8 ? "warn" : ""}>{o.distance_m} m</td></tr>)}</tbody></table>}
          </div>

          <div className="card">
            <h2>Model speed</h2>
            {bench.length === 0 ? <p className="muted">Run scripts/benchmark.py to compare PyTorch, ONNX and TensorRT.</p> :
              bench.map(b => (
                <div key={b.model} className="bar"><span>{b.model}</span>
                  <div><i style={{ width: Math.min(b.fps / Math.max(...bench.map(x => x.fps)) * 100, 100) + "%" }}/></div><b>{b.fps} FPS</b></div>))}
          </div>
        </aside>
      </main>
    </div>
  );
}

const Stat = ({ icon, label, value, warn }) => (
  <div className={"stat" + (warn ? " alert" : "")}><span>{icon}{label}</span><strong>{value}</strong></div>
);
