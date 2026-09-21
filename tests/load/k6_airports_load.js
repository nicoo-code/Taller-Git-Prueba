import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 10 },  // Rampa a 10 usuarios
    { duration: '30s', target: 50 },  // Pico sostenido de 50 usuarios concurrentes
    { duration: '10s', target: 0 },   // Rampa descendente
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // El 95% de las peticiones debe responder en < 200ms (Caché Redis activa)
    http_req_failed: ['rate<0.01'],   // Menos del 1% de errores permitidos
  },
};

const BASE_URL = __ENV.TARGET_URL || 'http://localhost:8000';

export default function () {
  // 1. Consultar catálogo completo de aeropuertos
  const resCatalog = http.get(`${BASE_URL}/api/v1/airports`);
  check(resCatalog, {
    'airports status is 200': (r) => r.status === 200,
    'airports returned list': (r) => Array.isArray(r.json()),
  });

  // 2. Consultar mapa Plotly Scattergeo
  const resMap = http.get(`${BASE_URL}/api/v1/airports/map/plotly`);
  check(resMap, {
    'map status is 200': (r) => r.status === 200,
    'map has data array': (r) => r.json('data') !== undefined,
  });

  sleep(1);
}
