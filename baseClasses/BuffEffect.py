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
        if len(name.split('.')) > 1:
            self.name = name.split('.')[0]
            self.mathType = name.split('.')[1]
        else:
            self.name = name
            self.mathType = mathType
        self.description = description
        self.amount = float(amount)
        self.type = type
        self.stacks= stacks
        self.uptime = uptime
        self.duration = duration

    def print(self):
        print([value for _, value in self.__dict__.items()])