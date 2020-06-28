import paho.mqtt.client as mqtt


class ClientReactionsFactory:
    @staticmethod
    def on_message_f(handler):
        """
        Handler has to be a function of two argument: topic and stringified message payload
        Factory returns a function that can be used as proper on_message handler
        """
        def on_message(client, userdata, message):
            handler(message.topic,
                    str(message.payload.decode("utf-8")))
        return on_message


class Client:
    """
    Mqtt client API
    """
    def __init__(self, name, address=None):
        self.address = address if address else "127.0.0.1"
        self.client = mqtt.Client(name)
    
    def add_on_message(self, function, simplified=True):
        if simplified:
            self.client.on_message = ClientReactionsFactory.on_message_f(function)
        else:
            self.client.on_message = function
    
    def connect(self, port=1883):
        self.client.connect(self.address, port)
    
    def disconnect(self):
        self.client.disconnect()
    
    def subscribe(self, topics):
        self.client.subscribe(topics)
    
    def publish(self, topic, msg):
        self.client.publish(topic, msg)
    
    def start(self):
        self.client.loop_start()
    
    def stop(self):
        self.client.loop_stop()