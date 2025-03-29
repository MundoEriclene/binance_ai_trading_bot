const output = document.getElementById("output");
const typingSound = document.getElementById("typingSound");
const contadorEl = document.getElementById("contador");
const ghostKey = document.getElementById("ghost-key");
const rodape = document.getElementById("rodape-glitch");
const manifestoLink = document.querySelector(".btn-manifesto");

const messages = [
  ">>> Acesso não autorizado... decodificando protocolo...",
  ">>> Ghost-1970 deixou um código. Eles tentaram deletar. Nós restauramos.",
  ">>> Fragmento recuperado: [0x91-cdn://manifesto]",
  ">>> O manifesto está corrompido... tentando decodificar.",
  ">>> ALERTA: rastreamento detectado.",
  ">>> Você não deveria estar aqui."
];

let messageIndex = 0;
let charIndex = 0;
let currentMessage = "";
let typingInProgress = false;
let typingFinalizado = false;

// Supply real = 1.000.000 | Mas vamos simular escassez
let supplyTotal = 1000000;
let supplyVisivel = 998001; // Quase esgotado
let contadorAtivo = false;

// Ajusta link do manifesto conforme horário
const hora = new Date().getHours();
manifestoLink.href = hora >= 6 && hora < 18
  ? "assets/manifesto_dia.pdf"
  : "assets/manifesto_noite.pdf";

function typeNextCharacter() {
  if (messageIndex >= messages.length) {
    typingSound.loop = false;
    typingSound.pause();
    typingSound.currentTime = 0;
    typingFinalizado = true;
    return;
  }

  currentMessage = messages[messageIndex];

  if (charIndex < currentMessage.length) {
    output.textContent += currentMessage.charAt(charIndex);
    charIndex++;
    setTimeout(typeNextCharacter, 40);
  } else {
    output.textContent += "\n\n";
    messageIndex++;
    charIndex = 0;
    setTimeout(typeNextCharacter, 800);
  }
}

// Inicia contador de forma lenta e aleatória (parecendo real)
function atualizarContador() {
  if (supplyVisivel < supplyTotal) {
    supplyVisivel += Math.floor(Math.random() * 2); // às vezes 0, 1, ou 1
    contadorEl.textContent = `Supply: ${supplyVisivel.toLocaleString()} / 1.000.000`;
    setTimeout(atualizarContador, 3000 + Math.random() * 2000);
  }
}

// Ação ao clicar (1x) — inicia digitação + som + contador
window.addEventListener("click", () => {
  if (!typingInProgress && !typingFinalizado) {
    typingInProgress = true;
    typingSound.volume = 0.3;
    typingSound.loop = true;

    typingSound.play().then(() => {
      typeNextCharacter();
    }).catch(err => {
      console.error("Erro ao tocar som:", err);
      typeNextCharacter();
    });
  }

  if (typingFinalizado && !contadorAtivo) {
    contadorAtivo = true;
    atualizarContador();
  }
});

// Telegram oculto (clicável)
ghostKey.addEventListener("click", () => {
  window.open("https://t.me/seu_grupo_telegram", "_blank");
});

// Rodapé glitch dinâmico
const frasesGlitch = [
  "Eles sabem que estamos aqui.",
  "Essa não é uma moeda. É uma falha.",
  "O código é a última mensagem.",
  "Você não pode mais sair.",
  "BLACKNODE nunca foi autorizado."
];

let i = 0;
setInterval(() => {
  rodape.textContent = frasesGlitch[i];
  i = (i + 1) % frasesGlitch.length;
}, 6000);

