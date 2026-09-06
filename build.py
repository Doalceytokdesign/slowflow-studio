#!/usr/bin/env python3
"""
=============================================================================
  SLOW FLOW STUDIO — Python Build System
  Gera index.html dinamicamente a partir de data/images.json
  Compila Tailwind CSS e sobe servidor local de preview
=============================================================================
"""

import json, os, sys, subprocess, shutil
from pathlib import Path
from datetime import datetime

ROOT        = Path(__file__).parent
DATA_FILE   = ROOT / "data" / "images.json"
OUTPUT_HTML = ROOT / "index.html"
CSS_INPUT   = ROOT / "src" / "input.css"
CSS_OUTPUT  = ROOT / "dist" / "output.css"
PORT        = 3000

# ── CALIBRACAO DE VELOCIDADE FLASH CINEMATOGRAFICA ─────────────────────────
# 60 cards x 0.02s (20ms por imagem) = 1.2s por ciclo completo
# 50 fps estroboscopicos estaveis e perfeitamente sincronizados com telas 60Hz/120Hz
CARD_DURATION = "1.2s"
CARD_DELAY    = "0.02s"

def load_images():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["images"]

def render_cards(images):
    lines = ["      <!-- ===== 60 CARDS CINEMATOGRAFICOS (ULTRA INSTANT HYDRATION) ===== -->"]
    for img in images:
        i, src, alt = img["i"], img["src"], img["alt"]
        niche = img.get("niche", "Design")
        if i < 15:
            # Primeiros 15 frames baixados imediatamente para inicializacao instantanea
            img_tag = (
                f'<img src="{src}" alt="{alt}" loading="eager" decoding="async" fetchpriority="high" '
                f'onerror="this.onerror=null;this.src=\'assets/casa-concreto.webp\';">'
            )
        else:
            # Frames 15-59 hidratados em segundo plano apos o primeiro frame renderizar
            img_tag = (
                f'<img src="" data-src="{src}" alt="{alt}" loading="lazy" decoding="async" '
                f'onerror="this.onerror=null;this.src=\'assets/casa-concreto.webp\';">'
            )
        lines.append(
            f'      <div class="halo-card" style="--i:{i}" onclick="openLightbox(this)" '
            f'data-niche="{niche}" data-alt="{alt}" title="{niche}">{img_tag}</div>'
        )
    return "\n".join(lines)

