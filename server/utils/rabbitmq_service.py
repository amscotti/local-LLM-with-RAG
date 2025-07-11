import pika
import json
from typing import Callable, Any

class RabbitMQService:
    def __init__(self, host='rabbitmq', port=5672, username='user', password='password'):
        self.credentials = pika.PlainCredentials(username, password)
        self.parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=self.credentials
        )
        self.connection = None
        self.channel = None

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()
        return self.channel

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def declare_queue(self, queue_name):
        channel = self.connect()
        channel.queue_declare(queue=queue_name, durable=True)
        return channel

    def publish_message(self, queue_name, message):
        channel = self.declare_queue(queue_name)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # делает сообщение персистентным
            )
        )

    def consume_messages(self, queue_name, callback: Callable[[Any], None]):
        channel = self.declare_queue(queue_name)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=lambda ch, method, properties, body: self._process_message(ch, method, properties, body, callback)
        )
        channel.start_consuming()

    def _process_message(self, ch, method, properties, body, callback):
        try:
            message = json.loads(body)
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Ошибка при обработке сообщения: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
