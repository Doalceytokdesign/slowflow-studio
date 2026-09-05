#!/usr/bin/env python3
"""
=============================================================================
  SLOW FLOW STUDIO — Python Build System
  Gera index.html dinamicamente a partir de data/images.json
  Compila Tailwind CSS e sobe servidor local de preview

  Uso:
    python build.py          -> gera HTML + compila CSS
    python build.py --serve  -> gera + compila + sobe servidor na porta 3000
    python build.py --watch  -> modo dev com Tailwind em modo watch
=============================================================================
"""

import json, os, sys, subprocess, shutil
from pathlib import Path
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).parent
DATA_FILE   = ROOT / "data" / "images.json"
OUTPUT_HTML = ROOT / "index.html"
CSS_INPUT   = ROOT / "src" / "input.css"
CSS_OUTPUT  = ROOT / "dist" / "output.css"
PORT        = 3000

# ── ANIMACAO: EFEITO CINEMATOGRAFICO ────────────────────────────────────────
# 60 cards x 0.007s de delay = 0.42s de loop total
# Cada card passa pelo centro em ~7ms = efeito de pelicula em alta velocidade
CARD_DURATION = "0.42s"   # duracao total do loop halfPipe
CARD_DELAY    = "0.007s"  # intervalo entre cada card (7ms = pelicula rapida)

# ── CARREGA BASE DE DADOS ────────────────────────────────────────────────────
def load_images():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["images"]

# ── GERA BLOCO DE CARDS HTML ─────────────────────────────────────────────────
def render_cards(images):
    lines = ["      <!-- ===== 60 CARDS CINEMATOGRAFICOS — gerado por build.py ===== -->"]
    for img in images:
        i, src, alt = img["i"], img["src"], img["alt"]
        niche = img.get("niche", "")
        lines.append(
            f'      <div class="halo-card" style="--i:{i}" onclick="openImage(this)" title="{niche}">'
            f'<img src="{src}" alt="{alt}" loading="lazy"></div>'
        )
    return "\n".join(lines)

