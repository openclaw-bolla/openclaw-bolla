/* Englisch-Trainer (Bolla) – gemeinsam für MP (Familie → Englisch) und mmp (Einstiegsseite).
   Einbinden: <script src="/englisch.js"></script>  →  EnglischTrainer.mount(document.getElementById('...'))
   Backend: /api/englisch/*  ·  TTS: /api/bolla/tts  ·  Aussprache: Azure Speech SDK (Key via /api/speech/config)  */
(function () {
  'use strict';
  if (window.EnglischTrainer) return;

  var CSS = `
  .en{font-size:16px;line-height:1.5;max-width:760px;margin:0 auto;padding:4px 2px 80px;color:inherit}
  .en *{box-sizing:border-box}
  .en h2{font-size:20px;margin:0 0 6px}
  .en h3{font-size:17px;margin:14px 0 6px}
  .en .card{background:rgba(127,127,127,.13);border:1px solid rgba(127,127,127,.28);border-radius:14px;padding:14px;margin:10px 0}
  .en .muted{opacity:.75;font-size:14px}
  .en .row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
  .en .grow{flex:1}
  .en .btn{min-height:44px;padding:9px 16px;border-radius:11px;border:0;background:#2563eb;color:#fff;font-size:16px;font-weight:600;cursor:pointer;font-family:inherit}
  .en .btn.sec{background:rgba(127,127,127,.25);color:inherit}
  .en .btn.ok{background:#16a34a}
  .en .btn.bad{background:#dc2626}
  .en .btn[disabled]{opacity:.45;cursor:default}
  .en .opt{display:block;width:100%;text-align:left;min-height:46px;margin:6px 0;padding:10px 14px;border-radius:11px;border:1.5px solid rgba(127,127,127,.4);background:rgba(127,127,127,.08);color:inherit;font-size:16px;cursor:pointer;font-family:inherit}
  .en .opt.right{border-color:#16a34a;background:rgba(22,163,74,.22)}
  .en .opt.wrong{border-color:#dc2626;background:rgba(220,38,38,.2)}
  .en .bar{height:12px;border-radius:7px;background:rgba(127,127,127,.25);overflow:hidden}
  .en .bar>i{display:block;height:100%;background:linear-gradient(90deg,#2563eb,#16a34a);border-radius:7px;transition:width .4s}
  .en .task{display:flex;gap:12px;align-items:center;cursor:pointer;min-height:56px}
  .en .task .ic{font-size:26px;width:36px;text-align:center}
  .en .task .sc{font-weight:700;white-space:nowrap}
  .en .task.done{opacity:.8}
  .en .chip{display:inline-block;padding:3px 10px;margin:3px 4px 3px 0;border-radius:999px;background:rgba(37,99,235,.2);font-size:14px}
  .en .part{display:inline-block;padding:6px 10px;margin:3px;border-radius:9px;border:1.5px solid rgba(127,127,127,.4);background:rgba(127,127,127,.08);cursor:pointer;font-size:17px}
  .en .part.right{border-color:#16a34a;background:rgba(22,163,74,.25)}
  .en .part.wrong{border-color:#dc2626;background:rgba(220,38,38,.22)}
  .en input.txt,.en textarea.txt{width:100%;padding:11px;border-radius:10px;border:1.5px solid rgba(127,127,127,.5);background:rgba(127,127,127,.08);color:inherit;font-size:17px;font-family:inherit}
  .en textarea.txt{min-height:120px;resize:vertical}
  .en .big{font-size:20px;line-height:1.6}
  .en .expl{margin-top:8px;padding:9px 12px;border-left:4px solid #2563eb;background:rgba(37,99,235,.12);border-radius:0 9px 9px 0;font-size:15px}
  .en .w-g{color:#16a34a;font-weight:600}.en .w-o{color:#d97706;font-weight:600}.en .w-r{color:#dc2626;font-weight:700}
  .en .w{cursor:pointer;margin-right:4px}
  .en .score{display:inline-block;min-width:92px;text-align:center;margin:4px;padding:8px 6px;border-radius:12px;background:rgba(127,127,127,.18)}
  .en .score b{display:block;font-size:22px}
  .en img.pic{width:100%;border-radius:12px;display:block;margin:8px 0}
  .en .bars{display:flex;gap:6px;align-items:flex-end;height:90px;margin:10px 0 2px}
  .en .bars div{flex:1;text-align:center;font-size:12px}
  .en .bars i{display:block;border-radius:5px 5px 0 0;background:#2563eb;min-height:3px}
  .en .bars i.t{background:#16a34a}
  .en .kbar{display:flex;align-items:center;gap:8px;margin:5px 0;font-size:14px}.en .kbar .bar{flex:1;height:9px}.en .kbar span:first-child{width:130px}
  .en .top{display:flex;align-items:center;gap:10px;margin-bottom:6px}
  .en .pill{padding:4px 12px;border-radius:999px;background:rgba(127,127,127,.22);font-weight:600;font-size:15px}
  .en .blink{animation:enb 1s infinite}@keyframes enb{50%{opacity:.35}}
  `;

  var ICON = { karten: '🃏', mc: '🧩', input: '✍️', fehler: '🔍', listen: '🎧', read: '🗣️', speak: '🎤' };
  var SELFICON = { bild: '🖼️', write: '✒️', translate: '🔁', rewrite: '🔀' };
  var VOICES = { 'en-US': ['en-US-AriaNeural', 'en-US-GuyNeural', 'en-US-JennyNeural'], 'en-GB': ['en-GB-SoniaNeural', 'en-GB-RyanNeural', 'en-GB-SoniaNeural'] };

  function h(tag, attrs) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === 'class') e.className = String(attrs[k]).split(/\s+/).filter(Boolean).map(function (c) { return c === 'enx' ? c : 'en-' + c; }).join(' ');
      else if (k === 'text') e.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on') e.addEventListener(k.slice(2), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    }
    for (var i = 2; i < arguments.length; i++) {
      var c = arguments[i];
      if (c == null || c === false) continue;
      e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    }
    return e;
  }
  function api(path, body) {
    var o = body ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) } : {};
    return fetch(path, o).then(function (r) { return r.json(); });
  }
  function norm(s) {
    return String(s || '').toLowerCase().replace(/[’‘`´]/g, "'").replace(/[^a-z0-9' \-äöüß]/g, ' ').replace(/\s+/g, ' ').trim();
  }
  function fmt(sec) { sec = Math.max(0, Math.round(sec)); return Math.floor(sec / 60) + ':' + ('0' + (sec % 60)).slice(-2); }
  function pct(x) { return Math.round(100 * x); }

  function mount(root) {
    if (!document.getElementById('en-css')) { var st = h('style', { id: 'en-css' }); st.textContent = CSS.replace(/\.([a-z][\w-]*)/g, '.en-$1').replace(/\.en-en\b/g, '.enx'); document.head.appendChild(st); }
    var el = h('div', { class: 'enx' });
    root.textContent = ''; root.appendChild(el);

    var S = { data: null, stat: null, today: { ergebnisse: {}, sek: 0 }, accent: localStorage.getItem('en_accent') || 'en-US', tick: null, taskStart: 0, audio: null, cache: {}, speechCfg: null };

    function resultsOf() { return (S.today && S.today.ergebnisse) || {}; }
    function totalSek() { return (S.today.sek || 0) + (S.inTask ? Math.min(300, (Date.now() - S.taskStart) / 1000) : 0); }
    function stopAudio() { if (S.audio) { try { S.audio.pause(); } catch (e) {} S.audio = null; } }

    /* ---------------- Laden ---------------- */
    function load() {
      el.textContent = ''; el.appendChild(h('div', { class: 'card', text: 'Lade dein Tagesset …' }));
      Promise.all([api('/api/englisch/heute'), api('/api/englisch/fortschritt')]).then(function (r) {
        var d = r[0], f = r[1];
        if (d.fehler) { el.textContent = ''; el.appendChild(h('div', { class: 'card' }, h('h2', { text: '🇬🇧 Englisch' }), h('p', { text: d.fehler }), h('button', { class: 'btn', text: '↻ Neu laden', onclick: load }))); return; }
        S.data = d; S.stat = f.stat; S.today = d.heute || {}; S.today.ergebnisse = S.today.ergebnisse || {}; S.today.sek = S.today.sek || 0;
        home();
      }).catch(function (e) { el.textContent = 'Fehler beim Laden: ' + e; });
    }

    /* ---------------- Übersicht ---------------- */
    function icon(a) { return a.typ === 'selfcheck' ? (SELFICON[a.slot] || '📝') : (ICON[a.typ] || '•'); }
    function home() {
      stopAudio(); S.inTask = false; clearInterval(S.tick);
      var set = S.data.set, A = set.aufgaben, er = resultsOf();
      var done = A.filter(function (a) { return er[a.id]; }).length;
      var ziel = (S.data.ziel_min || 12) * 60;
      el.textContent = '';
      var head = h('div', { class: 'card' },
        h('div', { class: 'row' }, h('h2', { class: 'grow', text: '🇬🇧 Englisch heute' }),
          h('span', { class: 'pill', text: '🔥 ' + (S.stat.streak || 0) + (S.stat.streak === 1 ? ' Tag' : ' Tage') })),
        set.gruss ? h('p', { class: 'muted', text: set.gruss + (set.gruss.indexOf('🐾') < 0 ? ' 🐾' : '') }) : null,
        S.data.hinweis ? h('p', { class: 'expl', text: S.data.hinweis }) : null,
        h('div', { class: 'muted', text: 'Thema: ' + (set.thema || '–') }),
        h('div', { class: 'row', style: 'margin-top:10px' }, h('span', { text: 'Aufgaben ' + done + '/' + A.length }), h('span', { class: 'grow' }), h('span', { id: 'en-time', text: '⏱ ' + fmt(S.today.sek || 0) + ' / ' + (S.data.ziel_min || 12) + ' min' })),
        h('div', { class: 'bar' }, h('i', { style: 'width:' + Math.min(100, Math.round(100 * done / A.length)) + '%' })),
        h('div', { class: 'bar', style: 'margin-top:5px;height:7px' }, h('i', { style: 'width:' + Math.min(100, Math.round(100 * (S.today.sek || 0) / ziel)) + '%' })));
      el.appendChild(head);
      var next = A.find(function (a) { return !er[a.id]; });
      if (done === A.length) {
        var sc = A.map(function (a) { return er[a.id].score; });
        el.appendChild(h('div', { class: 'card' }, h('h2', { text: '🎉 Tag geschafft!' }),
          h('p', { text: 'Durchschnitt heute: ' + pct(sc.reduce(function (x, y) { return x + y; }, 0) / sc.length) + ' % · Serie: ' + S.stat.streak + ' Tage. Morgen gibt es neue Aufgaben – bis dahin darfst du gern noch etwas wiederholen.' })));
      } else if (next) {
        el.appendChild(h('button', { class: 'btn', style: 'width:100%;margin:4px 0', text: (done ? '▶ Weiter: ' : '▶ Start: ') + next.titel, onclick: function () { openTask(A.indexOf(next)); } }));
      }
      A.forEach(function (a, i) {
        var r = er[a.id];
        el.appendChild(h('div', { class: 'card task' + (r ? ' done' : ''), onclick: function () { openTask(i); } },
          h('div', { class: 'ic', text: icon(a) }),
          h('div', { class: 'grow' }, h('b', { text: a.titel }), h('div', { class: 'muted', text: a.kat + ' · ca. ' + a.min + ' min' })),
          h('div', { class: 'sc', text: r ? ('✓ ' + pct(r.score) + ' %') : '›' })));
      });
      // Akzent
      el.appendChild(h('div', { class: 'card row' }, h('span', { text: 'Akzent (Aussprache & Hörtexte):' }),
        h('button', { class: 'btn ' + (S.accent === 'en-US' ? '' : 'sec'), text: '🇺🇸 US', onclick: function () { setAccent('en-US'); } }),
        h('button', { class: 'btn ' + (S.accent === 'en-GB' ? '' : 'sec'), text: '🇬🇧 UK', onclick: function () { setAccent('en-GB'); } })));
      // Meine Wörter
      var wbox = h('div', { class: 'card' }, h('h2', { text: '📌 Meine Wörter' }));
      var wl = h('div'); wbox.appendChild(wl);
      var wen = h('input', { class: 'txt', type: 'text', placeholder: 'Englisches Wort / Ausdruck', autocapitalize: 'off' });
      var wde = h('input', { class: 'txt', type: 'text', placeholder: 'Deutsch (optional)', style: 'margin-top:6px' });
      var wadd = h('button', { class: 'btn', style: 'margin-top:8px', text: '＋ Merken', onclick: function () {
        if (!wen.value.trim()) return;
        api('/api/englisch/wort', { en: wen.value, de: wde.value }).then(function () { wen.value = ''; wde.value = ''; ladeW(); });
      } });
      function ladeW() {
        api('/api/englisch/woerter').then(function (r) {
          wl.textContent = '';
          wl.appendChild(h('p', { class: 'muted', text: r.offen + ' offen · ' + r.gelernt + ' gelernt – offene Wörter kommen zufällig als Karteikarten, bis du sie 3× in Folge wusstest.' }));
          r.woerter.filter(function (x) { return x.streak < 3; }).slice(0, 40).forEach(function (x) {
            wl.appendChild(h('div', { class: 'row', style: 'margin:3px 0' }, h('span', { class: 'grow', text: x.en + (x.de ? ' – ' + x.de : '') }), h('span', { class: 'muted', text: x.streak + '/3' }),
              h('button', { class: 'btn sec', text: '✕', onclick: function () { api('/api/englisch/wort-loeschen', { id: x.id }).then(ladeW); } })));
          });
        });
      }
      wbox.appendChild(wen); wbox.appendChild(wde); wbox.appendChild(wadd); el.appendChild(wbox); ladeW();
      statistik();
    }
    function setAccent(a) { S.accent = a; localStorage.setItem('en_accent', a); S.cache = {}; home(); }

    function statistik() {
      var st = S.stat, box = h('div', { class: 'card' }, h('h2', { text: '📊 Statistik' }));
      var mx = Math.max.apply(null, st.woche.map(function (w) { return w.min; }).concat([12]));
      var bars = h('div', { class: 'bars' });
      st.woche.forEach(function (w) {
        bars.appendChild(h('div', {}, h('i', { class: w.geschafft ? 't' : '', style: 'height:' + Math.round(75 * w.min / mx) + 'px' }),
          h('div', { text: w.datum.slice(8) + '.' }), h('div', { text: w.min ? Math.round(w.min) + "'" : '–' })));
      });
      box.appendChild(h('div', { class: 'muted', text: 'Letzte 7 Tage (Minuten, grün = Tag geschafft)' }));
      box.appendChild(bars);
      box.appendChild(h('p', { class: 'muted', text: 'Bester Streak: ' + st.bester_streak + ' · Tage insgesamt: ' + st.tage_gesamt + ' · Minuten insgesamt: ' + st.minuten_gesamt + (st.aussprache_schnitt != null ? ' · Aussprache Ø ' + st.aussprache_schnitt + ' %' : '') }));
      if (st.kategorien.length) {
        box.appendChild(h('h3', { text: 'Stärken & Schwächen (14 Tage)' }));
        st.kategorien.forEach(function (k) {
          box.appendChild(h('div', { class: 'kbar' }, h('span', { text: k.kat }), h('div', { class: 'bar' }, h('i', { style: 'width:' + k.score + '%' })), h('span', { text: k.score + ' %' })));
        });
      }
      if (st.schwache_woerter.length) {
        box.appendChild(h('h3', { text: 'Aussprache-Baustellen' }));
        st.schwache_woerter.forEach(function (w) { box.appendChild(h('span', { class: 'chip', text: w.wort + ' ' + w.acc + '%' })); });
      }
      el.appendChild(box);
    }

    /* ---------------- Aufgabe öffnen ---------------- */
    function openTask(i) {
      stopAudio();
      var a = S.data.set.aufgaben[i], N = S.data.set.aufgaben.length;
      S.inTask = true; S.taskStart = Date.now(); S.cur = a; S.curIdx = i;
      el.textContent = '';
      var timeEl = h('span', { class: 'pill', text: '⏱ ' + fmt(totalSek()) });
      clearInterval(S.tick); S.tick = setInterval(function () { timeEl.textContent = '⏱ ' + fmt(totalSek()); }, 1000);
      el.appendChild(h('div', { class: 'top' },
        h('button', { class: 'btn sec', text: '← Übersicht', onclick: leave }),
        h('span', { class: 'grow muted', text: 'Aufgabe ' + (i + 1) + '/' + N + ' · ' + a.kat }), timeEl));
      el.appendChild(h('div', { class: 'bar', style: 'margin-bottom:8px' }, h('i', { style: 'width:' + Math.round(100 * i / N) + '%' })));
      var body = h('div'); el.appendChild(body);
      var fin = function (score, extra) { finish(a, score, extra, body); };
      var R = { karten: rKarten, mc: rMC, input: rInput, fehler: rFehler, listen: rListen, selfcheck: rSelf, read: rRead, speak: rSpeak }[a.typ];
      body.appendChild(h('h2', { text: icon(a) + ' ' + a.titel }));
      if (a.anweisung) body.appendChild(h('p', { class: 'muted', text: a.anweisung }));
      R(a, body, fin);
      window.scrollTo(0, 0);
    }
    function leave() {
      var sek = Math.round((Date.now() - S.taskStart) / 1000);
      if (S.inTask && sek >= 5) { S.today.sek = (S.today.sek || 0) + Math.min(300, sek); api('/api/englisch/zeit', { sek: Math.min(300, sek) }); }
      home();
    }
    function finish(a, score, extra, body) {
      var sek = Math.min(300, Math.round((Date.now() - S.taskStart) / 1000));
      S.inTask = false; clearInterval(S.tick); stopAudio();
      var payload = { datum: S.data.datum, id: a.id, typ: a.typ, kat: a.kat, titel: a.titel, score: score, sek: sek };
      if (extra && extra.woerter) payload.woerter = extra.woerter;
      api('/api/englisch/ergebnis', payload).then(function (r) {
        if (r && r.ok) { S.stat = r.stat; S.today = r.heute; }
      });
      var er = resultsOf(); er[a.id] = { score: Math.max(score, (er[a.id] || {}).score || 0) };
      var A = S.data.set.aufgaben, nxt = null;
      for (var k = 1; k <= A.length; k++) { var c = A[(S.curIdx + k) % A.length]; if (!er[c.id] && c.id !== a.id) { nxt = c; break; } }
      body.appendChild(h('div', { class: 'card' }, h('h3', { text: 'Geschafft: ' + pct(score) + ' %' }),
        h('div', { class: 'row' },
          nxt ? h('button', { class: 'btn', text: 'Weiter: ' + nxt.titel + ' ›', onclick: function () { openTask(A.indexOf(nxt)); } }) : null,
          h('button', { class: 'btn sec', text: 'Zur Übersicht', onclick: home }))));
      window.scrollTo(0, document.body.scrollHeight);
    }

    /* ---------------- Übersetzung (Button) ---------------- */
    function transBtn(de, enText) {
      var box = h('div'), b = h('button', { class: 'btn sec', style: 'margin-top:8px', text: '🇩🇪 Übersetzung' }), shown = false;
      b.onclick = function () {
        if (shown) { box.textContent = ''; shown = false; b.textContent = '🇩🇪 Übersetzung'; return; }
        shown = true; b.textContent = '🇩🇪 Übersetzung ausblenden';
        if (de) { box.appendChild(h('div', { class: 'expl', text: de })); return; }
        box.appendChild(h('div', { class: 'muted', text: '⏳ übersetze …' }));
        api('/api/englisch/uebersetzen', { text: enText }).then(function (r) {
          box.textContent = '';
          box.appendChild(h('div', { class: 'expl', text: r.ok ? r.de + '  (maschinell)' : '⚠️ ' + (r.error || 'nicht möglich') }));
        });
      };
      return h('div', {}, b, box);
    }
    function merkBtnIt(it, en, de, bsp, bild) { return merkBtn(en, it.wort_de || de, it.beispiel || bsp, bild); }
    /* ---------------- Wörter merken ---------------- */
    function merkBtn(en, de, bsp, bild) {
      var b = h('button', { class: 'btn sec', style: 'margin-top:10px', text: '📌 Wort merken' });
      b.onclick = function () {
        b.disabled = true;
        api('/api/englisch/wort', { en: en, de: de, bsp: bsp, bild: bild || '' }).then(function (r) { b.textContent = r.error ? '⚠️ ' + r.error : '📌 Gemerkt (' + r.anzahl + ' Wörter)'; });
      };
      return b;
    }
    function rKarten(a, body, fin) {
      var items = a.items, i = 0, ok = 0, box = h('div'); body.appendChild(box);
      (function show() {
        var it = items[i]; box.textContent = '';
        var back = h('div'), card = h('div', { class: 'card' }, h('div', { class: 'muted', text: 'Karte ' + (i + 1) + '/' + items.length + ' · Serie ' + (it.streak || 0) + '/3' }), h('p', { class: 'big', text: it.en }));
        if (it.bild) card.appendChild(h('img', { class: 'pic', src: '/api/englisch/img/' + it.bild, alt: '' }));
        var reveal = h('button', { class: 'btn', text: 'Aufdecken', onclick: function () {
          reveal.remove();
          back.appendChild(h('div', { class: 'expl', text: (it.de ? '🇩🇪 ' + it.de : '(keine Übersetzung hinterlegt)') + (it.bsp ? '\n' + it.bsp : '') }));
          function antw(g) {
            api('/api/englisch/wort-ergebnis', { id: it.wid, gewusst: g });
            if (g) ok++;
            i++; if (i < items.length) show(); else { box.textContent = ''; fin(ok / items.length); }
          }
          back.appendChild(h('div', { class: 'row', style: 'margin-top:10px' },
            h('button', { class: 'btn', text: '✅ Wusste ich', onclick: function () { antw(true); } }),
            h('button', { class: 'btn sec', text: '🔁 Noch nicht', onclick: function () { antw(false); } })));
        } });
        card.appendChild(reveal); card.appendChild(back); box.appendChild(card);
      })();
    }

    /* ---------------- Renderer: Multiple Choice ---------------- */
    function rMC(a, body, fin, items, container) {
      items = items || a.items; container = container || body;
      var i = 0, ok = 0, box = h('div'); container.appendChild(box);
      (function show() {
        var it = items[i]; box.textContent = '';
        box.appendChild(h('div', { class: 'card' }, h('div', { class: 'muted', text: 'Frage ' + (i + 1) + '/' + items.length }), h('p', { class: 'big', text: it.frage }), it.bild ? h('img', { class: 'pic', src: '/api/englisch/img/' + it.bild, alt: 'Merkbild' }) : null, transBtn(it.de, it.frage.replace('___', it.optionen ? it.optionen[it.richtig] : it.antworten[0]))));
        var answered = false, ex = h('div');
        it.optionen.forEach(function (o, k) {
          var b = h('button', { class: 'opt', text: o });
          b.onclick = function () {
            if (answered) return; answered = true;
            var right = k === it.richtig; if (right) ok++;
            Array.prototype.forEach.call(box.querySelectorAll('.en-opt'), function (x, n) { if (n === it.richtig) x.classList.add('en-right'); });
            if (!right) b.classList.add('en-wrong');
            if (it.erklaerung) ex.appendChild(h('div', { class: 'expl', text: (right ? '✅ ' : '❌ ') + it.erklaerung }));
            ex.appendChild(merkBtnIt(it, it.optionen[it.richtig], '', it.frage.replace('___', it.optionen[it.richtig]) + (it.erklaerung ? ' – ' + it.erklaerung : ''), it.bild));
            ex.appendChild(h('button', { class: 'btn', style: 'margin-top:10px', text: i + 1 < items.length ? 'Weiter ›' : 'Fertig ✓', onclick: function () { i++; if (i < items.length) show(); else { box.textContent = ''; fin(ok / items.length); } } }));
          };
          box.appendChild(b);
        });
        box.appendChild(ex);
      })();
    }

    /* ---------------- Renderer: Eintippen / Lückentext ---------------- */
    function rInput(a, body, fin) {
      var items = a.items, i = 0, ok = 0, box = h('div'); body.appendChild(box);
      (function show() {
        var it = items[i]; box.textContent = '';
        var inp = h('input', { class: 'txt', type: 'text', autocomplete: 'off', autocapitalize: 'off', spellcheck: 'false', placeholder: 'Antwort tippen …' });
        var res = h('div'), btn = h('button', { class: 'btn', style: 'margin-top:8px', text: 'Prüfen' });
        box.appendChild(h('div', { class: 'card' }, h('div', { class: 'muted', text: 'Frage ' + (i + 1) + '/' + items.length }), h('p', { class: 'big', text: it.frage }), it.bild ? h('img', { class: 'pic', src: '/api/englisch/img/' + it.bild, alt: 'Merkbild' }) : null, transBtn(it.de, it.frage.replace('___', it.optionen ? it.optionen[it.richtig] : it.antworten[0])), it.hinweis ? h('div', { class: 'muted', text: '💡 ' + it.hinweis }) : null, inp, btn, res));
        var checked = false;
        function check() {
          if (checked) return; checked = true; btn.disabled = true; inp.disabled = true;
          var u = norm(inp.value), good = it.antworten.some(function (x) { return norm(x) === u; });
          if (good) ok++;
          res.appendChild(h('div', { class: 'expl', text: (good ? '✅ Richtig! ' : '❌ Gesucht: ' + it.antworten[0] + '. ') + (it.erklaerung || '') }));
          res.appendChild(merkBtnIt(it, it.antworten[0], '', it.frage.replace('___', it.antworten[0]) + (it.erklaerung ? ' – ' + it.erklaerung : ''), it.bild));
          var row = h('div', { class: 'row', style: 'margin-top:10px' });
          if (!good) row.appendChild(h('button', { class: 'btn sec', text: 'Meine Antwort war auch richtig', onclick: function (ev) { ok++; ev.target.remove(); } }));
          row.appendChild(h('button', { class: 'btn', text: i + 1 < items.length ? 'Weiter ›' : 'Fertig ✓', onclick: function () { i++; if (i < items.length) show(); else { box.textContent = ''; fin(Math.min(1, ok / items.length)); } } }));
          res.appendChild(row);
        }
        btn.onclick = check; inp.onkeydown = function (e) { if (e.key === 'Enter') check(); };
        setTimeout(function () { inp.focus(); }, 50);
      })();
    }

    /* ---------------- Renderer: Fehlerjagd ---------------- */
    function rFehler(a, body, fin) {
      var items = a.items, i = 0, ok = 0, box = h('div'); body.appendChild(box);
      (function show() {
        var it = items[i]; box.textContent = '';
        var parts = h('div'), ex = h('div'), answered = false;
        it.teile.forEach(function (t, k) {
          var p = h('span', { class: 'part', text: t });
          p.onclick = function () {
            if (answered) return; answered = true;
            var right = k === it.falsch; if (right) ok++;
            Array.prototype.forEach.call(parts.children, function (x, n) { if (n === it.falsch) x.classList.add('en-right'); });
            if (!right) p.classList.add('en-wrong');
            ex.appendChild(h('div', { class: 'expl', text: (right ? '✅ ' : '❌ ') + 'Besser: „' + it.korrektur + '“. ' + (it.erklaerung || '') }));
            ex.appendChild(merkBtnIt(it, it.korrektur, '', it.erklaerung || '', ''));
            ex.appendChild(h('button', { class: 'btn', style: 'margin-top:10px', text: i + 1 < items.length ? 'Weiter ›' : 'Fertig ✓', onclick: function () { i++; if (i < items.length) show(); else { box.textContent = ''; fin(ok / items.length); } } }));
          };
          parts.appendChild(p);
        });
        box.appendChild(h('div', { class: 'card' }, h('div', { class: 'muted', text: 'Satz ' + (i + 1) + '/' + items.length + ' – tippe den Teil mit dem Fehler an' }), parts, transBtn(it.de, it.teile.map(function (t, k) { return k === it.falsch ? it.korrektur : t; }).join(' ')), ex));
      })();
    }

    /* ---------------- TTS ---------------- */
    function speakTTS(text, voice, rate) {
      var key = voice + '|' + rate + '|' + text;
      var go = function (url) { stopAudio(); var au = new Audio(url); S.audio = au; au.play(); return au; };
      if (S.cache[key]) return Promise.resolve(go(S.cache[key]));
      return fetch('/api/bolla/tts', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: text, voice: voice, rate: rate }) })
        .then(function (r) { if (!r.ok) throw new Error('TTS ' + r.status); return r.blob(); })
        .then(function (b) { var u = URL.createObjectURL(b); S.cache[key] = u; return go(u); });
    }
    function voice(n) { return VOICES[S.accent][(n || 0) % 3]; }

    /* ---------------- Renderer: Hörverstehen ---------------- */
    function rListen(a, body, fin) {
      var v = voice(S.data.datum.charCodeAt(9) || 0);
      var btnN = h('button', { class: 'btn', text: '▶ Anhören' }), btnS = h('button', { class: 'btn sec', text: '🐢 Langsamer' });
      var info = h('div', { class: 'muted', text: 'Du kannst beliebig oft hören. Das Transkript gibt es erst danach.' });
      var play = function (rate) { return function () { speakTTS(a.text, v, rate).catch(function (e) { info.textContent = '⚠️ Audio nicht möglich: ' + e.message; }); }; };
      btnN.onclick = play(0); btnS.onclick = play(-25);
      body.appendChild(h('div', { class: 'card' }, h('div', { class: 'row' }, btnN, btnS), info));
      var qs = h('div'); body.appendChild(qs);
      rMC(a, body, function (score) {
        body.appendChild(h('div', { class: 'card' }, h('h3', { text: 'Transkript' }), h('p', { text: a.text }), transBtn(a.text_de, a.text)));
        fin(score);
      }, a.items, qs);
    }

    /* ---------------- Renderer: Selbstkontrolle / Schreiben / Bild ---------------- */
    function rSelf(a, body, fin) {
      var items = a.items, i = 0, sum = 0, box = h('div'); body.appendChild(box);
      (function show() {
        var it = items[i]; box.textContent = '';
        var ta = h('textarea', { class: 'txt', placeholder: 'Deine Antwort …', spellcheck: 'false' });
        var res = h('div'), show_ = h('button', { class: 'btn', text: '👀 Lösung zeigen' });
        var card = h('div', { class: 'card' }, h('div', { class: 'muted', text: items.length > 1 ? ('Aufgabe ' + (i + 1) + '/' + items.length) : '' }));
        if (a.bild) card.appendChild(h('img', { class: 'pic', src: '/api/englisch/img/' + a.bild, alt: 'Bild zum Beschreiben' }));
        card.appendChild(h('p', { class: 'big', text: it.aufgabe }));
        if (it.vokabeln) { var v = h('div'); it.vokabeln.forEach(function (w) { v.appendChild(h('span', { class: 'chip', text: w })); }); card.appendChild(v); }
        card.appendChild(ta);
        var row = h('div', { class: 'row', style: 'margin-top:8px' }, show_);
        var fbBtn = it.feedback ? h('button', { class: 'btn sec', text: '🧠 Feedback von Bolla' }) : null;
        if (fbBtn) row.appendChild(fbBtn);
        card.appendChild(row); card.appendChild(res); box.appendChild(card);
        var rated = false;
        function next(score) {
          if (rated) return; rated = true; sum += score;
          res.appendChild(h('button', { class: 'btn', style: 'margin-top:10px', text: i + 1 < items.length ? 'Weiter ›' : 'Fertig ✓', onclick: function () { i++; if (i < items.length) show(); else { box.textContent = ''; fin(sum / items.length); } } }));
        }
        function rateRow() {
          if (res.querySelector('.en-rate')) return;
          res.appendChild(h('div', { class: 'row rate', style: 'margin-top:10px' }, h('span', { text: 'Wie lief es?' }),
            h('button', { class: 'btn ok', text: '😎 Sitzt', onclick: function (e) { hideRate(); next(1); } }),
            h('button', { class: 'btn sec', text: '🤏 Fast', onclick: function () { hideRate(); next(0.5); } }),
            h('button', { class: 'btn bad', text: '😬 Daneben', onclick: function () { hideRate(); next(0); } })));
        }
        function hideRate() { var r = res.querySelector('.en-rate'); if (r) r.remove(); }
        show_.onclick = function () {
          show_.disabled = true;
          res.appendChild(h('div', { class: 'expl' }, h('b', { text: it.loesungen.length > 1 ? 'Mögliche Lösungen:' : 'Musterlösung:' }), h('br'), it.loesungen.join('\n'), it.hinweis ? h('div', { class: 'muted', text: '💡 ' + it.hinweis }) : null));
          res.lastChild.style.whiteSpace = 'pre-wrap';
          if (!(fbBtn && ta.value.trim().length > 8 && fbBtn.dataset.done)) rateRow();
        };
        if (fbBtn) fbBtn.onclick = function () {
          if (ta.value.trim().length < 8) { res.appendChild(h('div', { class: 'expl', text: 'Schreib erst etwas (mind. ein Satz), dann gibt es Feedback.' })); return; }
          fbBtn.disabled = true; fbBtn.textContent = '⏳ Bolla liest …'; fbBtn.dataset.done = '1';
          api('/api/englisch/feedback', { aufgabe: it.aufgabe, text: ta.value }).then(function (r) {
            fbBtn.textContent = '🧠 Feedback erhalten';
            if (!r.ok) { res.appendChild(h('div', { class: 'expl', text: '⚠️ ' + (r.error || 'Feedback fehlgeschlagen') })); fbBtn.disabled = false; fbBtn.dataset.done = ''; rateRow(); return; }
            var f = r.feedback, c = h('div', { class: 'expl' });
            if (f.stark) c.appendChild(h('p', { text: '💪 ' + f.stark }));
            c.appendChild(h('b', { text: 'Korrigierte Version:' })); c.appendChild(h('p', { text: f.korrigiert || '–' }));
            (f.fehler || []).forEach(function (x) { c.appendChild(h('div', { text: '• „' + x.falsch + '“ → „' + x.richtig + '“ – ' + x.erklaerung })); });
            if (f.tipp) c.appendChild(h('p', { text: '🎯 ' + f.tipp }));
            res.appendChild(c);
            if (!show_.disabled) show_.click();
            hideRate(); next(f.note);
          }).catch(function (e) { fbBtn.disabled = false; res.appendChild(h('div', { class: 'expl', text: '⚠️ ' + e })); });
        };
      })();
    }

    /* ---------------- Azure Speech / Aussprache ---------------- */
    function ensureSDK() {
      if (window.SpeechSDK) return Promise.resolve();
      return new Promise(function (res, rej) {
        var s = h('script', { src: 'https://cdn.jsdelivr.net/npm/microsoft-cognitiveservices-speech-sdk/distrib/browser/microsoft.cognitiveservices.speech.sdk.bundle-min.js' });
        s.onload = res; s.onerror = function () { rej(new Error('Azure Speech SDK nicht ladbar')); }; document.head.appendChild(s);
      });
    }
    function speechCfg() {
      if (S.speechCfg) return Promise.resolve(S.speechCfg);
      return api('/api/speech/config').then(function (c) { if (c.error) throw new Error(c.error); S.speechCfg = c; return c; });
    }
    function cls(a) { return a >= 85 ? 'w-g' : a >= 60 ? 'w-o' : 'w-r'; }
    function wordsFromJson(j) {
      // SDK-JSON: Werte unter .PronunciationAssessment; REST-JSON: flach – beides abfangen
      var nb = j && j.NBest && j.NBest[0]; if (!nb) return { words: [], sc: null };
      var pick = function (o) { return o && o.PronunciationAssessment ? o.PronunciationAssessment : (o || {}); };
      return { sc: pick(nb), words: (nb.Words || []).map(function (w) {
        var wp = pick(w);
        return { w: w.Word, acc: wp.AccuracyScore != null ? wp.AccuracyScore : 0, err: wp.ErrorType || 'None',
          ph: (w.Phonemes || []).map(function (p) { return { p: p.Phoneme, acc: pick(p).AccuracyScore }; }) };
      }) };
    }
    function scoreTiles(sc) {
      var d = h('div');
      [['Gesamt', sc.PronScore], ['Genauigkeit', sc.AccuracyScore], ['Flüssigkeit', sc.FluencyScore], ['Vollständig', sc.CompletenessScore]].forEach(function (x) {
        if (x[1] != null) d.appendChild(h('span', { class: 'score' }, h('b', { class: cls(x[1]), text: Math.round(x[1]) }), x[0]));
      });
      return d;
    }
    function wordLine(words, detail) {
      var line = h('p', { class: 'big' });
      words.forEach(function (w) {
        var sp = h('span', { class: 'w ' + cls(w.acc), text: w.w });
        sp.onclick = function () {
          var bad = w.ph.filter(function (p) { return p.acc != null && p.acc < 70; });
          detail.textContent = '„' + w.w + '“: ' + Math.round(w.acc) + ' %' + (w.err !== 'None' ? ' (' + ({ Mispronunciation: 'falsch ausgesprochen', Omission: 'ausgelassen', Insertion: 'eingefügt' }[w.err] || w.err) + ')' : '') + (bad.length ? ' · schwache Laute: ' + bad.map(function (p) { return '/' + p.p + '/ ' + Math.round(p.acc) + '%'; }).join(', ') : '');
        };
        line.appendChild(sp); line.appendChild(document.createTextNode(' '));
      });
      return line;
    }
    function micErrorMsg(e) { return '⚠️ Mikrofon/Azure: ' + (e && e.message ? e.message : e) + ' – Mikrofon-Freigabe im Browser prüfen.'; }

    /* ---------------- Renderer: Laut lesen ---------------- */
    function rRead(a, body, fin) {
      var sents = a.saetze, i = 0, scores = [], allWords = [], box = h('div'); body.appendChild(box);
      if (a.fokus) body.insertBefore(h('div', { class: 'expl', text: '🎯 Fokus: ' + a.fokus + (a.tipp ? ' – ' + a.tipp : '') }), box);
      (function show() {
        var text = sents[i]; box.textContent = '';
        var out = h('div'), detail = h('div', { class: 'muted' }), best = null;
        var mic = h('button', { class: 'btn', text: '🎤 Aufnehmen' }), model = h('button', { class: 'btn sec', text: '🔊 Vorbild' }), slow = h('button', { class: 'btn sec', text: '🐢 langsam' });
        model.onclick = function () { speakTTS(text, voice(i), -5); }; slow.onclick = function () { speakTTS(text, voice(i), -30); };
        box.appendChild(h('div', { class: 'card' }, h('div', { class: 'muted', text: 'Satz ' + (i + 1) + '/' + sents.length + ' – erst Vorbild hören, dann selbst lesen' }), h('p', { class: 'big', text: text }), transBtn(a.saetze_de && a.saetze_de[i], text), h('div', { class: 'row' }, model, slow, mic), out, detail));
        mic.onclick = function () {
          mic.disabled = true; mic.textContent = '🔴 Sprich jetzt …'; mic.classList.add('en-blink'); out.textContent = ''; detail.textContent = '';
          assessOnce(text).then(function (r) {
            mic.disabled = false; mic.classList.remove('en-blink'); mic.textContent = '🎤 Nochmal';
            if (!r.words.length) { out.appendChild(h('div', { class: 'expl', text: 'Ich habe nichts verstanden – nochmal, etwas lauter und näher am Mikro.' })); return; }
            out.textContent = ''; out.appendChild(scoreTiles(r.sc)); out.appendChild(wordLine(r.words, detail));
            out.appendChild(h('div', { class: 'muted', text: 'Tippe ein Wort für Details (grün gut · orange ok · rot üben).' }));
            if (!best || (r.sc.PronScore || 0) > (best.sc.PronScore || 0)) best = r;
            if (!out.querySelector('.en-nx')) out.appendChild(h('button', { class: 'btn nx', style: 'margin-top:8px', text: i + 1 < sents.length ? 'Nächster Satz ›' : 'Fertig ✓', onclick: function () {
              scores.push((best.sc.PronScore || 0) / 100); best.words.forEach(function (w) { allWords.push({ w: w.w, acc: w.acc }); });
              i++; if (i < sents.length) show(); else { box.textContent = ''; fin(scores.reduce(function (x, y) { return x + y; }, 0) / scores.length, { woerter: allWords }); } } }));
          }).catch(function (e) { mic.disabled = false; mic.classList.remove('en-blink'); mic.textContent = '🎤 Nochmal'; out.appendChild(h('div', { class: 'expl', text: micErrorMsg(e) })); });
        };
      })();
    }
    function assessOnce(refText) {
      return Promise.all([ensureSDK(), speechCfg()]).then(function (r) {
        var cfg = r[1], SDK = window.SpeechSDK;
        var sc = SDK.SpeechConfig.fromSubscription(cfg.key, cfg.region); sc.speechRecognitionLanguage = S.accent;
        var rec = new SDK.SpeechRecognizer(sc, SDK.AudioConfig.fromDefaultMicrophoneInput());
        var pa = new SDK.PronunciationAssessmentConfig(refText, SDK.PronunciationAssessmentGradingSystem.HundredMark, SDK.PronunciationAssessmentGranularity.Phoneme, true);
        pa.applyTo(rec);
        return new Promise(function (res, rej) {
          rec.recognizeOnceAsync(function (result) {
            try {
              if (result.reason === SDK.ResultReason.NoMatch) { rec.close(); return res({ words: [], sc: {} }); }
              if (result.reason === SDK.ResultReason.Canceled) { var cd = SDK.CancellationDetails.fromResult(result); rec.close(); return rej(new Error(cd.errorDetails || 'abgebrochen')); }
              var j = JSON.parse(result.properties.getProperty(SDK.PropertyId.SpeechServiceResponse_JsonResult)); rec.close(); res(wordsFromJson(j));
            } catch (e) { rej(e); }
          }, function (err) { try { rec.close(); } catch (x) {} rej(new Error(err)); });
        });
      });
    }

    /* ---------------- Renderer: Frei sprechen ---------------- */
    function rSpeak(a, body, fin) {
      var card = h('div', { class: 'card' }, h('p', { class: 'big', text: a.frage }), h('div', { class: 'muted', text: 'Sprich etwa ' + (a.min_sek || 30) + ' Sekunden frei. Hilfreiche Phrasen:' }));
      (a.hilfen || []).forEach(function (p) { card.appendChild(h('span', { class: 'chip', text: p })); });
      var mic = h('button', { class: 'btn', text: '🎤 Start' }), out = h('div'), detail = h('div', { class: 'muted' }), tm = h('span', { class: 'pill', text: '0:00' });
      card.appendChild(h('div', { class: 'row', style: 'margin-top:10px' }, mic, tm)); card.appendChild(out); card.appendChild(detail); body.appendChild(card);
      var rec = null, started = 0, tmr = null, texts = [], jsons = [];
      mic.onclick = function () {
        if (rec) { stopRec(); return; }
        mic.disabled = true; out.textContent = ''; texts = []; jsons = [];
        Promise.all([ensureSDK(), speechCfg()]).then(function (r) {
          var cfg = r[1], SDK = window.SpeechSDK;
          var sc = SDK.SpeechConfig.fromSubscription(cfg.key, cfg.region); sc.speechRecognitionLanguage = S.accent;
          rec = new SDK.SpeechRecognizer(sc, SDK.AudioConfig.fromDefaultMicrophoneInput());
          var pa = new SDK.PronunciationAssessmentConfig('', SDK.PronunciationAssessmentGradingSystem.HundredMark, SDK.PronunciationAssessmentGranularity.Phoneme, false);
          pa.applyTo(rec);
          rec.recognized = function (s, e) {
            if (e.result.reason === SDK.ResultReason.RecognizedSpeech) {
              texts.push(e.result.text);
              try { jsons.push(JSON.parse(e.result.properties.getProperty(SDK.PropertyId.SpeechServiceResponse_JsonResult))); } catch (x) {}
            }
          };
          rec.canceled = function (s, e) { if (e.errorDetails) detail.textContent = '⚠️ ' + e.errorDetails; };
          rec.startContinuousRecognitionAsync(function () {
            started = Date.now(); mic.disabled = false; mic.textContent = '⏹ Fertig'; mic.classList.add('en-blink');
            tmr = setInterval(function () { tm.textContent = fmt((Date.now() - started) / 1000); }, 500);
          }, function (err) { mic.disabled = false; rec = null; out.appendChild(h('div', { class: 'expl', text: micErrorMsg(err) })); });
        }).catch(function (e) { mic.disabled = false; rec = null; out.appendChild(h('div', { class: 'expl', text: micErrorMsg(e) })); });
      };
      function stopRec() {
        mic.disabled = true; mic.classList.remove('en-blink'); clearInterval(tmr);
        var r = rec; rec = null;
        r.stopContinuousRecognitionAsync(function () {
          setTimeout(function () { try { r.close(); } catch (x) {} evaluate(); mic.disabled = false; mic.textContent = '🎤 Nochmal'; }, 400);
        }, function (err) { mic.disabled = false; out.appendChild(h('div', { class: 'expl', text: micErrorMsg(err) })); });
      }
      function evaluate() {
        out.textContent = '';
        var words = [], n = 0, sums = { PronScore: 0, AccuracyScore: 0, FluencyScore: 0, CompletenessScore: 0 };
        jsons.forEach(function (j) { var r = wordsFromJson(j); if (r.sc) { n++; for (var k in sums) sums[k] += (r.sc[k] || 0); } words = words.concat(r.words); });
        if (!n || words.length < 3) { out.appendChild(h('div', { class: 'expl', text: 'Zu wenig erkannt – sprich etwas länger/lauter und versuch es nochmal.' })); return; }
        for (var k in sums) sums[k] /= n;
        out.appendChild(scoreTiles(sums));
        out.appendChild(h('p', { class: 'muted', text: 'Du hast ' + words.length + ' Wörter in ' + fmt((Date.now() - started) / 1000) + ' gesprochen (' + Math.round(words.length * 60 / Math.max(5, (Date.now() - started) / 1000)) + ' Wörter/min).' }));
        out.appendChild(h('p', { text: 'Verstanden habe ich: „' + texts.join(' ') + '“' }));
        out.appendChild(wordLine(words, detail));
        var lang = Math.min(1, words.length / 35);
        out.appendChild(h('button', { class: 'btn', style: 'margin-top:8px', text: 'Fertig ✓', onclick: function () {
          out.textContent = ''; mic.style.display = 'none'; fin(Math.min(1, (sums.PronScore / 100) * (0.6 + 0.4 * lang)), { woerter: words.map(function (w) { return { w: w.w, acc: w.acc }; }) }); } }));
      }
    }

    load();
  }

  window.EnglischTrainer = { mount: mount };
})();
