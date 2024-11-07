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
};

const cardContainer = document.getElementById("card-container");
const cardTitle = document.getElementById("card-title");
const cardDescription = document.getElementById("card-description");
const closeCard = document.getElementById("close-card");

// Função para abrir o card
function showCard(category) {
  cardTitle.innerText = categories[category].title;
  cardDescription.innerText = categories[category].description;
  cardContainer.classList.remove("hidden");
  cardTitle.style.fontFamily = "Arial, sans-serif"; // Altere para a fonte desejada
  cardTitle.style.fontSize = "20px";
}

// Adiciona os eventos de clique nos boxes
document.getElementById("red").addEventListener("click", () => showCard("red"));
document
  .getElementById("blue")
  .addEventListener("click", () => showCard("blue"));
document
  .getElementById("yellow")
  .addEventListener("click", () => showCard("yellow"));
document
  .getElementById("green")
  .addEventListener("click", () => showCard("green"));

// Função para fechar o card
closeCard.addEventListener("click", () => {
  cardContainer.classList.add("hidden");
});
