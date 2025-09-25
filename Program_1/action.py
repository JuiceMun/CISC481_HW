class Action:
    def __init__(self,direction:str, a:int, b:int):
        self.direction = direction
        self.a = a
        self.b = b

    def __str__(self) -> str:
        return f"(Direction: {self.direction} a: {self.a} b: {self.b})"