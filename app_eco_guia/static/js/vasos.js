    // Função para lidar com o envio do formulário
    document.getElementById("submitComment").addEventListener("click", function(event) {
        event.preventDefault(); // Previne o comportamento padrão

        // Pegar os valores do nome e do comentário
        const name = document.getElementById("name").value;
        const comment = document.getElementById("comment").value;

        // Verifica se os campos estão preenchidos
        if (name && comment) {
            // Criar um novo elemento de comentário
            const commentSection = document.createElement("div");
            commentSection.classList.add("comment");
            commentSection.innerHTML = `<strong>${name}:</strong> <p>${comment}</p>`;

            // Adicionar o comentário à lista de comentários
            document.getElementById("commentList").appendChild(commentSection);

            // Limpar o formulário após o envio
            document.getElementById("name").value = "";
            document.getElementById("comment").value = "";
        } else {
            alert("Por favor, preencha todos os campos!");
        }
    });

