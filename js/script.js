const output = document.getElementById("output");
const typingSound = document.getElementById("typingSound");
const rodape = document.getElementById("rodape-glitch");
const manifestoLink = document.querySelector(".btn-manifesto");
const ghostKey = document.getElementById("ghost-key");

// Simulação de supply
let supplyTotal = 1000000;
let supplyVisivel = 998001;
let contadorAtivo = false;

// Criar dinamicamente o contador após digitação
let contadorEl = null;

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

    // Cria contador após finalização
    contadorEl = document.createElement("div");
    contadorEl.className = "contador-supply";
    contadorEl.id = "contador";
    contadorEl.textContent = `Supply: ${supplyVisivel.toLocaleString()} / 1.000.000`;
    document.body.appendChild(contadorEl);
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

// Atualiza contador lentamente após digitação
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

// Clique simples no 🔗 já leva ao Telegram
ghostKey.addEventListener("click", () => {
  window.open("https://t.me/blacknode1970", "_blank");
});

// Rodapé dinâmico
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


