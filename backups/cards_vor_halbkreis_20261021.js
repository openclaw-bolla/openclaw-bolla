/* Kartenstapel der Startseite: Karten drehen sich der Reihe nach nach vorn, die dahinter sind grau. */
var CARD_L = document.documentElement.lang === 'en' ? {go:'Take a look', show:function(i,n){return 'Show card '+i+' of '+n}, grp:'Card stack'}
                                                    : {go:'Ansehen', show:function(i,n){return 'Karte '+i+' von '+n+' zeigen'}, grp:'Kartenstapel'};

class PreviewCard extends HTMLElement {
  connectedCallback(){
    const g = a => this.getAttribute(a) || '';
    const shadow = this.attachShadow({mode:'open'});
    shadow.innerHTML = `
      <style>
        :host{display:block}
        a.card{display:flex; flex-direction:column; text-decoration:none; color:inherit; background:#fff;
          border:1px solid #eadfce; border-radius:26px; overflow:hidden; box-shadow:0 14px 40px rgba(26,21,36,.12);
          transition:transform .18s ease, box-shadow .18s ease}
        a.card:hover, a.card:focus-visible{transform:translateY(-5px); box-shadow:0 22px 52px rgba(26,21,36,.2); outline:none}
        .shot{background:linear-gradient(160deg,#0d1b3d,#3a2b5c 40%,#8a4a6b 75%,#e8896b); padding:20px 20px 0}
        .frame{border-radius:12px 12px 0 0; overflow:hidden; background:#fff; box-shadow:0 12px 30px rgba(0,0,0,.35)}
        .bar{display:flex; align-items:center; gap:6px; padding:9px 12px; background:#2a2140}
        .bar i{width:9px; height:9px; border-radius:50%; background:rgba(255,255,255,.45)}
        .addr{margin-left:8px; flex:1; font-size:12px; color:rgba(255,255,255,.8); background:rgba(255,255,255,.12);
          border-radius:999px; padding:3px 12px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
        img{display:block; width:100%; height:auto; max-height:300px; object-fit:cover; object-position:top}
        .body{padding:26px 30px 30px}
        .meta{display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:10px}
        .kicker{font-size:14px; letter-spacing:.16em; text-transform:uppercase; color:#8a4a6b; font-weight:700}
        .tag{font-size:13px; font-weight:700; color:#fff; background:#8a4a6b; padding:3px 12px; border-radius:999px}
        h3{font-size:clamp(23px,3vw,30px); line-height:1.2; color:#1a1524; margin-bottom:12px}
        p{font-size:18px; color:#4a4358; margin-bottom:18px; line-height:1.55}
        .go{font-size:17px; font-weight:700; color:#8a4a6b}
        .go .arrow{display:inline-block; transition:transform .18s ease}
        a.card:hover .go .arrow{transform:translateX(4px)}
      </style>
      <a class="card" href="${g('href')}">
        <div class="shot"><div class="frame">
          <div class="bar"><i></i><i></i><i></i><span class="addr">${g('url')}</span></div>
          <img src="${g('shot')}" alt="${g('url')}">
        </div></div>
        <div class="body">
          <div class="meta"><span class="kicker">${g('kicker')}</span>${g('tag') ? `<span class="tag">${g('tag')}</span>` : ''}</div>
          <h3>${g('heading')}</h3>
          <p>${g('desc')}</p>
          <div class="go">${CARD_L.go} <span class="arrow">→</span></div>
        </div>
      </a>`;
  }
}
customElements.define('preview-card', PreviewCard);

