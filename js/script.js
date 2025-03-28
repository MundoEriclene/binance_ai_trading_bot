const output = document.getElementById("output");
const typingSound = document.getElementById("typingSound");
const rodape = document.getElementById("rodape-glitch");
const manifestoLink = document.querySelector(".btn-manifesto");
const ghostKey = document.getElementById("ghost-key");

// Simulação de supply escasso
let supplyTotal = 1000000;
let supplyVisivel = 999001; // Ainda mais próximo do total
let contadorAtivo = false;
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

// Link do manifesto (baseado no horário do sistema)
const hora = new Date().getHours();
manifestoLink.href = hora >= 6 && hora < 18
  ? "assets/manifesto_dia.pdf"
  : "assets/manifesto_noite.pdf";

// Digitação dos textos
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

// Atualiza contador de forma realista
function atualizarContador() {
  if (!contadorEl) return;

  if (supplyVisivel < supplyTotal) {
    const incremento = Math.random() < 0.9 ? 1 : 0; // 90% chance de subir 1, 10% de nada
    supplyVisivel += incremento;

    contadorEl.textContent = `Supply: ${supplyVisivel.toLocaleString()} / 1.000.000`;

    // Diminui a velocidade conforme se aproxima do total
    const distancia = supplyTotal - supplyVisivel;
    const delay = Math.min(4000, 1000 + Math.random() * (distancia / 2));
    setTimeout(atualizarContador, delay);
  }
}

// Inicia tudo ao clicar
window.addEventListener("click", () => {
  if (!typingInProgress && !typingFinalizado) {
    typingInProgress = true;
    typingSound.volume = 0.3;
    typingSound.loop = true;

    typingSound.play().then(() => {
      typeNextCharacter();
    }).catch(() => {
      typeNextCharacter();
    });
  }

  if (typingFinalizado && !contadorAtivo) {
    contadorAtivo = true;
    atualizarContador();
  }
});

// Telegram visível
ghostKey.addEventListener("click", () => {
  window.open("https://t.me/blacknode1970", "_blank");
});

// Rodapé com frases glitch
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
