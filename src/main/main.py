from mqtt_api import Client
from window import Window
from topic_tree import Device
import topic_tree
import sys
import threading


class App:
    """
    The head module of the actual app
    > Initializes everything
    > Handles IOT connection and incoming mqtt actions
    > As long as an instance of this class exists, the app is considered to be on
    """
    def __init__(self, source):
        """
        Initialize the app instance

        :param source: string, path to the json file representing plan of the house
        """
        # Parse json file to the dedicated data structure being the topic tree
        self.tree = topic_tree.parse(topic_tree.readFile(source, verbose=False))

        # Above all, make sure the conversion to topic tree was successful
        assert self.tree

        # Initialize list of subscriptions
        subscriptions = []

        # Thread synchronization
        # Will be crucial for correct window instantiating
        lock = threading.Lock()

        # Instantiate the window
        self.frame = Window(lock, self)

        # Make sure that window is ready for further steps
        lock.acquire()
        lock.release()

        # Iterate through devices on topic tree
        for topic, device in self.tree.devices:
            # Add device to subscription list
            # Default quality of service set to 1
            # Quality of service (QoS) cheat sheet (in case the default is to be changed)
            #  QoS = 0: we prefer that the message will not arrive at all rather than arrive twice
            #  QoS = 1: we want the message to arrive at least once but don't care if it arrives twice or more
            #  QoS = 2: we want the message to arrive exactly once
            subscriptions += [(topic, 1)]

            # Add device to the window frame and get the feedback device id
            dev_id = self.frame.addDevice(device.device)

            # Save the acquired for it might be useful in future
            device.device.id = dev_id
            
        # Initialize mqtt client using 'mqtt-api' abstraction layer
        self.client = Client("App")

        # Incoming message handling
        self.client.add_on_message(self.handler)

        # Connection and subscribing to all topics mentioned on subscription list
        self.client.connect()
        self.client.subscribe(subscriptions)

        # Start the client
        self.client.start()

        # Set the window closing handling
        # When the window is being closed, the app terminates itself as well
        self.frame.on_closing(self.terminate)

        # Successful init log (to terminal by default)
        print("### Client turned on  ###")
    
    def terminate(self):
        """
        Make sure that the exit is clean
        Terminate connection with mqtt client

        :return: nothing
        """
        # Stop the client and cease the connection
        self.client.stop()
        self.client.disconnect()

        # Successful termination log (to terminal by default)
        print("### Client tunred off ###")
        
    def handler(self, topic, msg):
        """
        Default handler for the incoming messages

        :param topic: topic from which the message has been received
        :param msg: message content
        :return: nothing
        """
        # Get the reference to the right device via topic tree
        dev = self.tree[topic].device

        # Conclude the new state of the device in terms of allowed enumerates
        # If fails, sets to None
        new_state = Device.states_to_enum[msg] if msg in Device.states_to_enum else None

        # If the operation hasn't failed, then:
        if new_state is not None:
            # Update device icon on the window house overview
            self.frame.setIcon(dev.id, dev.dev_type, new_state)

            # Save the message
            dev.state = msg

            # Update latest actions list
            self.frame.updateLatestList(dev)


if __name__ == '__main__':
    """
    Main initializer
    """
    # Default run
    if len(sys.argv) == 1:
        main = App("../config/plan.json")
    # Nonstandard run
    elif len(sys.argv) >= 2:
        main = App(str(sys.argv[1]))
