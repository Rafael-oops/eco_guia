// MENU HAMBURGUER QUANDO A TELA FICAR PRA CELULAR
const navSlide = () => {
  const burger = document.querySelector(".burger");
  const nav = document.querySelector(".nav-links");
  const navLinks = document.querySelectorAll(".nav-links li");

  // Fazendo o clique do menu funcionar
  burger.addEventListener("click", () => {
    // Alternando a visibilidade do menu
    nav.classList.toggle("nav-active");

    // Animações dos links
    navLinks.forEach((link, index) => {
      if (link.style.animation) {
        link.style.animation = "";
      } else {
        link.style.animation = `navlinkFade 0.7s ease forwards ${
          index / 7 + 1.5
        }s`;
      }
    });

    // Transformando o ícone do menu em 'X'
    burger.classList.toggle("toggle");
  });
};

navSlide();



// CARDS FLUTUANTE QUE APARECE AO CLICAR NA IMAGEM DO LIXO  -------------------------------------------

const categories = {
  red: {
    title: "Lixo Vermelho",
    description:
      "O lixo vermelho é utilizado para descarte de plásticos como garrafas PET, embalagens de plástico, etc.",
  },
  blue: {
    title: "Lixo Azul",
    description:
      "O lixo azul é utilizado para descarte de papéis, como jornais, folhas impressas, revistas.",
  },
  yellow: {
    title: "Lixo Amarelo",
    description:
      "O lixo amarelo é destinado ao descarte de metais, como latas de alumínio e objetos de ferro.",
  },
  green: {
    title: "Lixo Verde",
    description:
      "O lixo verde é usado para o descarte de vidros, como garrafas, potes de vidro, entre outros.",
  },
  black: {
    title: "Lixo Preto",
    description:
      "O lixo preto é destinado ao descarte de madeiras, como móveis, paletes e outros itens de madeira.",
  },
  orange: {
    title: "Lixo Laranja",
    description:
      "O lixo laranja é utilizado para o descarte de resíduos perigosos, como pilhas, baterias e produtos químicos.",
  },
  white: {
    title: "Lixo Branco",
    description:
      "O lixo branco é destinado ao descarte de resíduos ambulatoriais e de serviços de saúde.",
  },
  purple: {
    title: "Lixo Roxo",
    description:
      "O lixo roxo é utilizado para o descarte de resíduos radioativos.",
  },
  brown: {
    title: "Lixo Marrom",
    description:
      "O lixo marrom é destinado ao descarte de resíduos orgânicos, como restos de comida e outros materiais biodegradáveis.",
  },
  gray: {
    title: "Lixo Cinza",
    description:
      "O lixo cinza é utilizado para o descarte de lixo não reciclável, contaminado ou cuja separação não é possível.",
  },
};


const cardContainer = document.getElementById("card-container");
const cardTitle = document.getElementById("card-title");
const cardDescription = document.getElementById("card-description");
const closeCard = document.getElementById("close-card");
// Função para abrir o card
function showCard(category, element) {
  cardTitle.innerText = categories[category].title;
  cardDescription.innerText = categories[category].description;
  cardContainer.classList.remove("hidden");
  cardTitle.style.fontFamily = "Arial, sans-serif"; // Altere para a fonte desejada
  cardTitle.style.fontSize = "20px";

  // Calcula a posição do item clicado
  const rect = element.getBoundingClientRect();
  const top = rect.top + window.scrollY; // Posição vertical do item
  const left = rect.left + window.scrollX; // Posição horizontal do item

  // Posiciona o card em cima do item
  cardContainer.style.top = `${top - cardContainer.offsetHeight - 10}px`; // 10px de margem superior
  cardContainer.style.left = `${left + rect.width / 2 - cardContainer.offsetWidth / 2}px`; // Centraliza o card horizontalmente
}


// Função para associar os eventos de clique de forma dinâmica
Object.keys(categories).forEach((color) => {
  document.getElementById(color).addEventListener("click", (event) => showCard(color, event.currentTarget));
});

// Função para fechar o card
closeCard.addEventListener("click", () => {
  cardContainer.classList.add("hidden");
});
