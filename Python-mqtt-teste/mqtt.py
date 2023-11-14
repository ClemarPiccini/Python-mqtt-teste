import paho.mqtt.client as mqtt
import json

broker_address = "test.mosquitto.org"
port = 1883
topic_subscribe = "/SenaiPowermig"
topic_publish = "/timestamp"

def on_message(client, userdata, msg):
    message_payload = msg.payload.decode("utf-8")
    print(f"Mensagem recebida: {message_payload}")

    try:
        message_data = json.loads(message_payload)
        timestamp = message_data.get("timestamp")

        if timestamp is not None:
            confirmation_message = {"timestamp": timestamp}
            client.publish(topic_publish, json.dumps(confirmation_message))
            print(f"Timestamp publicado: {timestamp}")
        else:
            print("Timestamp não encontrado na mensagem.")

    except json.JSONDecodeError:
        print("Erro ao analisar a mensagem JSON.")

client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, port, 1883)
client.subscribe(topic_subscribe)
client.loop_start()
try:
    while True:
        pass

except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("Desconectado do broker MQTT")
