import shutil
import subprocess
from pathlib import Path

from flask import Flask, jsonify, send_file, send_from_directory, abort

from settings import APP_ROOT, RECORDINGS_DIR, ENABLE_GPIO
from recorder import Recorder
from gpio_worker import GPIOWorker

app = Flask(
    __name__,
    static_folder=str(APP_ROOT / "frontend"),
    static_url_path="/static",
)

recorder = Recorder()
gpio_worker = GPIOWorker(recorder)
gpio_worker.start()


@app.get("/")
def index():
    return send_from_directory(str(APP_ROOT / "frontend"), "index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True})


@app.post("/api/record/start")
def start_recording():
    return jsonify(recorder.start())


@app.post("/api/record/stop")
def stop_recording():
    return jsonify(recorder.stop())


@app.get("/api/status")
def status():
    disk = shutil.disk_usage(RECORDINGS_DIR)
    data = recorder.status()
    data.update({
        "disk_total": disk.total,
        "disk_used": disk.used,
        "disk_free": disk.free,
        "gpio_enabled": ENABLE_GPIO,
        "gpio_error": gpio_worker.error,
    })

    try:
        data["temperature"] = subprocess.check_output(
            ["vcgencmd", "measure_temp"], text=True
        ).strip().replace("temp=", "")
    except Exception:
        data["temperature"] = None

    return jsonify(data)


@app.get("/api/files")
def list_files():
    files = []
    for path in sorted(RECORDINGS_DIR.rglob("*.wav"), key=lambda p: p.stat().st_mtime, reverse=True):
        st = path.stat()
        rel = path.relative_to(RECORDINGS_DIR).as_posix()
        files.append({
            "name": path.name,
            "relative_path": rel,
            "size": st.st_size,
            "mtime": int(st.st_mtime),
            "download_url": f"/files/{rel}",
        })
    return jsonify(files)


@app.get("/files/<path:file_path>")
def download_file(file_path):
    root = RECORDINGS_DIR.resolve()
    path = (RECORDINGS_DIR / file_path).resolve()

    if not str(path).startswith(str(root)):
        abort(403)

    if not path.exists() or not path.is_file():
        abort(404)

    return send_file(path, mimetype="audio/wav", as_attachment=False, download_name=path.name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