def render_html(images, inline_css=""):
    cards_html = render_cards(images)
    now = datetime.now().strftime("%Y")
    template = """<!DOCTYPE html>
<html lang="pt-BR" style="background:#0a0a0a;color-scheme:dark;">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta name="description" content="Slow Flow Studio — Websites de Alta Conversao, Branding, Moodboards e Portfolio Premium">
  <meta name="theme-color" content="#0a0a0a">
  <meta name="color-scheme" content="dark">
  <meta name="apple-mobile-web-app-capable" content="yes">

  <!-- SEO & Social Meta -->
  <meta name="keywords" content="design studio, websites, landing pages, branding, identidade visual, moodboard, portfolio, Google Ads, Instagram, alta conversao">
  <meta property="og:title" content="Slow Flow Studio — Digital Ecosystems">
  <meta property="og:description" content="Websites de alta conversao no Google e Instagram. Branding completo: moodboards, identidade visual e portfolio premium.">

  <title>Slow Flow — Digital Ecosystems</title>

  <!-- Preload dos primeiros 3 frames para abertura em 0ms no celular -->
  <link rel="preload" as="image" href="assets/cards/card_00.webp" type="image/webp" fetchpriority="high">
  <link rel="preload" as="image" href="assets/cards/card_01.webp" type="image/webp" fetchpriority="high">
  <link rel="preload" as="image" href="assets/cards/card_02.webp" type="image/webp" fetchpriority="high">

  <!-- Fontes assincronas nao-bloqueadoras -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@400;700&display=swap">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@400;700&display=swap" media="print" onload="this.media='all'">

  <!-- CSS Inlinado com Zero Round-trip HTTP: Abre no primeiro clique -->
  <style>
{{INLINE_CSS}}
  </style>
</head>
<body style="background:#0a0a0a !important; background-image:none !important;">

  <!-- ═══════════════════════════════════════════════════════════════
       LIGHTBOX MODAL CINEMATOGRAFICO
       ═══════════════════════════════════════════════════════════════ -->
  <div id="lightbox" onclick="closeLightbox(event)">
    <div class="lightbox-content" onclick="event.stopPropagation()">
      <button class="lightbox-close" onclick="closeLightbox(event)" title="Fechar (Esc)">&times;</button>
      <img id="lightbox-img" src="" alt="" onerror="this.onerror=null;this.src='assets/casa-concreto.png';" />
      <div class="lightbox-caption">
        <span id="lightbox-niche" class="lightbox-niche">Slow Flow Studio</span>
        <span id="lightbox-alt" class="lightbox-alt">Visual Experience</span>
      </div>
    </div>
  </div>

  <!-- ═══════════════════════════════════════════════════════════════
       HERO — PENDULUM FLOW 3D
       ═══════════════════════════════════════════════════════════════ -->
  <section class="world-container">

    <div class="corner-text top-left hidden md:block">
      SLOW FLOW STUDIO<br>PREMIUM DESIGN &amp; WEB
    </div>
    <div class="corner-text top-right">
      S-FLOW // {{YEAR}}<br>AESTHETICS &amp; CONVERSION
    </div>
    <div class="corner-text bottom-left hidden md:block">
      DIGITAL EXPERIENCES<br>BRAND ARCHITECTURE
    </div>
    <div class="corner-text bottom-right hidden md:block">
      FULLY RESPONSIVE<br>DATA-DRIVEN<br>OPTIMIZED PERFORMANCE
    </div>

    <div class="world-wrap">

      <!-- LOGO — BOLINHAS BRANCAS ACETINADAS (3D PEARL) -->
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
            <!-- Sombra vetorizada de alto desempenho: zero processamento de filtro -->
            <pattern id="satinDots" x="0" y="0" width="16" height="16" patternUnits="userSpaceOnUse">
              <circle cx="4.6" cy="4.8" r="3.6" fill="#000000" opacity="0.45"/>
              <circle cx="4" cy="4" r="3.6" fill="url(#pearl)"/>
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

{{CARDS_HTML}}

    </div>
  </section>

  <!-- ═══════════════════════════════════════════════════════════════
       EDITORIAL 01 — WEBSITES & LANDING PAGES
       ═══════════════════════════════════════════════════════════════ -->
  <section class="editorial-section">
    <div style="max-width:80rem;margin:0 auto;width:100%;padding:0 2rem;">
      <div class="editorial-grid-2">
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
        <div style="aspect-ratio:4/3;background:#111;overflow:hidden;position:relative;border-radius:6px;cursor:pointer;border:1px solid rgba(255,255,255,0.08);"
             onclick="openEditorialLightbox(this)" data-niche="01 // WEBSITES & LANDING PAGES" data-alt="Alta Conversão no Google e Instagram">
          <img src="https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1200&auto=format&fit=crop"
            alt="Websites Alta Conversao"
            style="width:100%;height:100%;object-fit:cover;filter:grayscale(100%);transition:filter 0.7s,transform 0.7s;"
            onmouseover="this.style.filter='grayscale(0%)';this.style.transform='scale(1.05)';"
            onmouseout="this.style.filter='grayscale(100%)';this.style.transform='scale(1)';"
            onerror="this.onerror=null;this.src='assets/casa-concreto.webp';">
        </div>
      </div>
    </div>
  </section>

  <!-- ═══════════════════════════════════════════════════════════════
       EDITORIAL 02 — BRANDING COMPLETO
       ═══════════════════════════════════════════════════════════════ -->
  <section class="editorial-section alt">
    <div style="max-width:80rem;margin:0 auto;width:100%;padding:0 2rem;">
      <div class="editorial-grid-2">
        <div style="aspect-ratio:4/3;background:#111;overflow:hidden;position:relative;border-radius:6px;cursor:pointer;border:1px solid rgba(255,255,255,0.08);"
             onclick="openEditorialLightbox(this)" data-niche="02 // BRANDING & IDENTIDADE" data-alt="Moodboards, Identidade Visual e Portfolio Completo">
          <img src="https://images.unsplash.com/photo-1600132806370-bf17e65e942f?q=80&w=1200&auto=format&fit=crop"
            alt="Branding Identidade Visual"
            style="width:100%;height:100%;object-fit:cover;filter:grayscale(100%);transition:filter 0.7s,transform 0.7s;"
            onmouseover="this.style.filter='grayscale(0%)';this.style.transform='scale(1.05)';"
            onmouseout="this.style.filter='grayscale(100%)';this.style.transform='scale(1)';"
            onerror="this.onerror=null;this.src='assets/cozinha-luxo.webp';">
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
       EDITORIAL 03 — FULL SERVICE STUDIO
       ═══════════════════════════════════════════════════════════════ -->
  <section class="editorial-section">
    <div style="max-width:80rem;margin:0 auto;width:100%;padding:0 2rem;">
      <div style="margin-bottom:4rem;">
        <span class="editorial-label" style="font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.12em;display:block;margin-bottom:1rem;">
          03 // Full Service Studio
        </span>
        <h2 class="editorial-title" style="font-family:'Inter',sans-serif;font-weight:900;font-size:clamp(2rem,4vw,3.5rem);text-transform:uppercase;letter-spacing:-0.03em;line-height:1;margin-bottom:0;">
          Tudo que sua marca precisa.<br>
          <span style="color:rgba(255,255,255,0.3);">Em um studio de alta tecnologia.</span>
        </h2>
      </div>
      <div class="editorial-grid-3">
        <div style="background:#111;padding:2.5rem;border-left:1px solid rgba(255,255,255,0.06);">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;">01</div>
          <h3 style="color:#f0f0f0;font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:-0.01em;">Websites &amp; Landing Pages</h3>
          <p style="color:rgba(255,255,255,0.5);font-size:0.875rem;line-height:1.7;margin:0;">Páginas otimizadas para Google, Instagram Ads e alta conversão. Mobile-first, ultrarrápidas.</p>
        </div>
        <div style="background:#111;padding:2.5rem;border-left:1px solid rgba(255,255,255,0.06);">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;">02</div>
          <h3 style="color:#f0f0f0;font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:-0.01em;">Branding &amp; Moodboards</h3>
          <p style="color:rgba(255,255,255,0.5);font-size:0.875rem;line-height:1.7;margin:0;">Logo, moodboard, identidade visual, manual de marca, paleta e tipografia premium.</p>
        </div>
        <div style="background:#111;padding:2.5rem;border-left:1px solid rgba(255,255,255,0.06);">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;">03</div>
          <h3 style="color:#f0f0f0;font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:-0.01em;">Portfólio Digital</h3>
          <p style="color:rgba(255,255,255,0.5);font-size:0.875rem;line-height:1.7;margin:0;">Sites de portfólio interativos para profissionais, arquitetos, fotógrafos e studios criativos.</p>
        </div>
      </div>
      <div style="margin-top:4rem;text-align:center;">
        <a href="https://wa.me/5544991244282" class="btn-light" style="font-size:11px;padding:1.2rem 3rem;">
          Falar com um Especialista &rarr;
        </a>
      </div>
    </div>
  </section>

  <!-- ═══════════════════════════════════════════════════════════════
       SCRIPTS LIGHTBOX & INTERATIVIDADE
       ═══════════════════════════════════════════════════════════════ -->
  <script>
    const lightbox     = document.getElementById("lightbox");
    const lightboxImg  = document.getElementById("lightbox-img");
    const lightboxNiche= document.getElementById("lightbox-niche");
    const lightboxAlt  = document.getElementById("lightbox-alt");

    function openLightbox(cardEl) {
      const img = cardEl.querySelector("img");
      if (!img) return;

      const src   = img.currentSrc || img.src;
      const niche = cardEl.getAttribute("data-niche") || "Design Portfolio";
      const alt   = cardEl.getAttribute("data-alt") || img.alt || "Slow Flow Studio";

      lightboxImg.src = src;
      lightboxNiche.textContent = niche;
      lightboxAlt.textContent = alt;

      lightbox.classList.add("show");
      document.body.classList.add("lightbox-active");
    }

    function openEditorialLightbox(containerEl) {
      const img = containerEl.querySelector("img");
      if (!img) return;

      const src   = img.currentSrc || img.src;
      const niche = containerEl.getAttribute("data-niche") || "Slow Flow Studio";
      const alt   = containerEl.getAttribute("data-alt") || img.alt || "Editorial";

      lightboxImg.src = src;
      lightboxNiche.textContent = niche;
      lightboxAlt.textContent = alt;

      lightbox.classList.add("show");
      document.body.classList.add("lightbox-active");
    }

    function closeLightbox(event) {
      if (event) event.stopPropagation();
      lightbox.classList.remove("show");
      document.body.classList.remove("lightbox-active");
      setTimeout(() => {
        if (!lightbox.classList.contains("show")) {
          lightboxImg.src = "";
        }
      }, 200);
    }

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeLightbox();
    });

    // Ultra Instant Mobile Hydration Engine
    window.addEventListener('DOMContentLoaded', () => {
      const deferred = document.querySelectorAll('.halo-card img[data-src]');
      if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
          deferred.forEach(img => {
            const src = img.getAttribute('data-src');
            if (src) img.src = src;
          });
        }, { timeout: 600 });
      } else {
        setTimeout(() => {
          deferred.forEach(img => {
            const src = img.getAttribute('data-src');
            if (src) img.src = src;
          });
        }, 200);
      }
    });
  </script>
</body>
</html>"""
    return template.replace("{{CARDS_HTML}}", cards_html).replace("{{YEAR}}", now).replace("{{INLINE_CSS}}", inline_css)

def build_css():
    print("  Compilando Tailwind CSS com aceleracao GPU...")
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

def serve():
    import http.server, socketserver, threading, webbrowser

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

    os.chdir(ROOT)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\n  Slow Flow Studio — Servidor Python")
        print(f"  http://localhost:{PORT}")
        print(f"  Pressione Ctrl+C para parar\n")
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
        httpd.serve_forever()

def main():
    print(f"\n  SLOW FLOW STUDIO — Build System Python (Zero Jank / Full GPU)")
    print(f"  {'='*55}")

    images = load_images()
    print(f"  Imagens carregadas: {len(images)} em {len(set(x['niche'] for x in images))} nichos")

    css_ok = build_css()
    inline_css = ""
    if css_ok and CSS_OUTPUT.exists():
        inline_css = CSS_OUTPUT.read_text(encoding="utf-8")

    html = render_html(images, inline_css)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"  HTML gerado com CSS Inlinado: index.html ({len(html):,} bytes)")

    if css_ok:
        print(f"\n  [OK] Build concluido com sucesso!")
        print(f"  Loop: {CARD_DURATION} | Delay por frame: {CARD_DELAY}")

    if "--serve" in sys.argv:
        serve()

if __name__ == "__main__":
    main()
