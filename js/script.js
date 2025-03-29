const output = document.getElementById("output");
const typingSound = document.getElementById("typingSound");
const rodape = document.getElementById("rodape-glitch");
const manifestoLink = document.querySelector(".btn-manifesto");

// Criar dinamicamente o contador
const contadorEl = document.createElement("div");
contadorEl.className = "contador-supply";
contadorEl.id = "contador";
document.body.appendChild(contadorEl);

// Simulação de supply
let supplyTotal = 1000000;
let supplyVisivel = 998001;
let contadorAtivo = false;

// Telegram oculto por clique triplo
const ghostKey = document.getElementById("ghost-key");
let ghostClickCount = 0;

// Frases da digitação
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

// Link do manifesto: dia/noite
const hora = new Date().getHours();
manifestoLink.href = hora >= 6 && hora < 18
  ? "assets/manifesto_dia.pdf"
  : "assets/manifesto_noite.pdf";

// Efeito de digitação
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

// Atualiza contador de supply
function atualizarContador() {
  if (supplyVisivel < supplyTotal) {
    supplyVisivel += Math.floor(Math.random() * 2);
    contadorEl.textContent = `Supply: ${supplyVisivel.toLocaleString()} / 1.000.000`;
    setTimeout(atualizarContador, 3000 + Math.random() * 2000);
  }
}

// Início via clique
window.addEventListener("click", () => {
  if (!typingInProgress && !typingFinalizado) {
    typingInProgress = true;
    typingSound.volume = 0.3;
    typingSound.loop = true;

    typingSound.play().then(() => {
      typeNextCharacter();
    }).catch(err => {
      typeNextCharacter();
    });
  }

  if (typingFinalizado && !contadorAtivo) {
    contadorAtivo = true;
    atualizarContador();
  }
});

// Clique oculto no ícone 🔗 = ativa Telegram após 3 toques
ghostKey.addEventListener("click", () => {
  ghostClickCount++;
  if (ghostClickCount >= 3) {
    window.open("https://t.me/seu_grupo_telegram", "_blank");
    ghostClickCount = 0;
  }
});

// Frases glitch do rodapé
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

