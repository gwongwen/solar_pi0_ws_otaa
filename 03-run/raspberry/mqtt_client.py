import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

class mqtt_client:
    #Class constructor, generates a clientMQTT
    #needs the mqtt parametters and the node's id
    def __init__(self, broker_address, port, client_id = "null"):
        self.broker_address_mqtt = broker_address
        self.port_mqtt = port
        self.client_mqtt_id = client_id
        print("Initializing mqtt client at " + self.broker_address_mqtt + ":" + str(self.port_mqtt))
    
    #Connects to the MQTT broker and returns the client instance
    #Adds the on_message callback
    def client_connect(self,on_message):
        print("--------------------------------------------")
        print("Creating Dispatcher Connection")
        client = mqtt.Client(self.client_mqtt_id)
        client.on_message=on_message
        print("Connecting to broker")
        client.connect(self.broker_address_mqtt, self.port_mqtt)
        print("Client connection successful")
        return client
    
    #Subscribe to a topic, needs the client and the topic to subscribe
    def subscribe_topic(self,client,topic_to_subscribe):
        print("Subscribing to topic " + topic_to_subscribe)
        client.subscribe(topic_to_subscribe)
        return client
    
    #Subscribe to a topic, needs the client and the topic to subscribe
    def unsubscribe_topic(self,client,topic_to_subscribe):
        print("Unsubscribing topic " + topic_to_subscribe)
        client.unsubscribe(topic_to_subscribe)
        return client
        
    #Starts client loop, needs a client
    def start_loop(self,client):
        client.loop_start()
        return client
    
    #Stops client loop, needs a client
    def stop_loop(self,client):
        client.loop_stop()
        return client
    
