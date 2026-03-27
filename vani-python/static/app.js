// ─── Background Canvas ────────────────────────────────────
(function () {
  const canvas = document.getElementById('bg-canvas');
  const ctx = canvas.getContext('2d');
  let W, H, dots = [];

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  for (let i = 0; i < 80; i++) {
    dots.push({
      x: Math.random() * 2000, y: Math.random() * 1200,
      r: Math.random() * 1.2 + 0.3,
      vx: (Math.random() - 0.5) * 0.2, vy: (Math.random() - 0.5) * 0.2,
      a: Math.random()
    });
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    dots.forEach(d => {
      d.x += d.vx; d.y += d.vy;
      if (d.x < 0) d.x = W; if (d.x > W) d.x = 0;
      if (d.y < 0) d.y = H; if (d.y > H) d.y = 0;
      ctx.beginPath();
      ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0,255,180,${0.3 * d.a})`;
      ctx.fill();
    });
    // Grid lines
    ctx.strokeStyle = 'rgba(0,255,180,0.03)';
    ctx.lineWidth = 1;
    for (let x = 0; x < W; x += 80) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    for (let y = 0; y < H; y += 80) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }
    requestAnimationFrame(draw);
  }
  draw();
})();

// ─── DOM ──────────────────────────────────────────────────
const micBtn    = document.getElementById('micBtn');
const iconMic   = micBtn.querySelector('.icon-mic');
const iconStop  = micBtn.querySelector('.icon-stop');
const orbWrap   = document.getElementById('orbWrap');
const waveBars  = document.getElementById('waveBars');
const statusDot = document.getElementById('statusDot');
const statusMsg = document.getElementById('statusMsg');
const chatLog   = document.getElementById('chatLog');
const textInput = document.getElementById('textInput');
const sendBtn   = document.getElementById('sendBtn');
const clearBtn  = document.getElementById('clearBtn');

// ─── State ────────────────────────────────────────────────
let isListening = false;
let recognition = null;

// ─── Speech Recognition ───────────────────────────────────
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

function initRecognition() {
  if (!SpeechRecognition) return null;
  const r = new SpeechRecognition();
  r.lang = 'hi-IN';
  r.interimResults = false;
  r.maxAlternatives = 1;

  r.onstart = () => {
    setStatus('listening', '🎙️ Sun rahi hoon...');
    orbWrap.classList.add('active');
    waveBars.classList.add('visible');
  };

  r.onresult = (e) => {
    const text = e.results[0][0].transcript;
    stopListening();
    addBubble('user', text);
    askServer(text);
  };

  r.onerror = (e) => {
    stopListening();
    if (e.error === 'no-speech') setStatus('', 'Koi awaaz nahi. Phir try karein.');
    else if (e.error === 'not-allowed') setStatus('', 'Mic permission deny hai!');
    else setStatus('', 'Error: ' + e.error);
  };

  r.onend = () => { if (isListening) stopListening(); };
  return r;
}

function startListening() {
  if (!SpeechRecognition) {
    setStatus('', 'Browser voice support nahi karta. Chrome use karein!');
    return;
  }
  isListening = true;
  micBtn.classList.add('active');
  iconMic.style.display = 'none';
  iconStop.style.display = 'block';
  recognition = initRecognition();
  if (recognition) recognition.start();
}

function stopListening() {
  isListening = false;
  micBtn.classList.remove('active');
  iconMic.style.display = 'block';
  iconStop.style.display = 'none';
  orbWrap.classList.remove('active');
  waveBars.classList.remove('visible');
  if (recognition) { try { recognition.stop(); } catch (e) {} }
  setStatus('', 'Mic dabayein ya Space press karein');
}

// ─── Server API ───────────────────────────────────────────
async function askServer(text) {
  setStatus('thinking', '🤔 Soch rahi hoon...');
  const typingId = addTyping();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    removeTyping(typingId);

    if (data.error) {
      addBubble('vani', '⚠️ ' + data.error);
      setStatus('', 'Mic dabayein ya Space press karein');
      return;
    }

    const reply = data.reply;
    addBubble('vani', reply, true);
    await playTTS(reply);

  } catch (err) {
    removeTyping(typingId);
    addBubble('vani', '⚠️ Server se connect nahi ho pa raha. Flask server chala raha hai?');
    setStatus('', 'Server error');
  }
}

async function playTTS(text) {
  setStatus('speaking', '🔊 Bol rahi hoon...');
  try {
    const res = await fetch('/api/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    if (!res.ok) throw new Error('TTS failed');

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);

    // Add audio player to last VANI bubble
    const bubbles = chatLog.querySelectorAll('.bubble.vani');
    const last = bubbles[bubbles.length - 1];
    if (last) {
      const audioDiv = document.createElement('div');
      audioDiv.className = 'bubble-audio';
      const audioEl = document.createElement('audio');
      audioEl.controls = true;
      audioEl.src = url;
      audioDiv.appendChild(audioEl);
      last.appendChild(audioDiv);
    }

    audio.play();
    audio.onended = () => setStatus('', 'Mic dabayein ya Space press karein');

  } catch (err) {
    // Fallback to browser TTS
    if ('speechSynthesis' in window) {
      const utt = new SpeechSynthesisUtterance(text);
      utt.lang = 'hi-IN'; utt.rate = 0.95;
      utt.onend = () => setStatus('', 'Mic dabayein ya Space press karein');
      window.speechSynthesis.speak(utt);
    } else {
      setStatus('', 'Mic dabayein ya Space press karein');
    }
  }
}

// ─── Chat Log UI ──────────────────────────────────────────
let typingCount = 0;

function addBubble(who, text, isVani = false) {
  const welcome = chatLog.querySelector('.chat-welcome');
  if (welcome) welcome.remove();

  const div = document.createElement('div');
  div.className = `bubble ${who === 'user' ? 'user' : 'vani'}`;

  const label = document.createElement('div');
  label.className = 'bubble-label';
  label.textContent = who === 'user' ? 'AAP' : 'VANI';

  const bubble = document.createElement('div');
  bubble.className = 'bubble-text';
  bubble.textContent = text;

  div.appendChild(label);
  div.appendChild(bubble);
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
  return div;
}

function addTyping() {
  const id = 'typing-' + (++typingCount);
  const div = document.createElement('div');
  div.className = 'bubble vani';
  div.id = id;

  const label = document.createElement('div');
  label.className = 'bubble-label';
  label.textContent = 'VANI';

  const dots = document.createElement('div');
  dots.className = 'typing-dots';
  dots.innerHTML = '<span></span><span></span><span></span>';

  div.appendChild(label);
  div.appendChild(dots);
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
  return id;
}

function removeTyping(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

// ─── Status ───────────────────────────────────────────────
function setStatus(state, msg) {
  statusDot.className = 'status-dot ' + (state || '');
  statusMsg.textContent = msg;
}

// ─── Events ───────────────────────────────────────────────
micBtn.addEventListener('click', () => {
  if (isListening) stopListening();
  else startListening();
});

sendBtn.addEventListener('click', sendText);
textInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendText();
});

function sendText() {
  const t = textInput.value.trim();
  if (!t) return;
  textInput.value = '';
  addBubble('user', t);
  askServer(t);
}

clearBtn.addEventListener('click', () => {
  chatLog.innerHTML = '';
  const welcome = document.createElement('div');
  welcome.className = 'chat-welcome';
  welcome.innerHTML = '<div class="welcome-icon">🤖</div><p>Log clear kar diya! Dobara poochiye.</p>';
  chatLog.appendChild(welcome);
});

document.addEventListener('keydown', (e) => {
  if (e.code === 'Space' && document.activeElement === document.body) {
    e.preventDefault();
    if (isListening) stopListening();
    else startListening();
  }
});

// ─── Init ─────────────────────────────────────────────────
setStatus('', 'Mic dabayein ya Space press karein');
