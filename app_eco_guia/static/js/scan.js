// Acessar a câmera
const openCameraButton = document.getElementById("open-camera");
const switchCameraButton = document.getElementById("switch-camera");
const cameraContainer = document.getElementById("camera-container");
const video = document.getElementById("video");
const captureButton = document.getElementById("capture");
const canvas = document.getElementById("canvas");
const uploadForm = document.getElementById("upload-form");
let stream = null;
let currentFacingMode = "environment";

async function openCamera() {
  const constraints = {
    video: {
      facingMode: { ideal: currentFacingMode },
      width: { ideal: window.innerWidth }, // Adapta ao tamanho da tela
      height: { ideal: window.innerHeight }, // Adapta ao tamanho da tela
    },
  };

  try {
    stream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = stream;
    cameraContainer.style.display = "block";

    // Ajustar o vídeo ao tamanho do dispositivo
    video.onloadedmetadata = function () {
      video.style.width = "100%"; // Ajusta para ocupar a largura do contêiner
      video.style.height = "auto"; // Mantém proporção correta
    };
  } catch (error) {
    console.error("Erro ao acessar a câmera:", error);
    alert("Não foi possível acessar a câmera.");
  }
}

openCameraButton.addEventListener("click", openCamera);

switchCameraButton.addEventListener("click", async function () {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
  }
  currentFacingMode =
    currentFacingMode === "environment" ? "user" : "environment";
  await openCamera();
});

// Capturar a imagem quando o botão é clicado
captureButton.addEventListener("click", function () {
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  // Pausar a visualização da câmera após capturar a imagem
  video.pause();

  // Converter a imagem do canvas para um blob e enviá-la
  canvas.toBlob(function (blob) {
    const fileInput = document.getElementById("file-input");
    const file = new File([blob], "captured_image.png", {
      type: "image/png",
    });

    // Colocar o arquivo capturado no input file (para ser enviado para a API)
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;

    // Atualizar o label do input
    document.getElementById("file-label-text").textContent =
      "captured_image.png";
  }, "image/png");

  // Fechar a câmera
  stream.getTracks().forEach((track) => track.stop());
  cameraContainer.style.display = "none"; // Esconder a visualização da câmera
});

// Listener para quando o arquivo é selecionado no input
const fileInput = document.getElementById("file-input");
fileInput.addEventListener("change", function () {
  const fileName =
    fileInput.files.length > 0
      ? fileInput.files[0].name
      : "Nenhum arquivo escolhido";
  document.getElementById("file-label-text").textContent = fileName;
});

// Função para atualizar o histórico no frontend
function addHistoryEntry(category, imageUrl, count) {
  const historyContainer = document.getElementById("history-container");

  // Verifica se já existe uma entrada para essa categoria
  let existingEntry = historyContainer.querySelector(
    `[data-category="${category}"]`
  );

  if (existingEntry) {
    // Atualiza o contador se a categoria já existir
    let counter = existingEntry.querySelector(".counter");
    counter.textContent = `(${count})`;
    let img = existingEntry.querySelector(".history-img");
    img.src = imageUrl; // Atualiza a imagem
  } else {
    // Cria uma nova entrada no histórico
    const entryHtml = `
  <div class="history-entry" data-category="${category}">
    <strong>Categoria:</strong> ${category}
    <span class="counter">(${count})</span>
    <p>Última imagem enviada: <img src="media/${imageUrl}" alt="Imagem" class="history-img"></p>
  </div>
`;
    historyContainer.insertAdjacentHTML("beforeend", entryHtml);
  }
}

// Enviar o formulário com a imagem capturada ou selecionada
uploadForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  let fileInput = document.getElementById("file-input");
  if (fileInput.files.length === 0) {
    alert("Por favor, selecione ou capture uma imagem primeiro.");
    return;
  }

  let file = fileInput.files[0];

  let formData = new FormData();
  formData.append("file", file);

  // Obtendo o CSRF token
  const csrftoken = getCookie("csrftoken");

  try {
    let response = await fetch(
      "https://e740-177-104-245-40.ngrok-free.app/predict/",
      {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken, // Incluindo o CSRF token no cabeçalho
        },
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error("Erro na solicitação: " + response.statusText);
    }

    let result = await response.json();
    document.getElementById("result").innerHTML = `
      <strong>Categoria:</strong> ${result.category}<br>
      <strong>Confiança:</strong> ${(result.confidence * 100).toFixed(2)}%
    `;

    // Atualizar o histórico no frontend após a predição
    addHistoryEntry(result.category, result.image_url, result.count);
  } catch (error) {
    console.error("Erro:", error);
    alert("Erro ao enviar a imagem. Tente novamente.");
    document.getElementById("result").innerText = "Erro no processamento";
  }
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Ajustar a câmera quando a janela ou orientação muda
window.addEventListener("resize", function () {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop()); // Para a câmera anterior
  }
  openCamera(); // Reabre a câmera com a nova resolução
});
