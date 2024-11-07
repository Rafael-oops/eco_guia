function initMap() {
  const mapId = "2879afcdd9c5ffa8"; // Substitua pelo seu mapId
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
      // Fecha o InfoWindow anterior, se estiver aberto
      infoWindow.close();

      // Obter o modo de transporte selecionado
      const travelMode = document.getElementById("travelMode").value;

      // Exibe as informações no InfoWindow com o botão para calcular rota
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


// Função para calcular a rota entre a localização atual e o destino selecionado
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
            alert(`Tempo estimado: ${duration}, Distância: ${distance}`);
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