# ── GERA O HTML COMPLETO ─────────────────────────────────────────────────────
def render_html(images):
    cards_html = render_cards(images)
    now = datetime.now().strftime("%Y")
    return f"""<!DOCTYPE html>
<html lang="pt-BR" style="background:#0a0a0a;color-scheme:dark;">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta name="description" content="Slow Flow Studio — Websites de Alta Conversao, Branding, Moodboard e Portfolio Premium">
  <meta name="theme-color" content="#0a0a0a">
  <meta name="color-scheme" content="dark">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <!-- SEO -->
  <meta name="keywords" content="design studio, websites, landing pages, branding, identidade visual, moodboard, portfolio, Google Ads, Instagram, alta conversao">
  <meta property="og:title" content="Slow Flow Studio — Digital Ecosystems">
  <meta property="og:description" content="Websites de alta conversao no Google e Instagram. Branding completo: moodboard, identidade visual e portfolio premium.">

  <title>Slow Flow — Digital Ecosystems</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="dist/output.css">

  <style>
    html, body {{
      background: #0a0a0a !important;
      background-color: #0a0a0a !important;
      background-image: none !important;
      color: #f0f0f0 !important;
      margin: 0;
    }}
    .world-container {{ background: #0a0a0a !important; }}
  </style>
</head>
<body style="background:#0a0a0a !important; background-image:none !important;">

  <!-- LIGHTBOX -->
  <div id="lightbox" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.96);z-index:9999;align-items:center;justify-content:center;cursor:pointer;" onclick="closeLightbox()">
    <img id="lightbox-img" src="" style="max-height:85vh;max-width:95vw;border-radius:6px;box-shadow:0 40px 100px rgba(0,0,0,0.9);object-fit:contain;" />
  </div>

  <!-- ═══════════════════════════════════════════════════════════════
       HERO — CINEMATIC PENDULUM FLOW
       {len(images)} cards | Loop: {CARD_DURATION} | Delay: {CARD_DELAY}/card
       ═══════════════════════════════════════════════════════════════ -->
  <section class="world-container">

    <div class="corner-text top-left hidden md:block">
      SLOW FLOW STUDIO<br>PREMIUM DESIGN &amp; WEB
    </div>
    <div class="corner-text top-right">
      S-FLOW // {now}<br>AESTHETICS &amp; CONVERSION
    </div>
    <div class="corner-text bottom-left hidden md:block">
      DIGITAL EXPERIENCES<br>BRAND ARCHITECTURE
    </div>
    <div class="corner-text bottom-right hidden md:block">
      FULLY RESPONSIVE<br>DATA-DRIVEN<br>OPTIMIZED PERFORMANCE
    </div>

    <div class="world-wrap">

      <!-- LOGO — BOLINHAS BRANCAS ACETINADAS -->
      <div class="center-logo-3d">
        <svg width="100%" height="100%" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="pearl" cx="32%" cy="28%" r="68%" fx="32%" fy="28%">
              <stop offset="0%"   stop-color="#ffffff" stop-opacity="1"/>
              <stop offset="25%"  stop-color="#f0f0f0" stop-opacity="1"/>
              <stop offset="55%"  stop-color="#c0c0c0" stop-opacity="1"/>
              <stop offset="80%"  stop-color="#888888" stop-opacity="1"/>
              <stop offset="100%" stop-color="#444444" stop-opacity="0.9"/>
            </radialGradient>
            <radialGradient id="sheen" cx="30%" cy="25%" r="35%">
              <stop offset="0%"   stop-color="#ffffff" stop-opacity="0.95"/>
              <stop offset="60%"  stop-color="#ffffff" stop-opacity="0.2"/>
              <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
            </radialGradient>
            <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
              <feDropShadow dx="0.4" dy="0.8" stdDeviation="0.8" flood-color="#000000" flood-opacity="0.6"/>
            </filter>
            <pattern id="satinDots" x="0" y="0" width="16" height="16" patternUnits="userSpaceOnUse">
              <circle cx="4" cy="4" r="3.6" fill="url(#pearl)" filter="url(#shadow)"/>
              <circle cx="4" cy="4" r="3.6" fill="url(#sheen)"/>
            </pattern>
          </defs>
          <text x="50%" y="35%" text-anchor="middle" dominant-baseline="central"
            font-family="'Inter', sans-serif" font-weight="900" font-size="160"
            fill="url(#satinDots)">SLOW</text>
          <text x="50%" y="85%" text-anchor="middle" dominant-baseline="central"
            font-family="'Inter', sans-serif" font-weight="900" font-size="160"
            fill="url(#satinDots)">FLOW</text>
        </svg>
      </div>

{cards_html}

    </div>
  </section>

  <!-- ═══════════════════════════════════════════════════════════════
       EDITORIAL 01 — WEBSITES & LANDING PAGES
       ═══════════════════════════════════════════════════════════════ -->
  <section class="editorial-section">
    <div style="max-width:80rem;margin:0 auto;width:100%;padding:0 2rem;">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6rem;align-items:center;">
        <div>
          <span class="editorial-label" style="font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.12em;display:block;margin-bottom:1.2rem;">
            01 // Digital Presence — Google &amp; Instagram
          </span>
          <h2 class="editorial-title" style="font-family:'Inter',sans-serif;font-weight:900;font-size:clamp(2.5rem,5.5vw,4.5rem);text-transform:uppercase;letter-spacing:-0.03em;line-height:0.95;margin-bottom:2rem;">
            Websites &amp;<br>Landing Pages<br><span style="color:rgba(255,255,255,0.35);font-size:0.65em;">de Alta Conversão.</span>
          </h2>
          <p class="editorial-body" style="font-size:1.05rem;line-height:1.75;margin-bottom:1.5rem;max-width:440px;">
            Dominamos o tráfego no <strong style="color:#f0f0f0;">Google</strong> e no <strong style="color:#f0f0f0;">Instagram</strong> com interfaces minimalistas de alta performance. Cada página é uma máquina de conversão — projetada para transformar visitantes em clientes.
          </p>
          <p class="editorial-body" style="font-size:1.05rem;line-height:1.75;margin-bottom:2.5rem;max-width:440px;">
            Arquitetamos ecossistemas digitais completos: landing pages, e-commerces, hotsites e sistemas web integrados ao seu CRM e métricas de negócio.
          </p>
          <a href="https://wa.me/5544991244282" class="btn-light">Iniciar Projeto Web &rarr;</a>
        </div>
        <div style="aspect-ratio:4/3;background:#111;overflow:hidden;position:relative;">
          <img src="https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1200&auto=format&fit=crop"
            alt="Websites Alta Conversao"
            style="width:100%;height:100%;object-fit:cover;filter:grayscale(100%);transition:filter 0.7s,transform 0.7s;"
            onmouseover="this.style.filter='grayscale(0%)';this.style.transform='scale(1.05)';"
            onmouseout="this.style.filter='grayscale(100%)';this.style.transform='scale(1)';">
        </div>
      </div>
    </div>
  </section>

  <!-- ═══════════════════════════════════════════════════════════════
       EDITORIAL 02 — BRANDING COMPLETO
       ═══════════════════════════════════════════════════════════════ -->
  <section class="editorial-section alt">
    <div style="max-width:80rem;margin:0 auto;width:100%;padding:0 2rem;">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6rem;align-items:center;">
        <div style="aspect-ratio:4/3;background:#111;overflow:hidden;position:relative;">
          <img src="https://images.unsplash.com/photo-1600132806370-bf17e65e942f?q=80&w=1200&auto=format&fit=crop"
            alt="Branding Identidade Visual"
            style="width:100%;height:100%;object-fit:cover;filter:grayscale(100%);transition:filter 0.7s,transform 0.7s;"
            onmouseover="this.style.filter='grayscale(0%)';this.style.transform='scale(1.05)';"
            onmouseout="this.style.filter='grayscale(100%)';this.style.transform='scale(1)';">
        </div>
        <div>
          <span class="editorial-label" style="font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.12em;display:block;margin-bottom:1.2rem;">
            02 // Visual Authority — Branding Completo
          </span>
          <h2 class="editorial-title" style="font-family:'Inter',sans-serif;font-weight:900;font-size:clamp(2.5rem,5.5vw,4.5rem);text-transform:uppercase;letter-spacing:-0.03em;line-height:0.95;margin-bottom:2rem;">
            Branding &amp;<br>Identidade<br><span style="color:rgba(255,255,255,0.35);font-size:0.65em;">Visual Completa.</span>
          </h2>
          <p class="editorial-body" style="font-size:1.05rem;line-height:1.75;margin-bottom:1.5rem;max-width:440px;">
            Do zero ao topo: criamos <strong style="color:#f0f0f0;">moodboards</strong>, <strong style="color:#f0f0f0;">identidade visual</strong>, <strong style="color:#f0f0f0;">portfólio digital</strong>, manual de marca, paleta de cores, tipografia, papelaria e todos os assets da sua marca.
          </p>
          <p class="editorial-body" style="font-size:1.05rem;line-height:1.75;margin-bottom:2.5rem;max-width:440px;">
            Marcas que lideram mercados são arquitetadas, não apenas desenhadas. Criamos sistemas visuais escaláveis que posicionam a sua empresa como a escolha óbvia do setor.
          </p>
          <a href="https://wa.me/5544991244282" class="btn-light">Construir Minha Marca &rarr;</a>
        </div>
      </div>
    </div>
  </section>

  <!-- ═══════════════════════════════════════════════════════════════
       EDITORIAL 03 — SERVICOS COMPLETOS
       ═══════════════════════════════════════════════════════════════ -->
  <section class="editorial-section">
    <div style="max-width:80rem;margin:0 auto;width:100%;padding:0 2rem;">
      <div style="margin-bottom:4rem;">
        <span class="editorial-label" style="font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.12em;display:block;margin-bottom:1rem;">
          03 // Full Service Studio
        </span>
        <h2 class="editorial-title" style="font-family:'Inter',sans-serif;font-weight:900;font-size:clamp(2rem,4vw,3.5rem);text-transform:uppercase;letter-spacing:-0.03em;line-height:1;margin-bottom:0;">
          Tudo que sua marca precisa.<br>
          <span style="color:rgba(255,255,255,0.3);">Em um studio.</span>
        </h2>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;">
        <div style="background:#111;padding:2.5rem;border-left:1px solid rgba(255,255,255,0.06);">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;">01</div>
          <h3 style="color:#f0f0f0;font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:-0.01em;">Websites &amp; Landing Pages</h3>
          <p style="color:rgba(255,255,255,0.5);font-size:0.875rem;line-height:1.7;margin:0;">Páginas otimizadas para Google, Instagram Ads e alta conversão. Mobile-first, ultrarrápidas.</p>
        </div>
        <div style="background:#111;padding:2.5rem;border-left:1px solid rgba(255,255,255,0.06);">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;">02</div>
          <h3 style="color:#f0f0f0;font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:-0.01em;">Branding Completo</h3>
          <p style="color:rgba(255,255,255,0.5);font-size:0.875rem;line-height:1.7;margin:0;">Logo, moodboard, identidade visual, manual de marca, paleta e tipografia premium.</p>
        </div>
        <div style="background:#111;padding:2.5rem;border-left:1px solid rgba(255,255,255,0.06);">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;">03</div>
          <h3 style="color:#f0f0f0;font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:-0.01em;">Portfólio Digital</h3>
          <p style="color:rgba(255,255,255,0.5);font-size:0.875rem;line-height:1.7;margin:0;">Sites de portfólio interativos para profissionais, arquitetos, fotógrafos e studios criativos.</p>
        </div>
        <div style="background:#111;padding:2.5rem;border-left:1px solid rgba(255,255,255,0.06);">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;">04</div>
          <h3 style="color:#f0f0f0;font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:-0.01em;">E-commerce Premium</h3>
          <p style="color:rgba(255,255,255,0.5);font-size:0.875rem;line-height:1.7;margin:0;">Lojas virtuais de alta performance integradas com pagamentos, ERP e logística.</p>
        </div>
        <div style="background:#111;padding:2.5rem;border-left:1px solid rgba(255,255,255,0.06);">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;">05</div>
          <h3 style="color:#f0f0f0;font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:-0.01em;">Social Media Design</h3>
          <p style="color:rgba(255,255,255,0.5);font-size:0.875rem;line-height:1.7;margin:0;">Templates para Instagram, LinkedIn e YouTube. Consistência visual que gera autoridade.</p>
        </div>
        <div style="background:#111;padding:2.5rem;border-left:1px solid rgba(255,255,255,0.06);">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;">06</div>
          <h3 style="color:#f0f0f0;font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:-0.01em;">Estratégia Digital</h3>
          <p style="color:rgba(255,255,255,0.5);font-size:0.875rem;line-height:1.7;margin:0;">SEO, Google Ads, Meta Ads e análise de dados. Tráfego qualificado que converte.</p>
        </div>
      </div>
      <div style="margin-top:4rem;text-align:center;">
        <a href="https://wa.me/5544991244282" class="btn-light" style="font-size:11px;padding:1.2rem 3rem;">
          Falar com um Especialista &rarr;
        </a>
      </div>
    </div>
  </section>

  <script>
    const lightbox    = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-img");
    function openImage(el) {{
      lightboxImg.src = el.querySelector("img").src;
      lightbox.style.display = "flex";
    }}
    function closeLightbox() {{
      lightbox.style.display = "none";
      lightboxImg.src = "";
    }}
    document.addEventListener("keydown", e => {{ if(e.key === "Escape") closeLightbox(); }});
  </script>
</body>
</html>"""

