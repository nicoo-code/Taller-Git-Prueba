import asyncio
import json
import logging

from src.functions.send_notification_function import SendNotificationFunction

logger = logging.getLogger(__name__)


class RabbitMQEventConsumer:
    """
    Consumidor AMQP reactivo.
    Escucha la cola 'itinerary.notifications.queue' y ejecuta la función serverless SendNotificationFunction.
    """

    def __init__(
        self,
        amqp_url: str = "amqp://guest:guest@rabbitmq:5672/",
        exchange_name: str = "itinerary.events",
        queue_name: str = "itinerary.notifications.queue",
        notification_func: SendNotificationFunction | None = None,
    ):
        self.amqp_url = amqp_url
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.notification_func = notification_func
        self._is_running = False

    async def start(self):
        self._is_running = True
        logger.info("Starting RabbitMQEventConsumer loop...")

        while self._is_running:
            try:
                import aio_pika

                connection = await aio_pika.connect_robust(self.amqp_url)
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=10)

                # Declarar exchange y cola
                exchange = await channel.declare_exchange(
                    self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
                )

                queue = await channel.declare_queue(self.queue_name, durable=True)
                await queue.bind(exchange, routing_key="itinerary.#")

                logger.info(
                    f"Consumer bound to queue '{self.queue_name}'. Waiting for events..."
                )

                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        if not self._is_running:
                            break

                        async with message.process():
                            try:
                                body_str = message.body.decode("utf-8")
                                payload = json.loads(body_str)
                                trace_id = message.headers.get(
                                    "trace_id", payload.get("trace_id", "")
                                )

                                logger.info(
                                    f"Received message on queue {self.queue_name}: {payload.get('event_type')}",
                                    extra={"trace_id": trace_id},
                                )

                                if self.notification_func:
                                    await self.notification_func.execute(payload)

                            except (
                                KeyError,
                                ValueError,
                                TypeError,
                                json.JSONDecodeError,
                                OSError,
                                RuntimeError,
                            ) as proc_err:
                                logger.error(f"Error processing message: {proc_err}")

            except (ImportError, OSError, TimeoutError, RuntimeError) as conn_err:
                logger.warning(
                    f"RabbitMQ connection error in consumer: {conn_err}. Retrying in 5 seconds..."
                )
                await asyncio.sleep(5)

    def stop(self):
        self._is_running = False
        logger.info("Stopped RabbitMQEventConsumer.")