class CardStack extends HTMLElement {
  connectedCallback(){
    this._index = 0; this._locked = false;
    const shadow = this.attachShadow({mode:'open'});
    shadow.innerHTML = `
      <style>
        :host{display:block}
        .viewport{position:relative; transition:height .35s cubic-bezier(.2,.8,.2,1)}
        .dots{display:flex; justify-content:center; gap:10px; margin-top:22px}
        .dots button{width:11px; height:11px; padding:0; border-radius:50%; border:none; background:#e0d3bd; cursor:pointer; transition:background .2s, transform .2s}
        .dots button.active{background:#8a4a6b; transform:scale(1.25)}
        .hint{text-align:center; font-size:15px; color:#6b6478; margin-top:14px; opacity:.85; transition:opacity .5s ease}
        .hint.gone{opacity:0}
      </style>
      <div class="viewport"><slot></slot></div>
      <div class="dots"></div>
      <div class="hint">${this.getAttribute('hint') || ''}</div>`;
    this._viewport = shadow.querySelector('.viewport');
    this._dotsEl = shadow.querySelector('.dots');
    this._hintEl = shadow.querySelector('.hint');
    this._cards = shadow.querySelector('slot').assignedElements();
    this._cards.forEach((card, i) => {
      card.style.position = 'absolute'; card.style.top = '0'; card.style.left = '0';
      card.style.transition = 'transform .45s cubic-bezier(.2,.8,.2,1), opacity .45s ease, filter .45s ease';
      card.addEventListener('click', e => { if(i !== this._index){ e.preventDefault(); this._goTo(i); } });
    });
    this._cards.forEach((_, i) => {
      const b = document.createElement('button');
      b.setAttribute('aria-label', CARD_L.show(i + 1, this._cards.length));
      b.addEventListener('click', () => this._goTo(i));
      this._dotsEl.appendChild(b);
    });
    this.tabIndex = 0;
    this.setAttribute('role', 'group'); this.setAttribute('aria-roledescription', CARD_L.grp);
    this.addEventListener('wheel', e => this._onWheel(e), {passive:false});
    this.addEventListener('keydown', e => this._onKey(e));
    this._touchY = null;
    this.addEventListener('touchstart', e => { this._touchY = e.touches[0].clientY; this._touchX = e.touches[0].clientX; }, {passive:true});
    this.addEventListener('touchend', e => {
      const dx = e.changedTouches[0].clientX - this._touchX, dy = e.changedTouches[0].clientY - this._touchY;
      if(Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)){ this._dismissHint(); this._advance(dx < 0 ? 1 : -1); }
    }, {passive:true});
    window.addEventListener('resize', () => this._layout());
    window.addEventListener('load', () => this._measure());
    this._layout();
  }
  _goTo(i){ if(i === this._index) return; this._index = i; this._layout(); this._dismissHint(); }
  _advance(dir){
    const n = this._cards.length;
    this._index = (this._index + dir + n) % n; this._layout(); this._locked = true;
    clearTimeout(this._lockT); this._lockT = setTimeout(() => { this._locked = false; }, 480);
  }
  _onWheel(e){
    /* Seite normal scrollen lassen, solange der Stapel am Rand angekommen ist */
    const dir = e.deltaY > 0 ? 1 : -1;
    if((dir > 0 && this._index === this._cards.length - 1) || (dir < 0 && this._index === 0)) return;
    e.preventDefault();
    if(this._locked) return;
    this._dismissHint(); this._advance(dir);
  }
  _onKey(e){
    if(e.key === 'ArrowDown' || e.key === 'ArrowRight'){ this._dismissHint(); this._advance(1); }
    else if(e.key === 'ArrowUp' || e.key === 'ArrowLeft'){ this._dismissHint(); this._advance(-1); }
  }
  _dismissHint(){ this._hintEl.classList.add('gone'); }
  _layout(){
    const n = this._cards.length;
    const boxW = this.getBoundingClientRect().width || 700;
    const ox = Math.min(boxW * 0.07, 70), oy = Math.min(boxW * 0.03, 26);
    this._off = oy;
    this._cards.forEach((card, i) => {
      const rel = (i - this._index + n) % n;
      card.style.width = (boxW - 2 * ox) + 'px';
      if(rel === 0){
        card.style.transform = 'translate(0,0) scale(1)'; card.style.opacity = '1'; card.style.filter = 'none';
        card.style.zIndex = String(n + 10); card.style.pointerEvents = 'auto'; card.style.visibility = 'visible';
      } else if(rel <= 2){
        card.style.transform = `translate(${rel * ox}px, ${rel * oy}px) scale(${1 - rel * 0.05})`;
        card.style.opacity = String(Math.max(0.55, 0.9 - (rel - 1) * 0.2)); card.style.filter = 'grayscale(1)';
        card.style.zIndex = String(n + 10 - rel); card.style.pointerEvents = 'auto'; card.style.visibility = 'visible';
      } else {
        card.style.transform = `translate(${ox * 2.5}px, ${oy * 2.5}px) scale(0.85)`; card.style.opacity = '0'; card.style.filter = 'grayscale(1)';
        card.style.zIndex = '1'; card.style.pointerEvents = 'none'; card.style.visibility = 'hidden';
      }
    });
    Array.from(this._dotsEl.children).forEach((d, i) => d.classList.toggle('active', i === this._index));
    requestAnimationFrame(() => this._measure());
  }
  _measure(){
    const front = this._cards[this._index];
    const h = front.getBoundingClientRect().height;
    if(h > 0) this._viewport.style.height = (h + (this._off || 26) * 2 + 24) + 'px';
  }
}
customElements.define('card-stack', CardStack);
