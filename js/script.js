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
let supplyAtual = 4819;

// Atualiza o link do manifesto conforme o horário
const hora = new Date().getHours();
if (hora >= 6 && hora < 18) {
  manifestoLink.href = "assets/manifesto_dia.pdf";
} else {
  manifestoLink.href = "assets/manifesto_noite.pdf";
}

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

function atualizarContador() {
  if (supplyAtual < 10000) {
    supplyAtual += Math.floor(Math.random() * 2);
    contadorEl.textContent = `Supply: ${supplyAtual} / 10.000`;
    setTimeout(atualizarContador, 1500 + Math.random() * 1500);
  }
}

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

  if (typingFinalizado) {
    atualizarContador();
  }
});

ghostKey.addEventListener("click", () => {
  window.open("https://t.me/seu_grupo_telegram", "_blank");
});

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
