const output = document.getElementById("output");
const typingSound = document.getElementById("typingSound");
const rodape = document.getElementById("rodape-glitch");
const manifestoLink = document.querySelector(".btn-manifesto");
const ghostKey = document.getElementById("ghost-key");

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

    // Exibe os botões após a digitação com efeito suave
    document.querySelector(".btn-sinistro").style.display = 'block'; // Exibe o botão "Revelar o Livro Perdido do Vaticano"
    document.querySelector(".btn-arquivo-cia").style.display = 'block'; // Exibe o botão "O Arquivo Perdido da CIA"
    document.querySelector(".btn-mundo-apos-queda").style.display = 'block'; // Exibe o botão "O Mundo Após a Queda"
    document.querySelector(".btn-arquivo-deepweb").style.display = 'block'; // Exibe o botão "O Arquivo Perigoso da Deep Web"

    // Transição suave para os botões
    document.querySelectorAll('.buttons-area a').forEach(btn => {
      btn.classList.add('show');
    });

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

document.getElementById("roadmap-key").addEventListener("click", () => {
    window.open("assets/roadmap_blacknode.pdf", "_blank");
});

// Novo botão sinistro para abrir página "O Livro Perdido do Vaticano"
const btnSinistro = document.querySelector(".btn-sinistro");
btnSinistro.addEventListener("click", () => {
  window.open("livro_perdido_vaticano.html", "_blank"); // Abre a nova página "O Livro Perdido do Vaticano"
});

// Função para alterar o tema dos botões
function changeButtonTheme(theme) {
  // Resetar os temas anteriores
  document.querySelectorAll('.btn-contrato, .btn-manifesto, .btn-sinistro, .btn-arquivo-cia, .btn-mundo-apos-queda, .btn-arquivo-deepweb')
    .forEach(btn => btn.classList.remove('fogo', 'sangue', 'gelo', 'vinganca', 'misterio', 'neon'));
  
  // Adicionar o novo tema nos botões
  document.querySelectorAll('.btn-contrato, .btn-manifesto, .btn-sinistro, .btn-arquivo-cia, .btn-mundo-apos-queda, .btn-arquivo-deepweb')
    .forEach(btn => btn.classList.add(theme));
}

// Exemplo de como ativar o tema "fogo" nos botões
changeButtonTheme('fogo');
