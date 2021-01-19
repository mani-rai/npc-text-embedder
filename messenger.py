import json

import pika

class Messenger:

    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.17.0.2"))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange='npc.exchange', exchange_type='direct', durable=True)
        self.channel.queue_declare("npc.queue.en.embeddings", durable=True, auto_delete=False)
        self.channel.queue_declare("npc.queue.ne.embeddings", durable=True, auto_delete=False)
        self.channel.queue_bind("npc.queue.en.embeddings", "npc.exchange", "npc.routing.en.embeddings")
        self.channel.queue_bind("npc.queue.ne.embeddings", "npc.exchange", "npc.routing.ne.embeddings")

    def get_text(self):
        method_frame, header_frame, body = self.channel.basic_get(queue='npc.queue')
        if method_frame is None:
            return None
        else:
            self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            content = json.loads(body)
            text = None
            if content is not None:
                fields = content['fields']
                if fields is not None or len(fields) > 0:
                    for field in fields:
                        type = field['key']
                        if type is not None and type == "content":
                            values = field['values']
                            if values is not None and len(values) > 0:
                                text = values[0]
            return text

    def send_embeddings(self, sentences, embeddings, lang):

        if embeddings is None:
            return

        for index, embedding in enumerate(embeddings):
            string_embedding = self.listToString(embedding)
            json_message = {"text": sentences[index], "embedding": string_embedding}
            message = json.dumps(json_message)
            if lang == "en":
                self.channel.basic_publish(exchange='npc.exchange', routing_key='npc.routing.en.embeddings', body=message)
            else:
                self.channel.basic_publish(exchange='npc.exchange', routing_key='npc.routing.ne.embeddings', body=message)

    def listToString(self, list):
        result = "["
        for idx, item in enumerate(list):
            result = result + str(item)
            if idx != (len(list) - 1):
                result = result + ","
        result = result + "]"
        return result