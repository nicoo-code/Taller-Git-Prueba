import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 5 },
    { duration: '20s', target: 20 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<400'], // P95 bajo 400ms incluyendo validación HTTP y Transactional Outbox
    http_req_failed: ['rate<0.02'],
  },
};

const BASE_URL = __ENV.TARGET_URL || 'http://localhost:8000';

export default function () {
  const payload = JSON.stringify({
    user_name: `LoadUser_${__VU}_${__ITER}`,
    origin_airport_id: 1,
    destination_airport_id: 5,
    departure_date: new Date(Date.now() + 86400000 * 3).toISOString(),
    duration_minutes: 55,
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer simulated-k6-jwt-token',
    },
  };

  // 1. Crear Itinerario
  const resCreate = http.post(`${BASE_URL}/api/v1/itineraries`, payload, params);
  check(resCreate, {
    'itinerary created 201': (r) => r.status === 201,
    'itinerary has id': (r) => r.json('id') !== undefined,
  });

  // 2. Listar Itinerarios
  const resList = http.get(`${BASE_URL}/api/v1/itineraries`);
  check(resList, {
    'list status is 200': (r) => r.status === 200,
  });

  sleep(1);
}
