const stateText = document.getElementById("stateText");
const timer = document.getElementById("timer");
const badge = document.getElementById("badge");
const statusDot = document.getElementById("statusDot");
const startButton = document.getElementById("startButton");
const stopButton = document.getElementById("stopButton");
const toast = document.getElementById("toast");

let isRecording = false;
let busy = false;
let toastTimer = null;

function showToast(message) {
  toast.textContent = message;
  toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.hidden = true;
  }, 1200);
}

function fmtTime(sec) {
  sec = Number(sec || 0);
  const h = String(Math.floor(sec / 3600)).padStart(2, "0");
  const m = String(Math.floor((sec % 3600) / 60)).padStart(2, "0");
  const s = String(sec % 60).padStart(2, "0");
  return `${h}:${m}:${s}`;
}

async function postJson(url) {
  const res = await fetch(url, { method: "POST" });
  if (!res.ok) throw new Error(`${res.status}`);
  return await res.json();
}

function updateMode(recording) {
  isRecording = recording;
  stateText.textContent = recording ? "RECORDING" : "READY";
  badge.textContent = recording ? "REC" : "IDLE";
  badge.classList.toggle("recording", recording);
  statusDot.classList.toggle("recording", recording);
  startButton.disabled = busy || recording;
  stopButton.disabled = busy || !recording;
}

async function refreshStatus() {
  try {
    const res = await fetch("/api/status", { cache: "no-store" });
    if (!res.ok) throw new Error(`${res.status}`);
    const s = await res.json();
    updateMode(Boolean(s.recording));
    timer.textContent = fmtTime(s.elapsed_seconds);
  } catch (e) {
    stateText.textContent = "OFFLINE";
  }
}

async function startRecording() {
  if (busy || isRecording) return;
  busy = true;
  updateMode(isRecording);
  try {
    const result = await postJson("/api/record/start");
    showToast(result.message || "Started.");
  } catch (e) {
    showToast("Start failed.");
  } finally {
    busy = false;
    await refreshStatus();
  }
}

async function stopRecording() {
  if (busy || !isRecording) return;
  busy = true;
  updateMode(isRecording);
  try {
    const result = await postJson("/api/record/stop");
    showToast(result.message || "Stopped.");
  } catch (e) {
    showToast("Stop failed.");
  } finally {
    busy = false;
    await refreshStatus();
  }
}

startButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

setInterval(refreshStatus, 1000);
refreshStatus();
