from .baseprimative import Primative
from PIL.Image import Image

class image(Primative):
    image: Image
    alt_text: str

    def __init__(self, image: Image, alt_text: str):
        self.image = image
        self.alt_text = alt_text