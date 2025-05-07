from .baseprimative import Primative

class treenode(Primative):
    children: list[Primative]

    def __init__(self, children: list[Primative]):
        self.children = children