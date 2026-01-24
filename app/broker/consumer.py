from dataclasses import dataclass
import json
from aiokafka import AIOKafkaConsumer


@dataclass
class BrokerConsumer:
    bootstrap_servers: str
    email_callback_topic: str
    consumer: AIOKafkaConsumer | None = None

    async def _get_consumer(self) -> AIOKafkaConsumer:
        if self.consumer is None:
            self.consumer = AIOKafkaConsumer(
                self.email_callback_topic,              
                bootstrap_servers=self.bootstrap_servers,
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            )
            await self.consumer.start()
        return self.consumer

    async def consume_callback_message(self) -> None:
        consumer = await self._get_consumer()

        try:
            async for message in consumer:
                # message.value уже dict
                print("CALLBACK MESSAGE:", message.value)

                # тут дальше будет твоя бизнес-логика
                # await self.handle_callback(message.value)

        except Exception as e:
            print("Consumer error:", e)

        finally:
            await consumer.stop()

    async def close(self):
        if self.consumer:
            await self.consumer.stop()