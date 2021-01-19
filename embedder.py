from indicnlp.tokenize import sentence_tokenize
from sentence_splitter import SentenceSplitter
from sentence_transformers import SentenceTransformer

class Embedder:

    def __init__(self):
        self.model = SentenceTransformer("LaBSE")
        self.en_sent_splitter = SentenceSplitter(language="en")

    def encode(self, text, lang):
        sentences = None
        if lang == "en":
            sentences = self.en_sent_splitter.split(text)
        elif lang == "ne":
            sentences = sentence_tokenize.sentence_split(text, "ne")
        filtered_sentences = [sentence for sentence in sentences if len(sentence.split()) > 3]
        return filtered_sentences, self.model.encode(filtered_sentences)