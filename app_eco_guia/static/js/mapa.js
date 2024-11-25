function initMap() {
  const mapId = "2879afcdd9c5ffa8";
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: -1.450526, lng: -48.468272 },
    mapId: mapId,
  });

  // Inicializando os serviços de direção
  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);

  const pontosData = document.getElementById("pontos_data").textContent.trim();
  const pontos = JSON.parse(pontosData);

  const infoWindow = new google.maps.InfoWindow();

  pontos.forEach(function (ponto) {
    const advancedMarkerElement = new google.maps.marker.AdvancedMarkerElement({
      position: {
        lat: parseFloat(ponto.latitude),
        lng: parseFloat(ponto.longitude),
      },
      map: map,
      title: ponto.nome,
    });

    advancedMarkerElement.addListener("click", function () {
      // Atualiza a InfoWindow (como já faz atualmente)
      infoWindow.close();
      
      const travelMode = document.getElementById("travelMode").value;

      infoWindow.setContent(`
        <div class="info-window">
            <h3>${ponto.nome}</h3>
            <p>${ponto.endereco}</p>
            <p><strong>Horário:</strong> ${ponto.horario}</p>
            <p>${ponto.descricao}</p>
            <div class="button-container">
              <button onclick="calcRoute(${ponto.latitude}, ${ponto.longitude}, '${travelMode}')">Calcular Rota</button>
            </div>
        </div>
      `);
      
      infoWindow.setPosition({
        lat: parseFloat(ponto.latitude),
        lng: parseFloat(ponto.longitude),
      });
      infoWindow.open(map);
    });
  });
}

// Obtenha os elementos do pop-up
const routePopup = document.getElementById("route-popup");
const routeDetails = document.getElementById("route-details");
const closePopup = document.getElementById("close-popup");

// Função para mostrar o pop-up
function showPopup(message) {
  routeDetails.textContent = message;
  routePopup.classList.remove("hidden");
}

// Fechar o pop-up ao clicar no botão
closePopup.addEventListener("click", () => {
  routePopup.classList.add("hidden");
});

// Atualize a função calcRoute
function calcRoute(destLatitude, destLongitude, travelMode) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function (position) {
        const origin = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
        const destination = {
          lat: destLatitude,
          lng: destLongitude,
        };

        const request = {
          origin: origin,
          destination: destination,
          travelMode: google.maps.TravelMode[travelMode],
        };

        directionsService.route(request, function (result, status) {
          if (status === google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(result);

            // Opcional: Obter duração e distância da rota
            const route = result.routes[0].legs[0];
            const duration = route.duration.text;
            const distance = route.distance.text;

            // Substitui o alert pelo pop-up
            showPopup(`Tempo estimado: ${duration}, Distância: ${distance}`);
          } else {
            console.error("Erro ao calcular a rota: " + status);
          }
        });
      },
      function () {
        console.error("Erro ao obter a localização do usuário.");
      }
    );
  } else {
    console.error("Geolocalização não suportada pelo seu navegador.");
  }
}
