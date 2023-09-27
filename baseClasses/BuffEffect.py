class BuffEffect:
    name:str
    amount:float
    stacks:float
    uptime:float

    def __init__(self, name:str, amount:float, stacks:float=1.0, uptime:float=1.0):
        self.name = name
        self.amount = amount
        self.stacks= stacks
        self.uptime = uptime

    def print(self):
        print(self.__dict__)