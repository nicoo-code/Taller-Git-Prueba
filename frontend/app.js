document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('itinerary-form');
  const alertBox = document.getElementById('alert-box');
  const originSelect = document.getElementById('origin_airport');
  const destSelect = document.getElementById('destination_airport');
  const itinerariesList = document.getElementById('itineraries-list');
  const btnRefresh = document.getElementById('btn-refresh-itineraries');
  const airportsCount = document.getElementById('airports-count');
  const circuitIndicator = document.getElementById('circuit-indicator');

  // Mapa local de ID a nombre para renderizar nombres en la tabla
  const airportsMap = {};

  function showAlert(message, type = 'success') {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
    alertBox.classList.remove('d-none');
    setTimeout(() => {
      alertBox.classList.add('d-none');
    }, 5000);
  }

  // 1. Cargar Mapa Geográfico con Plotly JS
  async function loadAirportsMap() {
    try {
      const response = await fetch('/api/v1/airports/map/plotly');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();

      Plotly.newPlot('map', payload.data, payload.layout, {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['lasso2d', 'select2d']
      });

      if (airportsCount) {
        airportsCount.textContent = `${payload.count || payload.data[0]?.lat?.length || 0} Aeropuertos`;
      }
    } catch (err) {
      console.warn('Error loading Plotly map:', err);
      if (airportsCount) airportsCount.textContent = 'Modo Offline';
    }
  }

  // 2. Poblar selectores de aeropuertos
  async function loadAirportsSelect() {
    try {
      const response = await fetch('/api/v1/airports');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const airports = await response.json();

      originSelect.innerHTML = '<option value="">Seleccione aeropuerto de salida...</option>';
      destSelect.innerHTML = '<option value="">Seleccione aeropuerto de llegada...</option>';

      airports.forEach(airport => {
        airportsMap[airport.id] = `${airport.name} (${airport.iata_code})`;
        const option1 = document.createElement('option');
        option1.value = airport.id;
        option1.textContent = `${airport.city} - ${airport.name} [${airport.iata_code}]`;
        originSelect.appendChild(option1);

        const option2 = document.createElement('option');
        option2.value = airport.id;
        option2.textContent = `${airport.city} - ${airport.name} [${airport.iata_code}]`;
        destSelect.appendChild(option2);
      });

      // Pre-seleccionar BOG y MDE por comodidad
      if (airports.find(a => a.id === 1)) originSelect.value = "1";
      if (airports.find(a => a.id === 5)) destSelect.value = "5";

    } catch (err) {
      console.error('Error fetching airports list:', err);
      showAlert('No se pudo cargar el catálogo de aeropuertos.', 'error');
    }
  }

  // 3. Cargar y listar itinerarios
  async function loadItineraries() {
    try {
      const response = await fetch('/api/v1/itineraries');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const itineraries = await response.json();

      if (itineraries.length === 0) {
        itinerariesList.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No hay itinerarios registrados aún.</td></tr>';
        return;
      }

      itinerariesList.innerHTML = '';
      itineraries.forEach(item => {
        const tr = document.createElement('tr');
        const originName = airportsMap[item.origin_airport_id] || `ID ${item.origin_airport_id}`;
        const destName = airportsMap[item.destination_airport_id] || `ID ${item.destination_airport_id}`;
        const dateFormatted = new Date(item.departure_date).toLocaleDateString('es-CO', {
          month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
        });

        tr.innerHTML = `
          <td><strong>${item.user_name}</strong></td>
          <td>${originName} → ${destName}</td>
          <td>${dateFormatted}</td>
          <td>${item.duration_minutes} min</td>
          <td><span class="badge badge-success">${item.status}</span></td>
        `;
        itinerariesList.appendChild(tr);
      });
    } catch (err) {
      console.warn('Error fetching itineraries:', err);
    }
  }

  // 4. Formulario de creación de itinerario
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const originId = parseInt(originSelect.value);
    const destId = parseInt(destSelect.value);

    if (originId === destId) {
      showAlert('El aeropuerto de salida y de llegada no pueden ser el mismo.', 'error');
      return;
    }

    const payload = {
      user_name: document.getElementById('user_name').value.trim(),
      origin_airport_id: originId,
      destination_airport_id: destId,
      departure_date: new Date(document.getElementById('departure_date').value).toISOString(),
      duration_minutes: parseInt(document.getElementById('duration_minutes').value)
    };

    const submitBtn = document.getElementById('btn-submit');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Validando y guardando...';

    try {
      const response = await fetch('/api/v1/itineraries', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer sim-jwt-token-sample'
        },
        body: JSON.stringify(payload)
      });

      const resData = await response.json();

      if (response.status === 201) {
        showAlert(`¡Itinerario para ${resData.user_name} creado con éxito! Evento despachado al outbox.`, 'success');
        form.reset();
        setDefaultDateTime();
        await loadItineraries();
      } else {
        showAlert(resData.detail || 'Error al crear itinerario.', 'error');
      }
    } catch (err) {
      showAlert(`Error de conexión: ${err.message}`, 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Confirmar y Guardar Itinerario';
    }
  });

  function setDefaultDateTime() {
    const now = new Date();
    now.setDate(now.getDate() + 3);
    now.setHours(9, 0, 0, 0);
    const isoString = now.toISOString().slice(0, 16);
    document.getElementById('departure_date').value = isoString;
  }

  // 5. Monitoreo de salud
  async function checkSystemHealth() {
    try {
      const res = await fetch('/api/v1/airports/health');
      if (res.ok) {
        const data = await res.json();
        if (circuitIndicator && data.circuit_breaker) {
          circuitIndicator.textContent = `Circuit: ${data.circuit_breaker.state}`;
          circuitIndicator.className = data.circuit_breaker.state === 'CLOSED' ? 'badge badge-info' : 'badge badge-warning';
        }
      }
    } catch (e) {
      // Ignorar
    }
  }

  // Inicialización
  setDefaultDateTime();
  loadAirportsMap();
  loadAirportsSelect();
  loadItineraries();
  checkSystemHealth();

  if (btnRefresh) {
    btnRefresh.addEventListener('click', loadItineraries);
  }
});
