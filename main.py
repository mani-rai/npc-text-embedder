from embedder import Embedder
from messenger import Messenger
from langdetect import detect

class Application:

    def __init__(self):
        self.messenger = Messenger()
        self.embedder = Embedder()

    def start(self):
        text = self.messenger.get_text()
        if text is not None:
            lang = detect(text)
            if lang == "en" or lang == "ne":
                sentences, embeddings = self.embedder.encode(text, lang)
                self.messenger.send_embeddings(sentences, embeddings, lang)

if __name__ == '__main__':
    app = Application()
    app.start()
