const output = document.getElementById("output");
const typingSound = document.getElementById("typingSound");
const contadorEl = document.getElementById("contador");
const ghostKey = document.getElementById("ghost-key");
const rodape = document.getElementById("rodape-glitch");

const messages = [
  ">>> Acesso não autorizado... decodificando protocolo...",
  ">>> Ghost-91 deixou um código. Eles tentaram deletar. Nós restauramos.",
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
let supplyAtual = 4819;

function typeNextCharacter() {
  if (messageIndex >= messages.length) {
    // ✅ Final da digitação
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

function atualizarContador() {
  if (supplyAtual < 10000) {
    supplyAtual += Math.floor(Math.random() * 2);
    contadorEl.textContent = `Supply: ${supplyAtual} / 10.000`;
    setTimeout(atualizarContador, 1500 + Math.random() * 1500);
  }
}

window.addEventListener("click", () => {
  if (!typingInProgress && !typingFinalizado) {
    // Inicia som e digitação
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

  if (typingFinalizado) {
    atualizarContador();
  }
});

// Entrada oculta do Telegram
ghostKey.addEventListener("click", () => {
  window.open("https://t.me/seu_grupo_telegram", "_blank");
});

// Rodapé com frases glitch alternadas
const frasesGlitch = [
  "Eles sabem que estamos aqui.",
  "Essa não é uma moeda. É uma falha.",
  "O código é a última mensagem.",
  "Você não pode mais sair.",
  "Protocolo restaurado por Ghost-91."
];

let i = 0;
setInterval(() => {
  rodape.textContent = frasesGlitch[i];
  i = (i + 1) % frasesGlitch.length;
}, 6000);
