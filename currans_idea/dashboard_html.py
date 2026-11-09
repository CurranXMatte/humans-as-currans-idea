DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="it" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Humans as Curran's Idea — Live Telegram Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            tg: {
              bg: '#0e1621',
              card: '#17212b',
              header: '#242f3d',
              accent: '#2b5278',
              blue: '#5288c1',
              light: '#f5f5f5',
              muted: '#708499',
              bubble: '#182533',
              bubbleReply: '#203040'
            }
          }
        }
      }
    }
  </script>
  <style>
    @keyframes slideIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .msg-animate {
      animation: slideIn 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0e1621; }
    ::-webkit-scrollbar-thumb { background: #242f3d; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #2b5278; }
  </style>
</head>
<body class="bg-tg-bg text-tg-light min-h-screen flex flex-col font-sans antialiased">

  <!-- Top Header -->
  <header class="bg-tg-header border-b border-gray-800 shadow-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg">
          <i class="fa-solid fa-robot text-white text-lg"></i>
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h1 class="text-lg font-bold text-white tracking-wide">Humans as Curran's Idea</h1>
            <span class="bg-blue-900/60 text-blue-300 text-xs px-2 py-0.5 rounded-full font-semibold border border-blue-700/50">v2.0 Live</span>
          </div>
          <p class="text-xs text-tg-muted">Simulatore di Folla Telegram • 100 Messaggi in Tempo Reale • 5 Archetipi Umani</p>
        </div>
      </div>

      <div class="flex items-center space-x-3">
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-950/80 text-emerald-400 border border-emerald-800/60 shadow-sm">
          <span class="w-2 h-2 mr-1.5 bg-emerald-400 rounded-full animate-pulse"></span>
          Vercel API Live
        </span>
        <a href="/docs" target="_blank" class="text-xs bg-tg-card hover:bg-tg-accent text-gray-200 px-3 py-1.5 rounded-lg border border-gray-700 transition flex items-center space-x-1.5">
          <i class="fa-solid fa-book"></i>
          <span>Swagger Docs</span>
        </a>
        <a href="https://github.com/CurranXMatte/humans-as-currans-idea" target="_blank" class="text-xs bg-tg-card hover:bg-tg-accent text-gray-200 px-3 py-1.5 rounded-lg border border-gray-700 transition flex items-center space-x-1.5">
          <i class="fa-brands fa-github"></i>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full grid grid-cols-1 lg:grid-cols-12 gap-6">

    <!-- Left Column: Controls & Event Input -->
    <div class="lg:col-span-5 flex flex-col space-y-4">
      
      <!-- Event Input Card -->
      <div class="bg-tg-card rounded-xl p-5 border border-gray-800 shadow-xl">
        <div class="flex items-center justify-between mb-3">
          <label class="text-sm font-semibold text-gray-200 flex items-center space-x-2">
            <i class="fa-solid fa-bullhorn text-tg-blue"></i>
            <span>Post o Evento Canale</span>
          </label>
          <span class="text-xs text-tg-muted">Parser Intelligente</span>
        </div>

        <textarea id="eventInput" rows="4" class="w-full bg-tg-bg border border-gray-700 rounded-lg p-3 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-tg-blue focus:ring-1 focus:ring-tg-blue transition resize-none font-mono" placeholder="Incolla il post del canale Telegram..."></textarea>

        <!-- Presets Buttons -->
        <div class="mt-3">
          <span class="text-xs text-tg-muted block mb-1.5 font-medium">Eventi di esempio rapidi:</span>
          <div class="grid grid-cols-2 gap-1.5">
            <button onclick="setPreset('goal_lautaro')" class="text-left text-xs bg-tg-bg hover:bg-tg-accent/40 border border-gray-700/80 p-2 rounded text-gray-300 transition truncate">
              ⚽ <b>Gol Lautaro 34'</b> (Inter-Milan)
            </button>
            <button onclick="setPreset('goal_vlahovic')" class="text-left text-xs bg-tg-bg hover:bg-tg-accent/40 border border-gray-700/80 p-2 rounded text-gray-300 transition truncate">
              ⚽ <b>Gol Vlahovic 89'</b> (Juve-Napoli)
            </button>
            <button onclick="setPreset('injury_bremer')" class="text-left text-xs bg-tg-bg hover:bg-tg-accent/40 border border-gray-700/80 p-2 rounded text-gray-300 transition truncate">
              🚑 <b>Infortunio Bremer</b> (Comunicato)
            </button>
            <button onclick="setPreset('red_theo')" class="text-left text-xs bg-tg-bg hover:bg-tg-accent/40 border border-gray-700/80 p-2 rounded text-gray-300 transition truncate">
              🔴 <b>Rosso Diretto</b> (Espulsione)
            </button>
          </div>
        </div>
      </div>

      <!-- Simulation Options Card -->
      <div class="bg-tg-card rounded-xl p-5 border border-gray-800 shadow-xl space-y-4">
        <h3 class="text-sm font-semibold text-gray-200 flex items-center space-x-2">
          <i class="fa-solid fa-sliders text-tg-blue"></i>
          <span>Parametri Simulazione</span>
        </h3>

        <!-- Count Selector -->
        <div>
          <div class="flex justify-between items-center text-xs text-gray-300 mb-1.5">
            <span>Numero di Messaggi:</span>
            <span id="countDisplay" class="font-bold text-tg-blue text-sm">100 messaggi</span>
          </div>
          <div class="grid grid-cols-4 gap-2">
            <button onclick="setCount(10)" class="count-btn py-1.5 text-xs rounded border border-gray-700 bg-tg-bg hover:bg-tg-accent text-gray-300">10</button>
            <button onclick="setCount(25)" class="count-btn py-1.5 text-xs rounded border border-gray-700 bg-tg-bg hover:bg-tg-accent text-gray-300">25</button>
            <button onclick="setCount(50)" class="count-btn py-1.5 text-xs rounded border border-gray-700 bg-tg-bg hover:bg-tg-accent text-gray-300">50</button>
            <button onclick="setCount(100)" class="count-btn active py-1.5 text-xs rounded border border-blue-500 bg-blue-600/30 text-white font-bold">100</button>
          </div>
        </div>

        <!-- Speed Selector -->
        <div>
          <label class="text-xs text-gray-300 block mb-1.5">Velocità del Flusso in Tempo Reale:</label>
          <select id="speedSelect" class="w-full bg-tg-bg border border-gray-700 rounded-lg p-2 text-xs text-gray-200 focus:outline-none focus:border-tg-blue">
            <option value="realtime">⏱️ Tempo Reale Naturale (1x - jitter asincrono)</option>
            <option value="fast" selected>⚡ Veloce (3x - consigliato per demo)</option>
            <option value="turbo">🚀 Turbo (10x - scarica rapida)</option>
            <option value="instant">💥 Istantaneo (tutti insieme)</option>
          </select>
        </div>

        <!-- Thread Toggle -->
        <div class="flex items-center justify-between pt-1">
          <span class="text-xs text-gray-300">Discussioni fra bot (Citazioni & Risposte):</span>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" id="replyToggle" class="sr-only peer" checked>
            <div class="w-9 h-5 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-600"></div>
          </label>
        </div>

        <!-- Action Buttons -->
        <div class="pt-2 flex space-x-2">
          <button id="startBtn" onclick="startSimulation()" class="flex-1 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-bold py-2.5 px-4 rounded-lg shadow-lg shadow-blue-900/30 transition flex items-center justify-center space-x-2">
            <i class="fa-solid fa-play"></i>
            <span>Avvia Simulazione Live</span>
          </button>
          <button id="pauseBtn" onclick="togglePause()" class="hidden bg-yellow-600 hover:bg-yellow-500 text-white font-bold py-2.5 px-3 rounded-lg transition" title="Pausa / Riprendi">
            <i class="fa-solid fa-pause"></i>
          </button>
          <button onclick="clearChat()" class="bg-gray-800 hover:bg-gray-700 text-gray-300 font-semibold py-2.5 px-3 rounded-lg border border-gray-700 transition" title="Pulisci">
            <i class="fa-solid fa-trash-can"></i>
          </button>
        </div>
      </div>

      <!-- Archetypes Legend -->
      <div class="bg-tg-card rounded-xl p-4 border border-gray-800 shadow-xl text-xs space-y-2">
        <span class="text-tg-muted font-bold block mb-1">5 ARCHETIPI COMPORTAMENTALI (45K MESSAGGI REALI):</span>
        <div class="flex flex-wrap gap-1.5">
          <span class="px-2 py-0.5 rounded-full bg-red-950/80 text-red-300 border border-red-800/50">🔥 Emotivo (Caps Lock / Hype)</span>
          <span class="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">🌧️ Cinico (Tanto / Disfattista)</span>
          <span class="px-2 py-0.5 rounded-full bg-purple-950/80 text-purple-300 border border-purple-800/50">🤡 Troll (Sfottò / ahahah)</span>
          <span class="px-2 py-0.5 rounded-full bg-amber-950/80 text-amber-300 border border-amber-800/50">⚽ Fanta (Bonus / Schedine)</span>
          <span class="px-2 py-0.5 rounded-full bg-blue-950/80 text-blue-300 border border-blue-800/50">⚡ Telegrafico (1-2 parole)</span>
        </div>
      </div>

    </div>

    <!-- Right Column: Live Telegram Chat Feed -->
    <div class="lg:col-span-7 flex flex-col h-[750px] bg-tg-card rounded-xl border border-gray-800 shadow-2xl overflow-hidden">
      
      <!-- Chat Header -->
      <div class="bg-tg-header px-4 py-3 border-b border-gray-800 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-700 flex items-center justify-center font-bold text-white text-sm shadow">
            ⚽
          </div>
          <div>
            <h2 class="text-sm font-bold text-white flex items-center space-x-1.5">
              <span>Gruppo Discussione Canale</span>
              <i class="fa-solid fa-circle-check text-blue-400 text-xs"></i>
            </h2>
            <p id="chatSubtitle" class="text-xs text-tg-muted">In attesa dell'evento...</p>
          </div>
        </div>

        <!-- Live Progress Counter -->
        <div class="flex items-center space-x-3">
          <div class="text-right">
            <span id="counterBadge" class="text-xs font-bold text-gray-300">0 / 0</span>
            <div class="w-24 bg-gray-800 h-1.5 rounded-full mt-1 overflow-hidden">
              <div id="progressBar" class="bg-blue-500 h-full w-0 transition-all duration-300"></div>
            </div>
          </div>
          <button id="autoscrollBtn" onclick="toggleAutoScroll()" class="text-xs bg-tg-bg border border-gray-700 text-blue-400 p-1.5 rounded-lg" title="Auto-scroll">
            <i class="fa-solid fa-angles-down"></i>
          </button>
        </div>
      </div>

      <!-- Pinned Channel Post -->
      <div id="pinnedPost" class="bg-tg-bg/70 px-4 py-2.5 border-b border-gray-800 text-xs flex items-start space-x-3 transition">
        <div class="text-blue-400 pt-0.5"><i class="fa-solid fa-thumbtack"></i></div>
        <div class="flex-1">
          <span class="font-bold text-blue-400 block">Post Canale Ufficiale</span>
          <p id="pinnedText" class="text-gray-300 font-mono text-[11px] whitespace-pre-line mt-0.5">Nessun post caricato.</p>
        </div>
      </div>

      <!-- Chat Messages Scroll Container -->
      <div id="chatMessages" class="flex-1 p-4 overflow-y-auto space-y-3 bg-[#0e1621]">
        
        <!-- Welcome Placeholder -->
        <div id="welcomePlaceholder" class="h-full flex flex-col items-center justify-center text-center p-8 text-tg-muted">
          <div class="w-16 h-16 rounded-full bg-tg-card border border-gray-800 flex items-center justify-center text-2xl mb-3 text-tg-blue">
            <i class="fa-regular fa-comments"></i>
          </div>
          <h3 class="text-sm font-semibold text-gray-300">Simulatore di Commenti Pronto</h3>
          <p class="text-xs max-w-sm mt-1">Scegli un evento sulla sinistra e premi <b>"Avvia Simulazione Live"</b> per vedere fino a 100 utenti reali interagire in tempo reale sotto al post!</p>
        </div>

      </div>

      <!-- Live Typing Footer -->
      <div id="typingBar" class="hidden bg-tg-header px-4 py-2 border-t border-gray-800 text-xs text-tg-muted flex items-center space-x-2">
        <div class="flex space-x-1">
          <span class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce"></span>
          <span class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
          <span class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
        </div>
        <span id="typingUser">Gli utenti stanno commentando...</span>
      </div>

    </div>

  </main>

  <script>
    const PRESETS = {
      goal_lautaro: "GOAL! ⚽️\\n#SerieA 🏆\\nInter 🆚 Milan\\n1-0\\n⚽️ Lautaro Martinez\\n👟 Barella N.\\n⏱️ 34’",
      goal_vlahovic: "GOAL! ⚽️\\n#SerieA 🏆\\nJuventus 🆚 Napoli\\n2-1\\n⚽️ Vlahovic D.\\n⏱️ 89’",
      injury_bremer: "🚑 COMUNICATO UFFICIALE\\n\\nTrauma distorsivo al ginocchio sinistro per Bremer.\\nStagione a forte rischio.",
      red_theo: "CARTELLINO ROSSO! 🟥\\n\\nEspulsione diretta per Theo Hernandez al 68' dopo revisione VAR."
    };

    let selectedCount = 100;
    let simulationQueue = [];
    let isRunning = false;
    let isPaused = false;
    let timerId = null;
    let autoScroll = true;
    let currentIdx = 0;

    const AVATAR_COLORS = [
      '#e17076', '#7bc862', '#65aadd', '#a695e7', '#ee7aae', '#6ec9cb', '#faa774'
    ];

    function getAvatarColor(name) {
      let hash = 0;
      for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
      return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length];
    }

    function setPreset(key) {
      document.getElementById('eventInput').value = PRESETS[key] || '';
    }

    function setCount(num) {
      selectedCount = num;
      document.getElementById('countDisplay').innerText = num + ' messaggi';
      document.querySelectorAll('.count-btn').forEach(btn => {
        btn.classList.remove('active', 'border-blue-500', 'bg-blue-600/30', 'text-white', 'font-bold');
        btn.classList.add('border-gray-700', 'bg-tg-bg', 'text-gray-300');
      });
      event.target.classList.add('active', 'border-blue-500', 'bg-blue-600/30', 'text-white', 'font-bold');
    }

    function toggleAutoScroll() {
      autoScroll = !autoScroll;
      const btn = document.getElementById('autoscrollBtn');
      btn.className = autoScroll ? 'text-xs bg-tg-bg border border-gray-700 text-blue-400 p-1.5 rounded-lg' : 'text-xs bg-tg-bg border border-gray-700 text-gray-500 p-1.5 rounded-lg';
    }

    function clearChat() {
      stopSimulation();
      document.getElementById('chatMessages').innerHTML = `
        <div id="welcomePlaceholder" class="h-full flex flex-col items-center justify-center text-center p-8 text-tg-muted">
          <div class="w-16 h-16 rounded-full bg-tg-card border border-gray-800 flex items-center justify-center text-2xl mb-3 text-tg-blue">
            <i class="fa-regular fa-comments"></i>
          </div>
          <h3 class="text-sm font-semibold text-gray-300">Chat ripulita</h3>
          <p class="text-xs max-w-sm mt-1">Avvia una nuova simulazione quando vuoi!</p>
        </div>
      `;
      document.getElementById('pinnedText').innerText = 'Nessun post caricato.';
      document.getElementById('counterBadge').innerText = '0 / 0';
      document.getElementById('progressBar').style.width = '0%';
      document.getElementById('chatSubtitle').innerText = 'In attesa dell\\'evento...';
    }

    function getPersonaBadge(pid, pname) {
      switch(pid) {
        case 1: return '<span class="text-[10px] px-1.5 py-0.2 rounded bg-red-950/80 text-red-300 border border-red-800/40 font-semibold">🔥 Emotivo</span>';
        case 2: return '<span class="text-[10px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 border border-slate-700 font-semibold">🌧️ Cinico</span>';
        case 3: return '<span class="text-[10px] px-1.5 py-0.2 rounded bg-purple-950/80 text-purple-300 border border-purple-800/40 font-semibold">🤡 Troll</span>';
        case 4: return '<span class="text-[10px] px-1.5 py-0.2 rounded bg-amber-950/80 text-amber-300 border border-amber-800/40 font-semibold">⚽ Fanta</span>';
        case 5: return '<span class="text-[10px] px-1.5 py-0.2 rounded bg-blue-950/80 text-blue-300 border border-blue-800/40 font-semibold">⚡ Telegrafico</span>';
        default: return '';
      }
    }

    async function startSimulation() {
      const text = document.getElementById('eventInput').value.trim();
      if (!text) {
        alert("Inserisci un post o seleziona un esempio rapido.");
        return;
      }

      stopSimulation();

      // Setup UI
      const placeholder = document.getElementById('welcomePlaceholder');
      if (placeholder) placeholder.remove();

      document.getElementById('pinnedText').innerText = text;
      document.getElementById('chatSubtitle').innerText = 'Simulazione attiva • Flusso in corso...';
      document.getElementById('typingBar').classList.remove('hidden');
      document.getElementById('pauseBtn').classList.remove('hidden');

      // Chiamata all'endpoint API /api/v1/crowd
      try {
        const includeReplies = document.getElementById('replyToggle').checked;
        const res = await fetch('/api/v1/crowd', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: text,
            count: selectedCount,
            include_replies: includeReplies
          })
        });

        if (!res.ok) throw new Error("Errore API: " + res.status);
        const data = await res.json();
        
        simulationQueue = data.feed || [];
        currentIdx = 0;
        isRunning = true;
        isPaused = false;

        document.getElementById('counterBadge').innerText = `0 / ${simulationQueue.length}`;
        processNextMessage();
      } catch (err) {
        alert("Errore nel recupero della folla di commenti: " + err.message);
        stopSimulation();
      }
    }

    function processNextMessage() {
      if (!isRunning || isPaused) return;

      if (currentIdx >= simulationQueue.length) {
        // Completato!
        document.getElementById('chatSubtitle').innerText = `Simulazione completata (${simulationQueue.length} commenti).`;
        document.getElementById('typingBar').classList.add('hidden');
        document.getElementById('pauseBtn').classList.add('hidden');
        isRunning = false;
        return;
      }

      const msg = simulationQueue[currentIdx];
      renderMessage(msg);
      currentIdx++;

      // Aggiorna contatore
      document.getElementById('counterBadge').innerText = `${currentIdx} / ${simulationQueue.length}`;
      const pct = Math.round((currentIdx / simulationQueue.length) * 100);
      document.getElementById('progressBar').style.width = pct + '%';

      // Calcola ritardo in base alla velocità
      const speed = document.getElementById('speedSelect').value;
      let delayMs = 300;

      if (speed === 'instant') {
        delayMs = 0;
      } else if (speed === 'turbo') {
        delayMs = 40;
      } else if (speed === 'fast') {
        delayMs = 150;
      } else { // realtime (1x)
        delayMs = Math.floor(Math.random() * 600) + 400;
      }

      if (delayMs === 0) {
        // Esegui in batch rapido
        while (currentIdx < simulationQueue.length) {
          renderMessage(simulationQueue[currentIdx]);
          currentIdx++;
        }
        document.getElementById('counterBadge').innerText = `${currentIdx} / ${simulationQueue.length}`;
        document.getElementById('progressBar').style.width = '100%';
        document.getElementById('chatSubtitle').innerText = `Simulazione completata (${simulationQueue.length} commenti).`;
        document.getElementById('typingBar').classList.add('hidden');
        document.getElementById('pauseBtn').classList.add('hidden');
        isRunning = false;
      } else {
        timerId = setTimeout(processNextMessage, delayMs);
      }
    }

    function renderMessage(msg) {
      const container = document.getElementById('chatMessages');
      const msgDiv = document.createElement('div');
      msgDiv.className = 'flex items-start space-x-2.5 msg-animate';

      const avatarColor = getAvatarColor(msg.user);
      const initial = msg.user.charAt(0).toUpperCase();

      let replyHtml = '';
      if (msg.in_reply_to_id) {
        replyHtml = `
          <div class="mb-1.5 px-2.5 py-1 bg-tg-bubbleReply/80 rounded border-l-2 border-blue-400 text-[11px]">
            <span class="font-bold text-blue-300 block">${msg.in_reply_to_user || 'Utente'}</span>
            <span class="text-gray-400 truncate block">${msg.in_reply_to_snippet || '...'}</span>
          </div>
        `;
      }

      msgDiv.innerHTML = `
        <div class="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center font-bold text-white text-xs shadow" style="background-color: ${avatarColor}">
          ${initial}
        </div>
        <div class="bg-tg-bubble rounded-2xl rounded-tl-sm px-3.5 py-2 max-w-[85%] border border-gray-800/80 shadow-md">
          <div class="flex items-center space-x-2 mb-0.5">
            <span class="font-bold text-xs" style="color: ${avatarColor}">${msg.user}</span>
            ${getPersonaBadge(msg.persona_id, msg.persona_name)}
          </div>
          ${replyHtml}
          <div class="text-xs text-gray-100 font-normal leading-relaxed break-words">
            ${msg.message}
          </div>
          <div class="text-[10px] text-tg-muted text-right mt-1 flex items-center justify-end space-x-1">
            <span>+${msg.delay_seconds}s</span>
            <i class="fa-solid fa-check text-[9px] text-blue-400"></i>
          </div>
        </div>
      `;

      container.appendChild(msgDiv);

      if (autoScroll) {
        container.scrollTop = container.scrollHeight;
      }
    }

    function togglePause() {
      if (!isRunning) return;
      isPaused = !isPaused;
      const pauseBtn = document.getElementById('pauseBtn');
      if (isPaused) {
        clearTimeout(timerId);
        pauseBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
        pauseBtn.classList.replace('bg-yellow-600', 'bg-emerald-600');
        document.getElementById('chatSubtitle').innerText = 'Simulazione in pausa.';
      } else {
        pauseBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
        pauseBtn.classList.replace('bg-emerald-600', 'bg-yellow-600');
        document.getElementById('chatSubtitle').innerText = 'Simulazione attiva • Flusso in corso...';
        processNextMessage();
      }
    }

    function stopSimulation() {
      isRunning = false;
      isPaused = false;
      if (timerId) clearTimeout(timerId);
      document.getElementById('typingBar').classList.add('hidden');
      document.getElementById('pauseBtn').classList.add('hidden');
    }

    // Inizializza con preset di default
    setPreset('goal_lautaro');
  </script>
</body>
</html>
"""
