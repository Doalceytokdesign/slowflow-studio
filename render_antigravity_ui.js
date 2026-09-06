const puppeteer = require('puppeteer');
const path = require('path');

const htmlContent = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1600px;
    height: 1050px;
    background: #0d0f14;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* TOP BAR */
  .topbar {
    height: 38px;
    background: #151821;
    display: flex;
    align-items: center;
    padding: 0 16px;
    border-bottom: 1px solid #232736;
    font-size: 12px;
    user-select: none;
  }
  .mac-dots {
    display: flex;
    gap: 8px;
    margin-right: 20px;
  }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot-red { background: #ff5f56; }
  .dot-yellow { background: #ffbd2e; }
  .dot-green { background: #27c93f; }

  .title {
    flex: 1;
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  .title strong { color: #f8fafc; font-weight: 600; }
  .badge-pt {
    background: #1e293b;
    color: #38bdf8;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    border: 1px solid #334155;
  }

  /* MAIN WORKSPACE */
  .workspace {
    flex: 1;
    display: flex;
    overflow: hidden;
  }

  /* ACTIVITY BAR */
  .activity-bar {
    width: 52px;
    background: #11141c;
    border-right: 1px solid #232736;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px 0;
    gap: 22px;
  }
  .logo-ai {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #6366f1, #06b6d4);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    color: #fff;
    font-size: 16px;
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.5);
    margin-bottom: 8px;
  }
  .act-icon {
    width: 22px;
    height: 22px;
    color: #64748b;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  .act-icon.active {
    color: #38bdf8;
    position: relative;
  }
  .act-icon.active::before {
    content: "";
    position: absolute;
    left: -15px;
    top: -2px;
    bottom: -2px;
    width: 3px;
    background: #38bdf8;
    border-radius: 0 2px 2px 0;
  }

  /* SIDEBAR EXPLORER */
  .sidebar {
    width: 240px;
    background: #13161f;
    border-right: 1px solid #232736;
    display: flex;
    flex-direction: column;
  }
  .sidebar-header {
    padding: 12px 16px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94a3b8;
    font-weight: 700;
    border-bottom: 1px solid #1e293b;
  }
  .file-tree {
    padding: 10px 0;
    font-size: 13px;
    font-family: 'JetBrains Mono', monospace, Consolas;
    line-height: 2.1;
  }
  .tree-item {
    padding: 0 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: #94a3b8;
  }
  .tree-item.active {
    background: #1e2433;
    color: #f8fafc;
    border-left: 2px solid #38bdf8;
  }
  .tree-item.indent { padding-left: 32px; }
  .tree-item.indent-2 { padding-left: 48px; }
  .icon-folder { color: #f59e0b; }
  .icon-py { color: #38bdf8; }
  .icon-css { color: #38bdf8; }
  .icon-html { color: #f97316; }
  .icon-img { color: #a855f7; }

  /* CODE EDITOR (CENTER) */
  .editor {
    flex: 1;
    background: #0d0f14;
    display: flex;
    flex-direction: column;
    border-right: 1px solid #232736;
  }
  .editor-tabs {
    height: 38px;
    background: #13161f;
    display: flex;
    border-bottom: 1px solid #232736;
  }
  .tab {
    padding: 0 18px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-family: 'JetBrains Mono', monospace;
    color: #64748b;
    border-right: 1px solid #232736;
    background: #11141c;
  }
  .tab.active {
    background: #0d0f14;
    color: #f8fafc;
    border-top: 2px solid #38bdf8;
  }
  .code-area {
    flex: 1;
    padding: 20px;
    font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
    font-size: 13px;
    line-height: 1.8;
    overflow: hidden;
  }
  .line { display: flex; }
  .ln { width: 36px; color: #475569; text-align: right; margin-right: 20px; user-select: none; }
  .c-kw { color: #ec4899; }
  .c-fn { color: #38bdf8; }
  .c-str { color: #4ade80; }
  .c-cmt { color: #64748b; font-style: italic; }
  .c-num { color: #f59e0b; }
  .c-prop { color: #c084fc; }

  /* TERMINAL AT BOTTOM OF EDITOR */
  .terminal-panel {
    height: 230px;
    background: #0a0c10;
    border-top: 1px solid #232736;
    display: flex;
    flex-direction: column;
  }
  .term-header {
    height: 30px;
    background: #13161f;
    padding: 0 16px;
    display: flex;
    align-items: center;
    gap: 16px;
    font-size: 11px;
    color: #94a3b8;
    border-bottom: 1px solid #232736;
  }
  .term-tab.active { color: #f8fafc; font-weight: 600; }
  .term-body {
    padding: 12px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    line-height: 1.7;
    color: #cbd5e1;
  }
  .t-prompt { color: #38bdf8; }
  .t-ok { color: #4ade80; font-weight: bold; }
  .t-url { color: #a855f7; text-decoration: underline; }

  /* ANTIGRAVITY AI AGENT PANEL (RIGHT) */
  .ai-panel {
    width: 440px;
    background: #13161f;
    display: flex;
    flex-direction: column;
  }
  .ai-header {
    padding: 12px 18px;
    background: #171b26;
    border-bottom: 1px solid #232736;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .ai-brand {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .ai-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 10px #10b981;
  }
  .ai-name {
    font-size: 13px;
    font-weight: 700;
    color: #f8fafc;
  }
  .ai-sub {
    font-size: 10px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .ai-chat {
    flex: 1;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    overflow: hidden;
  }
  .bubble {
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 12.5px;
    line-height: 1.6;
  }
  .bubble-user {
    background: #1e2433;
    border: 1px solid #334155;
    color: #f1f5f9;
    align-self: flex-end;
    max-width: 90%;
  }
  .bubble-ai {
    background: #181d2a;
    border: 1px solid #2b354c;
    color: #e2e8f0;
    align-self: flex-start;
    max-width: 100%;
    position: relative;
  }
  .ai-pill {
    display: inline-block;
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
    margin-bottom: 6px;
  }
  .action-box {
    margin-top: 10px;
    background: #0f121a;
    border: 1px solid #232a3b;
    border-radius: 6px;
    padding: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #94a3b8;
  }
  .action-box strong { color: #4ade80; }

  /* STATUS BAR AT BOTTOM */
  .statusbar {
    height: 24px;
    background: #0a0c10;
    border-top: 1px solid #1e2433;
    display: flex;
    align-items: center;
    padding: 0 16px;
    font-size: 11px;
    color: #64748b;
    justify-content: space-between;
  }
  .status-left { display: flex; gap: 16px; align-items: center; }
  .status-right { display: flex; gap: 16px; }
  .st-git { color: #38bdf8; display: flex; align-items: center; gap: 4px; }
</style>
</head>
<body>

  <!-- BARRA SUPERIOR -->
  <div class="topbar">
    <div class="mac-dots">
      <div class="dot dot-red"></div>
      <div class="dot dot-yellow"></div>
      <div class="dot dot-green"></div>
    </div>
    <div class="title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/></svg>
      <strong>Antigravity Studio</strong> &mdash; SlowFlow_Studio &mdash; main*
      <span class="badge-pt">PORTUGUÊS (BRASIL)</span>
    </div>
    <div style="font-size:11px;color:#64748b;font-weight:600;">v2.6.4 AI Engine</div>
  </div>

  <div class="workspace">
    <!-- BARRA DE ATIVIDADES -->
    <div class="activity-bar">
      <div class="logo-ai">A</div>
      <div class="act-icon active">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-6l-2-2H5a2 2 0 0 0-2 2z"/></svg>
      </div>
      <div class="act-icon">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      </div>
      <div class="act-icon">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
      </div>
      <div class="act-icon" style="margin-top:auto;">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
      </div>
    </div>

    <!-- SIDEBAR ARQUIVOS -->
    <div class="sidebar">
      <div class="sidebar-header">Explorador &bull; Slow Flow</div>
      <div class="file-tree">
        <div class="tree-item"><span class="icon-folder">&#9662;</span> <strong>SlowFlow_Studio</strong></div>
        <div class="tree-item indent"><span class="icon-folder">&#9662;</span> assets</div>
        <div class="tree-item indent-2"><span class="icon-folder">&#9656;</span> cards (60 webp)</div>
        <div class="tree-item indent-2"><span class="icon-img">&#9632;</span> editorial-web.webp</div>
        <div class="tree-item indent-2"><span class="icon-img">&#9632;</span> editorial-brand.webp</div>
        <div class="tree-item indent"><span class="icon-folder">&#9662;</span> src</div>
        <div class="tree-item indent-2"><span class="icon-css">#</span> input.css</div>
        <div class="tree-item indent active"><span class="icon-py">&lang;&rang;</span> build.py</div>
        <div class="tree-item indent"><span class="icon-html">&lt;&gt;</span> index.html</div>
        <div class="tree-item indent"><span class="icon-py">{}</span> data/images.json</div>
        <div class="tree-item indent"><span class="icon-html">{}</span> vercel.json</div>
      </div>
    </div>

    <!-- EDITOR CENTRAL -->
    <div class="editor">
      <div class="editor-tabs">
        <div class="tab active"><span class="icon-py">&lang;&rang;</span> build.py &times;</div>
        <div class="tab"><span class="icon-css">#</span> input.css</div>
        <div class="tab"><span class="icon-html">&lt;&gt;</span> index.html</div>
      </div>
      <div class="code-area">
        <div class="line"><span class="ln">1</span><span class="c-cmt"># Antigravity Studio Engine &mdash; Otimiza&ccedil;&atilde;o Mobile Extrema (GPU 60 FPS)</span></div>
        <div class="line"><span class="ln">2</span><span class="c-kw">import</span> json, os, subprocess</div>
        <div class="line"><span class="ln">3</span></div>
        <div class="line"><span class="ln">4</span><span class="c-kw">def</span> <span class="c-fn">calibrate_mobile_gpu</span>():</div>
        <div class="line"><span class="ln">5</span>    <span class="c-cmt"># Or&ccedil;amento de 12 cards ativos no celular: 80% menos mem&oacute;ria de v&iacute;deo</span></div>
        <div class="line"><span class="ln">6</span>    active_cards = <span class="c-num">12</span></div>
        <div class="line"><span class="ln">7</span>    cycle_duration = <span class="c-str">"1.2s"</span></div>
        <div class="line"><span class="ln">8</span>    step_delay     = <span class="c-str">"0.10s"</span>  <span class="c-cmt"># 12 cards x 0.1s = ciclo cont&iacute;nuo sem travar</span></div>
        <div class="line"><span class="ln">9</span></div>
        <div class="line"><span class="ln">10</span>    <span class="c-kw">return</span> {</div>
        <div class="line"><span class="ln">11</span>        <span class="c-prop">"fps_target"</span>: <span class="c-str">"60-120 FPS ProMotion"</span>,</div>
        <div class="line"><span class="ln">12</span>        <span class="c-prop">"mobile_freeze"</span>: <span class="c-kw">False</span>,</div>
        <div class="line"><span class="ln">13</span>        <span class="c-prop">"instant_click"</span>: <span class="c-kw">True</span>,</div>
        <div class="line"><span class="ln">14</span>        <span class="c-prop">"platform"</span>: <span class="c-str">"Slow Flow Digital Ecosystems"</span></div>
        <div class="line"><span class="ln">15</span>    }</div>
        <div class="line"><span class="ln">16</span></div>
        <div class="line"><span class="ln">17</span><span class="c-fn">print</span>(<span class="c-str">"[OK] Sistema Antigravity sincronizado com Vercel Edge."</span>)</div>
      </div>

      <!-- TERMINAL -->
      <div class="terminal-panel">
        <div class="term-header">
          <span class="term-tab active">TERMINAL</span>
          <span class="term-tab">SAÍDA (OUTPUT)</span>
          <span class="term-tab">AGENT LOGS</span>
        </div>
        <div class="term-body">
          <div><span class="t-prompt">PS C:\SlowFlow_Studio&gt;</span> python build.py</div>
          <div>  Compilando Tailwind CSS com aceleração GPU...</div>
          <div>  CSS compilado -&gt; dist/output.css (12.9 KB)</div>
          <div>  <span class="t-ok">[OK]</span> Build concluído! Loop móvel estabilizado em 1.2s</div>
          <div><span class="t-prompt">PS C:\SlowFlow_Studio&gt;</span> git push origin main</div>
          <div>  To github.com/Doalceytokdesign/slowflow-studio.git &mdash; <span class="t-ok">DEPLOY ATIVO</span></div>
          <div>  URL de Produção: <span class="t-url">https://slowflow-studio.vercel.app</span> (200 OK)</div>
        </div>
      </div>
    </div>

    <!-- PAINEL DO AGENTE ANTIGRAVITY (DIREITA) -->
    <div class="ai-panel">
      <div class="ai-header">
        <div class="ai-brand">
          <div class="ai-dot"></div>
          <div>
            <div class="ai-name">Antigravity AI Agent</div>
            <div class="ai-sub">DeepMind Advanced Assistant &bull; Ativo</div>
          </div>
        </div>
        <span class="badge-pt" style="background:#059669;color:#fff;border:none;">ONLINE</span>
      </div>

      <div class="ai-chat">
        <div class="bubble bubble-user">
          <strong>Usuário:</strong><br>
          "Quero que nesse card apareça na tela do computador a tela do Antigravity rodando para ter uma experiência imersiva, em português!"
        </div>

        <div class="bubble bubble-ai">
          <span class="ai-pill">&#10022; ANTIGRAVITY AGENT</span>
          <div>
            Com certeza! Conectando a interface do <strong>Antigravity Studio</strong> diretamente na tela do laptop com mapeamento em perspectiva 3D sub-pixel.
          </div>
          <div class="action-box">
            <div>&check; Mapeamento de Perspectiva: <strong>4 Pontos LCD OK</strong></div>
            <div>&check; Idioma: <strong>Português (Brasil)</strong></div>
            <div>&check; Resolução Retina: <strong>Alta Nitidez</strong></div>
            <div>&check; Experiência Imersiva: <strong>Ativada</strong></div>
          </div>
        </div>

        <div class="bubble bubble-ai" style="border-left: 3px solid #10b981;">
          <div style="color:#4ade80;font-weight:600;margin-bottom:4px;">&bull; Status da Operação</div>
          Tela renderizada e integrada com sucesso na cena editorial do Slow Flow Studio.
        </div>
      </div>
    </div>
  </div>

  <!-- STATUSBAR INFERIOR -->
  <div class="statusbar">
    <div class="status-left">
      <span class="st-git">&#9679; main*</span>
      <span>&uarr; 0 &darr; 0</span>
      <span>UTF-8</span>
      <span>Python 3.12</span>
    </div>
    <div class="status-right">
      <span>Antigravity Pair Programming</span>
      <span style="color:#4ade80;">&bull; 100% Conectado</span>
    </div>
  </div>

</body>
</html>`;

async function main() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 1050, deviceScaleFactor: 2 });
  await page.setContent(htmlContent, { waitUntil: 'networkidle0' });
  const outPath = path.join(__dirname, 'antigravity_screen.png');
  await page.screenshot({ path: outPath });
  await browser.close();
  console.log('antigravity_screen.png gerado com sucesso em:', outPath);
}

main().catch(err => {
  console.error('ERRO:', err);
  process.exit(1);
});
