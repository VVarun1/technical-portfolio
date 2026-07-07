import pika
# Order Service publishing 'order.created' event to RabbitMQ
def create_order(order_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.basic_publish(exchange='orders', routing_key='order.created', body=f"Order {order_id}")
    print(f"Order {order_id} created")
