class BuffEffect:
    name:str
    description:str
    type:str
    amount:float
    stacks:float
    uptime:float
    mathType:str
    duration:int

    def __init__(self, name:str, description:str, amount:float, type:str=None, stacks:float=1.0, uptime:float=1.0, mathType:str='base',duration:int=None):
        self.name = name
        self.description = description
        self.amount = float(amount)
        self.type = type
        self.stacks= stacks
        self.uptime = uptime
        self.mathType = mathType
        self.duration = duration

    def print(self):
        print([value for _, value in self.__dict__.items()])