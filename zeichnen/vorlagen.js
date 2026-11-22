// Zeichentrainer — Vorlagen. Neue Vorlagen werden von Bolla am Ende angehängt (L.push({...})).
// Koordinaten: 1600 x 1200. outline = Umrisslinien (dunkelgrau), hatch = Schraffur-Hilfen (hellgrau).
// Beides verschwindet dort, wo Chris darüber zeichnet.
(function () {
  const L = (window.VORLAGEN = []);

  // Linienschar im Winkel (Grad) mit Abstand gap — wird per clip/mask zugeschnitten
  function hatch(angle, gap, cx = 800, cy = 600, R = 1100) {
    const a = (angle * Math.PI) / 180, dx = Math.cos(a), dy = Math.sin(a), nx = -dy, ny = dx;
    let d = '';
    for (let o = -R; o <= R; o += gap) {
      const px = cx + nx * o, py = cy + ny * o;
      d += `M${(px - dx * R).toFixed(1)} ${(py - dy * R).toFixed(1)}L${(px + dx * R).toFixed(1)} ${(py + dy * R).toFixed(1)}`;
    }
    return `<path d="${d}"/>`;
  }
  // Maske: weiße Form minus schwarze Formen
  function mask(id, white, black) {
    return `<mask id="${id}" maskUnits="userSpaceOnUse" x="0" y="0" width="1600" height="1200"><rect width="1600" height="1200" fill="#000"/>${white}${black || ''}</mask>`;
  }
  const W = (s) => s.replace('/>', ' fill="#fff" stroke="none"/>');
  const B = (s) => s.replace('/>', ' fill="#000" stroke="none"/>');
  const sun =
    '<circle cx="150" cy="150" r="34"/>' +
    [0, 45, 90, 135, 180, 225, 270, 315].map((a) => {
      const r = (a * Math.PI) / 180;
      return `<path d="M${150 + Math.cos(r) * 50} ${150 + Math.sin(r) * 50}L${150 + Math.cos(r) * 72} ${150 + Math.sin(r) * 72}"/>`;
    }).join('') +
    '<path d="M215 215L320 320M320 320L286 316M320 320L316 286"/>';

  // ---------- 0: Leeres Blatt ----------
  L.push({
    id: 'leer', title: 'Leeres Blatt',
    hints: ['Freies Zeichnen ohne Vorlage.', 'Neue Vorlage gewünscht? Sag Bolla im Chat, was du üben willst — danach F5.'],
    defs: '', outline: '', hatch: '',
  });

  // ---------- 1: Kugel ----------
  L.push({
    id: 'kugel', title: 'Kugel (Licht oben links)',
    hints: [
      '1. Kreis nachzeichnen — locker, in einem Zug.',
      '2. ☀ Licht kommt von oben links. Die Lichtseite bleibt weiß.',
      '3. Halbschatten unten rechts: Schraffur, Linien parallel, gleicher Abstand.',
      '4. Kernschatten: zweite Schraffur quer darüber (Kreuzschraffur), dichter.',
      '5. Schlagschatten am Boden: waagrechte Linien, direkt unter der Kugel am dunkelsten.',
      '6. Tipp: Schraffur-Linien leicht der Kugelrundung folgen lassen.',
    ],
    defs:
      mask('mA', W('<circle cx="800" cy="560" r="300"/>'), B('<circle cx="680" cy="440" r="300"/>')) +
      mask('mB', W('<circle cx="800" cy="560" r="300"/>'), B('<circle cx="740" cy="500" r="300"/>')) +
      mask('mS', W('<ellipse cx="1030" cy="868" rx="340" ry="58"/>'), B('<circle cx="800" cy="560" r="300"/>')) +
      mask('mK', W('<ellipse cx="800" cy="864" rx="160" ry="20"/>'), B('<circle cx="800" cy="560" r="300"/>')),
    outline: '<circle cx="800" cy="560" r="300"/>',
    hatch:
      `<g mask="url(#mA)">${hatch(45, 20)}</g>` +
      `<g mask="url(#mB)">${hatch(-45, 18)}</g>` +
      `<g mask="url(#mS)">${hatch(0, 13)}</g>` +
      `<g mask="url(#mK)">${hatch(0, 7)}</g>` + sun,
  });

  // ---------- 2: Würfel ----------
  L.push({
    id: 'wuerfel', title: 'Würfel (Licht oben links)',
    hints: [
      '1. Umriss: erst die Deckfläche (Raute), dann die senkrechten Kanten, dann unten.',
      '2. ☀ Licht von oben links: Deckfläche hell (weiß), linke Fläche mittel, rechte Fläche dunkel.',
      '3. Linke Fläche: einfache Schraffur, Linien parallel zur Oberkante.',
      '4. Rechte Fläche: Kreuzschraffur, dichter.',
      '5. Schlagschatten fällt nach rechts vorn auf den Boden: Linien parallel zur Bodenkante.',
      '6. Kanten, die dem Licht abgewandt sind, kräftiger nachziehen.',
    ],
    defs:
      '<clipPath id="cl"><path d="M540 450L800 600V900L540 750Z"/></clipPath>' +
      '<clipPath id="cr"><path d="M800 600L1060 450V750L800 900Z"/></clipPath>' +
      '<clipPath id="cs"><path d="M800 900L1060 750L1290 880L1030 1030Z"/></clipPath>',
    outline: '<path d="M800 300L1060 450L800 600L540 450Z M540 450V750L800 900L1060 750V450 M800 600V900"/>',
    hatch:
      `<g clip-path="url(#cl)">${hatch(30, 22)}</g>` +
      `<g clip-path="url(#cr)">${hatch(-30, 16)}${hatch(90, 16)}</g>` +
      `<g clip-path="url(#cs)">${hatch(-30, 14)}</g>` + sun,
  });

  // ---------- 3: Zylinder ----------
  L.push({
    id: 'zylinder', title: 'Zylinder (Licht oben links)',
    hints: [
      '1. Obere Ellipse zeichnen, dann die zwei senkrechten Seiten, unten nur den vorderen Halbbogen.',
      '2. ☀ Licht von links: Schatten liegt rechts am Körper.',
      '3. Senkrechte Schraffur rechts — nach außen hin dichter (weicher Verlauf).',
      '4. Ganz rechts zusätzlich schräg kreuzen = Kernschatten.',
      '5. Schlagschatten: langgezogene Ellipse am Boden nach rechts, waagrecht schraffieren.',
      '6. Die Deckfläche bleibt hell.',
    ],
    defs:
      '<clipPath id="body"><path d="M580 330V830A220 70 0 0 0 1020 830V330A220 70 0 0 1 580 330Z"/></clipPath>' +
      '<clipPath id="b1"><rect x="850" y="250" width="200" height="700"/></clipPath>' +
      '<clipPath id="b2"><rect x="940" y="250" width="120" height="700"/></clipPath>' +
      mask('mZ', W('<ellipse cx="1110" cy="862" rx="310" ry="54"/>'),
        B('<path d="M580 330V830A220 70 0 0 0 1020 830V330Z"/>')),
    outline:
      '<ellipse cx="800" cy="330" rx="220" ry="70"/><path d="M580 330V830M1020 330V830M580 830A220 70 0 0 0 1020 830"/>',
    hatch:
      `<g clip-path="url(#body)"><g clip-path="url(#b1)">${hatch(90, 18)}</g><g clip-path="url(#b2)">${hatch(55, 14)}</g></g>` +
      `<g mask="url(#mZ)">${hatch(0, 13)}</g>` + sun,
  });

  // ---------- 4: Berg mit Kind auf Zipfelbob ----------
  const poly = (pts) => 'M' + pts.map((q) => q.join(' ')).join('L') + 'Z';
  const mount = [[0,760],[120,620],[230,540],[330,420],[400,340],[480,260],[550,330],[610,390],[680,470],[780,580],[860,680],[920,760]];
  const shadeFace = [[480,260],[550,330],[610,390],[680,470],[780,580],[860,680],[920,760],[760,760],[640,560],[560,380]];
  const coreFace = [[550,330],[610,390],[680,470],[780,580],[860,680],[800,700],[700,560],[600,420]];
  const tree = (x, y, h) =>
    [0, 1, 2].map((i) => {
      const w = h * (0.34 - i * 0.07), top = y - h + i * h * 0.27;
      return `<path d="M${x} ${top}L${x - w} ${top + h * 0.42}L${x + w} ${top + h * 0.42}Z"/>`;
    }).join('') + `<path d="M${x} ${y - h * 0.2}V${y}"/>`;
  const BOB = 'M-150 -8L110 -8Q175 -8 200 -70Q150 -32 110 -32L-150 -32Q-162 -20 -150 -8Z';
  const TORSO = 'M-125 -32Q-135 -100 -108 -150Q-90 -172 -60 -165Q-30 -150 -22 -110L-18 -32Z';
  const LEGS = 'M-80 -34L40 -34L125 -36L126 -62L44 -72L-70 -66Z';
  const K = 'translate(1180 1061) rotate(9.65) scale(1.6)';
  const kid = (inner, sw) => `<g transform="${K}" stroke-width="${sw}">${inner}</g>`;
  L.push({
    id: 'berg-zipfelbob', title: 'Berg mit Kind auf Zipfelbob',
    hints: [
      '1. Zuerst die schräge Hanglinie von links oben nach rechts unten — der Boden für alles.',
      '2. Bergumriss: kantige Linien, vom Gipfel nach links und rechts abwärts. Der Berg steht hinten, klein.',
      '3. Schneegrenze als Zickzack quer über den Berg.',
      '4. Zipfelbob: flache Platte mit hochgebogener Spitze vorn. Er liegt parallel zum Hang!',
      '5. Kind: Rumpf als Oval, Kopf als Kreis, Mütze mit Bommel, Beine vorn aufs Bob, Arm zur Leine.',
      '6. ☀ Licht oben links: Schatten rechts am Berg, rechts am Kind, am Bob und im Schnee dahinter.',
      '7. Zum Schluss Spuren im Schnee und Tannen.',
    ],
    defs:
      `<clipPath id="bgS"><path d="${poly(shadeFace)}"/></clipPath>` +
      `<clipPath id="bgC"><path d="${poly(coreFace)}"/></clipPath>` +
      `<clipPath id="kTorso"><path d="${TORSO}"/></clipPath>` +
      '<clipPath id="kRight"><rect x="-62" y="-300" width="260" height="300"/></clipPath>' +
      '<clipPath id="kHead"><circle cx="-72" cy="-205" r="36"/></clipPath>' +
      `<clipPath id="bobS"><path d="${BOB}"/></clipPath>` +
      '<clipPath id="bobLow"><rect x="-200" y="-22" width="420" height="30"/></clipPath>' +
      `<clipPath id="kLeg"><path d="${LEGS}"/></clipPath>` +
      '<clipPath id="kLegLow"><rect x="-100" y="-52" width="260" height="30"/></clipPath>' +
      mask('mSn', W('<ellipse cx="1420" cy="1118" rx="230" ry="26" transform="rotate(9.65 1420 1118)"/>')),
    outline:
      `<path d="${mount.map((q, i) => (i ? 'L' : 'M') + q.join(' ')).join('')}"/>` +
      '<path d="M920 760L1600 760M0 860L1600 1132"/>' +
      '<path d="M322 430L375 480L425 440L480 495L535 450L590 505L640 470L680 470"/>' +
      '<path d="M480 260L462 320L500 370M400 340L420 395M550 330L560 385"/>' +
      tree(120, 885, 200) + tree(250, 903, 150) +
      '<path d="M560 975L950 1041M570 992L960 1058"/>' +
      kid(
        `<path d="${BOB}"/>` +
        '<path d="M62 -100Q130 -90 196 -66"/>' +
        `<path d="${LEGS}"/><ellipse cx="136" cy="-50" rx="24" ry="17"/>` +
        `<path d="${TORSO}"/>` +
        '<path d="M-60 -145Q0 -130 62 -108L58 -90Q0 -108 -62 -122"/><circle cx="64" cy="-99" r="10"/>' +
        '<circle cx="-72" cy="-205" r="36"/><path d="M-110 -208Q-72 -275 -34 -208Q-72 -218 -110 -208Z"/><circle cx="-75" cy="-250" r="13"/><circle cx="-50" cy="-203" r="3"/>',
        3.75),
    hatch:
      `<g clip-path="url(#bgS)">${hatch(62, 16)}</g><g clip-path="url(#bgC)">${hatch(-30, 16)}</g>` +
      `<g mask="url(#mSn)">${hatch(9.65, 10)}</g>` +
      kid(
        `<g clip-path="url(#kTorso)"><g clip-path="url(#kRight)">${hatch(60, 6, 0, -100, 200)}</g></g>` +
        `<g clip-path="url(#kHead)"><g clip-path="url(#kRight)">${hatch(60, 5, -72, -205, 60)}</g></g>` +
        `<g clip-path="url(#kLeg)"><g clip-path="url(#kLegLow)">${hatch(0, 5, 20, -50, 140)}</g></g>` +
        `<g clip-path="url(#bobS)"><g clip-path="url(#bobLow)">${hatch(0, 4, 0, -15, 260)}</g></g>`,
        1.9) + sun,
  });
})();
