from dataclasses import dataclass
import json
from aiokafka import AIOKafkaProducer

@dataclass
class BrokerProducer:
    bootstrap_servers: str
    email_topic: str
    producer: AIOKafkaProducer | None = None

    async def _get_producer(self) -> AIOKafkaProducer:
        if self.producer is None:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers
            )
            await self.producer.start()
        return self.producer

    async def send_welcome_email(self, email_data: dict) -> None:
        producer = await self._get_producer()
        await producer.send(
            topic=self.email_topic,
            value=json.dumps(email_data).encode(),
        )
        

    async def close(self):
        if self.producer:
            await self.producer.stop