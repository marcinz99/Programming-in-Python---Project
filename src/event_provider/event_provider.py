from mqtt_api import Client
from time import sleep
import sys


class EventProvider:
    """
    Simulate the real functioning of the system
    """
    def __init__(self, source):
        """
        Given the string path to the source of the schedule, initialize the event provider

        :param source: string path to the text file containing scheduled events
        """
        # Initialize event provider's mqtt client
        self.client = Client("EventProvider")

        # Read the data and save it as list of triplets as presented below
        #  (delay in milliseconds, topic, message)
        self.schedule = []
        with open(source, 'r', encoding='utf-8') as file:
            for a in file:
                delay, topic, msg = a.strip().split(' ')
                self.schedule += [[int(delay), topic, msg]]
    
    def run(self):
        # Run the client
        self.client.connect()
        self.client.start()

        # Iterate through the list of the scheduled actions and publish appropriate messages on time
        for i, event in enumerate(self.schedule):
            delay, topic, msg = event
            sleep(delay/1000.0)
            self.client.publish(topic, msg)
            print("Event {}: Delay = {}ms, Topic = '{}', Message = '{}'".format(
                i+1, delay, topic, msg))

        # When work is done, terminate yourself
        self.terminate()
    
    def terminate(self):
        # Make sure program exits cleanly, ceasing the mqtt connection first
        self.client.stop()
        self.client.disconnect()
        print("### Done - total: {} event(s) ###".format(len(self.schedule)))


if __name__ == '__main__':
    """
    Event provider initializer
    """
    # Default run
    if len(sys.argv) == 1:
        main = EventProvider("events_schedule.txt")
        main.run()
    # Nonstandard run
    elif len(sys.argv) >= 2:
        main = EventProvider(str(sys.argv[1]))
        main.run()
