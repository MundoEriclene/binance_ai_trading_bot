const output = document.getElementById("output");
const typingSound = document.getElementById("typingSound");

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

function typeNextCharacter() {
  if (messageIndex >= messages.length) {
    // Todas as mensagens foram digitadas — parar som
    typingSound.pause();
    typingSound.currentTime = 0;
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

// Iniciar digitação e som após clique
window.addEventListener("click", () => {
  if (typingInProgress) return; // Evita iniciar duas vezes

  typingInProgress = true;
  typingSound.volume = 0.3;
  typingSound.loop = true;

  typingSound.play().then(() => {
    typeNextCharacter();
  }).catch(err => {
    console.error("Erro ao tocar som:", err);
    typeNextCharacter();
  });
});
