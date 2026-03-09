/* ═══════════════════════════════════════════════════════════════════
   STRIPBOARD.JS — Universal Production Slate Software
   ───────────────────────────────────────────────────────────────────
   A shared engine that renders a side-scrolling Kanban board for
   prestige-production slates. It knows nothing about biometrics
   or concrete — only how to render a slate based on the config
   object fed by the parent app (DUOMO or THAUMA).
   ═══════════════════════════════════════════════════════════════════ */
window.renderStripboard = function (container, config) {
  'use strict';

  /* ── inject styles once ── */
  var styleId = 'stripboard-styles';
  if (!document.getElementById(styleId)) {
    var style = document.createElement('style');
    style.id = styleId;
    style.textContent = [
      '.strip-root { font-family: system-ui, -apple-system, sans-serif; color: #f5f0e8; animation: strip-fadein 0.5s ease; padding-bottom: 3rem; }',
      '@keyframes strip-fadein { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }',

      '.strip-header { margin-bottom: 2rem; max-width: 900px; }',
      '.strip-title { font-family: Georgia, serif; font-size: clamp(1.8rem, 3vw, 2.4rem); margin-bottom: 0.75rem; font-weight: 300; letter-spacing: -0.02em; }',
      '.strip-thesis { font-size: 1rem; color: rgba(245,240,232,0.6); line-height: 1.6; }',

      '.manifesto-card { background: rgba(201,168,76,0.03); border: 1px solid rgba(201,168,76,0.15); padding: 1.5rem; border-radius: 12px; margin-bottom: 2.5rem; }',
      '.m-quote { padding-left: 1rem; font-style: italic; color: rgba(245,240,232,0.8); margin-bottom: 1rem; font-family: Georgia, serif; font-size: 1.1rem; }',
      '.m-desc { font-size: 0.9rem; color: rgba(245,240,232,0.6); line-height: 1.6; }',

      '.board-container { display: flex; gap: 1.5rem; overflow-x: auto; padding-bottom: 2rem; scroll-snap-type: x mandatory; }',
      '.board-container::-webkit-scrollbar { height: 6px; }',
      '.board-container::-webkit-scrollbar-track { background: rgba(201,168,76,0.05); border-radius: 4px; }',
      '.board-container::-webkit-scrollbar-thumb { background: rgba(201,168,76,0.3); border-radius: 4px; }',

      '.strip-col { flex: 0 0 340px; background: rgba(10,10,15,0.8); border: 1px solid rgba(201,168,76,0.12); border-radius: 12px; scroll-snap-align: start; display: flex; flex-direction: column; overflow: hidden; }',
      '.strip-col-header { padding: 1.5rem; background: rgba(201,168,76,0.04); border-bottom: 1px solid rgba(201,168,76,0.12); }',
      '.strip-col-id { font-family: "SF Mono", Consolas, monospace; font-size: 0.75rem; font-weight: bold; letter-spacing: 0.1em; margin-bottom: 0.5rem; }',
      '.strip-col-title { font-size: 1.3rem; font-weight: 600; color: #f5f0e8; margin-bottom: 0.5rem; }',
      '.strip-col-budget { font-family: "SF Mono", Consolas, monospace; font-size: 0.8rem; margin-bottom: 0.5rem; }',
      '.strip-col-thesis { font-size: 0.8rem; color: rgba(245,240,232,0.5); font-style: italic; line-height: 1.4; }',

      '.strip-event { display: grid; grid-template-columns: 45px 1fr; gap: 1rem; padding: 1.25rem 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.2s; }',
      '.strip-event:hover { background: rgba(201,168,76,0.05); }',
      '.strip-event:last-child { border-bottom: none; }',

      '.event-time { font-family: "SF Mono", Consolas, monospace; color: rgba(245,240,232,0.4); font-size: 0.75rem; font-weight: 600; padding-top: 3px; }',
      '.event-title { display: block; color: #f5f0e8; font-size: 0.9rem; font-weight: 600; margin-bottom: 6px; }',
      '.event-desc { display: block; color: rgba(245,240,232,0.6); font-size: 0.8rem; line-height: 1.5; margin-bottom: 12px; }',

      '.event-tags { display: flex; gap: 6px; flex-wrap: wrap; }',
      '.e-tag { padding: 3px 8px; border-radius: 4px; font-size: 0.65rem; font-family: "SF Mono", Consolas, monospace; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; border: 1px solid currentColor; }'
    ].join('\n');
    document.head.appendChild(style);
  }

  /* ── build HTML ── */
  var parts = [];

  parts.push(
    '<div class="strip-root">',
    '<div class="strip-header">',
    '<h1 class="strip-title" style="color: ' + config.themeColor + ';">' + config.title + '</h1>',
    '<p class="strip-thesis">' + config.thesis + '</p>',
    '</div>',
    '<div class="manifesto-card" style="border-color: ' + config.themeColor + '44; border-left: 4px solid ' + config.themeColor + ';">',
    '<div class="m-quote" style="border-left-color: ' + config.themeColor + ';">\u201c' + config.quote + '\u201d</div>',
    '<p class="m-desc">' + config.manifesto + '</p>',
    '</div>',
    '<div class="board-container">'
  );

  config.columns.forEach(function (col) {
    parts.push(
      '<div class="strip-col">',
      '<div class="strip-col-header" style="border-top: 4px solid ' + config.themeColor + ';">',
      '<div class="strip-col-id" style="color: ' + config.themeColor + ';">' + col.id + '</div>',
      '<div class="strip-col-title">' + col.title + '</div>',
      '<div class="strip-col-budget" style="color: ' + (config.budgetColor || '#4caf50') + ';">' + col.budget + '</div>',
      '<div class="strip-col-thesis">Thesis: ' + col.thesis + '</div>',
      '</div>'
    );
    col.events.forEach(function (ev) {
      var tagHtml = (ev.tags || []).map(function (t) {
        return '<span class="e-tag" style="color: ' + t.color + '; background: ' + t.color + '15;">' + t.label + '</span>';
      }).join('');
      parts.push(
        '<div class="strip-event">',
        '<div class="event-time">' + ev.time + '</div>',
        '<div>',
        '<span class="event-title">' + ev.title + '</span>',
        '<span class="event-desc">' + ev.desc + '</span>',
        '<div class="event-tags">' + tagHtml + '</div>',
        '</div>',
        '</div>'
      );
    });
    parts.push('</div>');
  });

  /* remaining-slots ghost column */
  var remaining = 10 - config.columns.length;
  parts.push(
    '<div class="strip-col" style="justify-content: center; align-items: center; border: 1px dashed rgba(255,255,255,0.1); background: transparent; opacity: 0.6;">',
    '<div style="font-family: \'SF Mono\', Consolas, monospace; color: rgba(245,240,232,0.4); text-align: center;">',
    '+ ' + remaining + ' Slots Remaining<br/>',
    '<span style="font-size: 0.7rem; margin-top: 8px; display: block;">IN DEVELOPMENT</span>',
    '</div>',
    '</div>'
  );

  parts.push('</div>', '</div>');

  container.innerHTML = parts.join('\n');
};