# ── COMPILA TAILWIND CSS ─────────────────────────────────────────────────────
def build_css():
    print("  Compilando Tailwind CSS...")
    npx_cmd = "npx.cmd" if sys.platform == "win32" else "npx"
    result = subprocess.run(
        [npx_cmd, "tailwindcss", "-i", str(CSS_INPUT), "-o", str(CSS_OUTPUT), "--minify"],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    if result.returncode != 0:
        print(f"  ERRO CSS: {result.stderr}")
        return False
    print(f"  CSS compilado -> dist/output.css")
    return True

# ── SERVIDOR LOCAL PYTHON ────────────────────────────────────────────────────
def serve():
    import http.server, socketserver, threading, webbrowser, time

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass  # silencia logs repetitivos

    os.chdir(ROOT)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\n  Slow Flow Studio — Servidor Python")
        print(f"  http://localhost:{PORT}")
        print(f"  Pressione Ctrl+C para parar\n")
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
        httpd.serve_forever()

# ── PONTO DE ENTRADA ─────────────────────────────────────────────────────────
def main():
    print(f"\n  SLOW FLOW STUDIO — Build System Python")
    print(f"  {'='*50}")

    images = load_images()
    print(f"  Imagens carregadas: {len(images)} em {len(set(x['niche'] for x in images))} nichos")

    html = render_html(images)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"  HTML gerado: index.html ({len(html):,} bytes)")

    css_ok = build_css()

    print(f"\n  Build concluido! Abra index.html no browser.")
    print(f"  Velocidade: {CARD_DURATION} loop | {CARD_DELAY} entre cards\n")

    if "--serve" in sys.argv:
        serve()

if __name__ == "__main__":
    main()

