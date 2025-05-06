from PIL import Image as PILImage

class FragmentPiece:
    def __init__(self, children: list):
        self.children = children

class TextPiece:
    text: str

    def __init__(self, text: str):
        self.text = text

class ImagePiece:
    image: PILImage.Image

    def __init__(self, image: PILImage.Image):
        self.image = image
