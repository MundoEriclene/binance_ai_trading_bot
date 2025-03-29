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

function typeNextCharacter() {
  if (messageIndex >= messages.length) return;

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

window.addEventListener("click", () => {
  // Iniciar som e digitação apenas depois do clique
  typingSound.volume = 0.3; // ajusta o volume conforme necessário
  typingSound.loop = true;
  typingSound.play().then(() => {
    // Quando som for liberado, iniciar digitação
    typeNextCharacter();
  }).catch(err => {
    console.error("Erro ao reproduzir o som:", err);
    typeNextCharacter(); // continua mesmo sem som
  });
});

  