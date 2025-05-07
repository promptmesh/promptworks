from .baseprimative import Primative

class text(Primative):
    text: str

    def __init__(self, text: str):
        self.text = text