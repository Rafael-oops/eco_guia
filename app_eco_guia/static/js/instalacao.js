let instalando;

window.addEventListener('beforeinstallprompt', (e) => {
    // Evita o prompt automático
    e.preventDefault();
    instalando = e;

    // Exibe o botão para instalar o PWA
    const installButton = document.getElementById('instalacao');
    installButton.style.display = 'block';

    installButton.addEventListener('click', () => {
        // Exibe o prompt
        instalando.prompt();
        instalando.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('Usuário aceitou instalar o PWA');
            } else {
                console.log('Usuário recusou instalar o PWA');
            }
            instalando = null;
        });
    });
});

