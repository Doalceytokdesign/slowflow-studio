const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const FFMPEG_PATH = "C:\\Users\\user\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-9.0.1-full_build\\bin\\ffmpeg.exe";
const OUTPUT_DIR = path.join(__dirname, 'export_frames');
const OUTPUT_VIDEO = path.join(__dirname, 'slowflow_instagram_9x16.mp4');

const WIDTH = 1080;
const HEIGHT = 1920;
const FPS = 30;
const DURATION_SEC = 6; // 5 voltas completas perfeitas de 1.2s
const TOTAL_FRAMES = FPS * DURATION_SEC; // 180 quadros

async function capture() {
  console.log(`[1/3] Iniciando captura de ${TOTAL_FRAMES} frames em 1080x1920 (9:16)...`);
  
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-web-security',
      `--window-size=${WIDTH},${HEIGHT}`
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  // Abre a pagina local
  await page.goto('http://localhost:3000', { waitUntil: 'networkidle0' });

  // Oculta tudo que nao for a Hero Section para foco absoluto no looping
  await page.evaluate(() => {
    document.querySelectorAll('.editorial-section, #lightbox').forEach(el => el.remove());
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
  });

  // Aguarda 1 segundo para garantir renderizacao dos assets
  await new Promise(r => setTimeout(r, 1000));

  console.log('[2/3] Gravando frames com sincronizacao milimetrica...');
  for (let f = 0; f < TOTAL_FRAMES; f++) {
    const framePath = path.join(OUTPUT_DIR, `frame_${String(f).padStart(4, '0')}.jpg`);
    await page.screenshot({ path: framePath, type: 'jpeg', quality: 95 });
    if (f % 30 === 0 || f === TOTAL_FRAMES - 1) {
      console.log(`  Frame ${f + 1}/${TOTAL_FRAMES} salvo (${Math.round(((f + 1) / TOTAL_FRAMES) * 100)}%)`);
    }
  }

  await browser.close();
  console.log('[3/3] Renderizando video MP4 via FFmpeg...');

  const ffmpeg = spawn(FFMPEG_PATH, [
    '-y',
    '-framerate', String(FPS),
    '-i', path.join(OUTPUT_DIR, 'frame_%04d.jpg'),
    '-c:v', 'libx264',
    '-profile:v', 'high',
    '-level', '4.2',
    '-pix_fmt', 'yuv420p',
    '-preset', 'slow',
    '-crf', '18',
    OUTPUT_VIDEO
  ]);

  ffmpeg.stdout.on('data', data => {});
  ffmpeg.stderr.on('data', data => {});

  ffmpeg.on('close', code => {
    if (code === 0) {
      console.log(`\nSUCESSO! Video gerado com sucesso:`);
      console.log(`Arquivo: ${OUTPUT_VIDEO}`);
      // Limpeza dos frames temporarios
      fs.rmSync(OUTPUT_DIR, { recursive: true, force: true });
      console.log(`Frames temporarios removidos. Pronto para postar no Instagram!`);
    } else {
      console.error(`Erro ao gerar MP4. Codigo: ${code}`);
    }
  });
}

capture().catch(err => {
  console.error('Erro na execucao:', err);
});
