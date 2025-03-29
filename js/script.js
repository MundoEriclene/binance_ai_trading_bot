const output = document.getElementById("output");
const typingSound = document.getElementById("typingSound"); // ativar se for usar áudio

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
let typing = true;

function typeNextCharacter() {
  if (messageIndex >= messages.length) return;

  currentMessage = messages[messageIndex];

  if (charIndex < currentMessage.length) {
    output.textContent += currentMessage.charAt(charIndex);
    charIndex++;

    // typingSound.play(); // descomente se quiser som
    setTimeout(typeNextCharacter, 40); // velocidade da digitação
  } else {
    output.textContent += "\n\n";
    messageIndex++;
    charIndex = 0;
    setTimeout(typeNextCharacter, 800); // tempo entre mensagens
  }
}

// Iniciar efeito digitando após carregamento
window.onload = () => {
  typeNextCharacter();
};
// Desbloqueia o som após o primeiro clique
window.addEventListener("click", () => {
    typingSound.play();
  });
  