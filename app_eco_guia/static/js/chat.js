const chatContainer = document.getElementById("chat-container");
const chatbotIcon = document.getElementById("chatbot-icon");
const closeBtn = document.getElementById("close-btn");
const input = document.getElementById("mensagem-input");
const enviarBtn = document.getElementById("enviar-btn");

chatbotIcon.addEventListener("click", function () {
  chatContainer.classList.toggle("active");
  input.focus();  // Foca no campo de input ao abrir o chat
});

closeBtn.addEventListener("click", function () {
  chatContainer.classList.remove("active");
});

input.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    enviarMensagem();
  }
});

enviarBtn.addEventListener("click", function () {
  enviarMensagem();
});

function enviarMensagem() {
  const mensagem = input.value.trim();
  if (mensagem) {
    adicionarMensagemUsuario(mensagem);
    processarMensagem(mensagem);
    input.value = "";
    input.focus();
  }
}

function adicionarMensagemUsuario(mensagem) {
  const chatBox = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = "chat-message user";
  div.textContent = mensagem;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function adicionarMensagemBot(resposta) {
  const chatBox = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = "chat-message bot";
  div.innerHTML = `<img src="${avatarUrl}" alt="ÁlvaroBot" class="message-avatar"><span>${resposta}</span>`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function adicionarMensagemComBotoes() {
  const typingIndicator = document.getElementById("typing-indicator");
  const chatBox = document.getElementById("chat-box");

  typingIndicator.style.display = "flex";
  chatBox.appendChild(typingIndicator);

  setTimeout(() => {
    typingIndicator.style.display = "none";

    const div = document.createElement("div");
    div.className = "chat-message bot";
    div.innerHTML = `
      <img src="${avatarUrl}" alt="ÁlvaroBot" class="message-avatar">
      <span>Posso ajudar em algo mais?</span>
      <div class="botao-container">
        <button id="botao-sim">Sim</button>
        <button id="botao-nao">Não</button>
      </div>`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;

    document.getElementById("botao-sim").onclick = () => {
      removerBotoes();
      mostrarOpcoesIniciais();
    };

    document.getElementById("botao-nao").onclick = () => {
      removerBotoes();
      mostrarMensagemDespedida();
    };
  }, 2000);
}

function removerBotoes() {
  const botaoContainer = document.querySelector(".botao-container");
  if (botaoContainer) {
    botaoContainer.remove();
  }
}

function mostrarOpcoesIniciais() {
  adicionarMensagemBot(`Selecione uma das opções de ajuda abaixo:<br />
    1- Localização de eco pontos🔎.<br />
    2- Lixeira ideal para descarte🗑️.<br />
    3- Dicas de Reciclagem♻️.<br />
    4- Dicas de Redução de Resíduos.`);
}

function mostrarMensagemDespedida() {
  adicionarMensagemBot("Obrigado por usar o ÁlvaroBot! Tenha um ótimo dia!");
}

// Função para obter o CSRF token do meta tag
function getCSRFTokenFromMeta() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

const csrftoken = getCSRFTokenFromMeta();

// Atualizando a função processarMensagem
function processarMensagem(mensagem) {
  const typingIndicator = document.getElementById("typing-indicator");
  const chatBox = document.getElementById("chat-box");

  typingIndicator.style.display = "flex";
  chatBox.appendChild(typingIndicator);

  setTimeout(() => {
    fetch("/chat/", {  
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ mensagem: mensagem }),
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Erro na resposta do servidor");
      }
      return response.json();
    })
    .then((data) => {
      typingIndicator.style.display = "none";
      adicionarMensagemBot(data.resposta);
      adicionarMensagemComBotoes();
    })
  }, 1000);
}
