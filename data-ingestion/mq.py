import pika
from config import Settings

class RabbitMQConnection:
    "Singleton class to manage RabbitMQ connection."
    
    _instance = None
    
    def __new__(
        cls,
        host: str = None,
        port: str = None,
        user_name: str = None,
        password: str = None,
        virtual_host: str = "/",
    ):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance 
    
    def __init__(
        self,
        host: str = None,
        port: str = None,
        user_name: str = None,
        password: str = None,
        virtual_host: str = "/",
        fail_silently: bool = True,
        **kwargs,
    ):
        self.host = host or Settings.RABBITMQ_HOST
        self.port = port or Settings.RABBITMQ_PORT 
        self.user_name = user_name or Settings.RABBITMQ_DEFAULT_USERNAME
        self.password = password or Settings.RABBITMQ_DEFAULT_PASSWORD
        self.virtual_host = virtual_host 
        self.fail_silently = fail_silently
        self._connection = None 
        
    def __enter__(self):
        self.connect()
        return self 

    def __exit__(self):
        self.close()
        
        
    def connect(self):
        try:
            credentials = pika.PlainCredentials(self.user_name, self.password)
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    virtual_host=self.virtual_host,
                    credentials=credentials,
                
                )
            )
        
        except pika.exceptions.AMQPConnectionError as e:
            print("Failed to connect to RabbitMQ:  ",e)
            if not self.fail_silently:
                raise e
        
    def is_connected(self) -> bool:
        return self._connection is not None and self._connection.is_open
        
    
    def close(self):
        if self.is_connected():
            self._connection.close()
            self._connection = None 
            print("Closed RabbitMQ connection.")
        
    def get_channel(self):
        if self.is_connected():
            return self._connection.channel()
        
        
        
def publish_data_to_rabbitmq(queue_name: str, data: str) -> None :
    try:
        #Create an instance of RabbitMQConnection(class implemented using singleton design pattern)
        rabbimq_connection = RabbitMQConnection()
        
        #Establich connection
        with rabbimq_connection:
            channel = rabbimq_connection.get_channel()
            
            #Declare a queue
            channel.queue_declare(queue=queue_name, durable=True)
            
            #Publish data to the queue
            channel.basic_publish(
                exchange="", 
                routing_key=queue_name, 
                body=data,
                properties=pika.BasicProperties(
                    delivery_mode=2 # make message persistent
                ),
            )
            
            print("Data published to the queue.")
    except pika.exceptions.UnroutableError as e:
        print("Message could not be routed!")        
    except Exception as e:
        print(f"Error publishing to RabbitMQ:  {e}")

if __name__ == "__main__":
    publish_data_to_rabbitmq("test_queue", "Hello, World!")
        
        
        
        
        
        
        
        
        
        
        
        
        