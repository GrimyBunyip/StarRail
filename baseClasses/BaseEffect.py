class BaseEffect:
  damage:float
  gauge:float
  energy:float
  skillpoints:float

  def __init__(self, damage:float=0.0, gauge:float=0.0, energy:float=0.0, skillpoints:float=0.0):
    self.damage = damage
    self.gauge = gauge
    self.energy = energy
    self.skillpoints = skillpoints

  def print(self):
    print(self.__dict__)

  # some code so we can do arithmetic with this object

  def __add__(self, value:'BaseEffect'):
    damage = self.damage + value.damage
    gauge = self.gauge + value.gauge
    energy = self.energy + value.energy
    skillpoints = self.skillpoints + value.skillpoints

    return BaseEffect(damage, gauge, energy, skillpoints)

  def __sub__(self, value:'BaseEffect'):
    damage = self.damage - value.damage
    gauge = self.gauge - value.gauge
    energy = self.energy - value.energy
    skillpoints = self.skillpoints - value.skillpoints

    return BaseEffect(damage, gauge, energy, skillpoints)

  def __mul__(self, value:float):
    damage = self.damage * value
    gauge = self.gauge * value
    energy = self.energy * value
    skillpoints = self.skillpoints * value

    return BaseEffect(damage, gauge, energy, skillpoints)

  def __radd__(self, value:float):
    return self.__add__(value)

  def __iadd__(self, value:float):
    return self.__add__(value)

  def __rsub__(self, value:float):
    return self.__sub__(value)

  def __isub__(self, value:float):
    return self.__sub__(value)

  def __rmul__(self, value:float):
    return self.__mul__(value)

  def __imul__(self, value:float):
    return self.__mul__(value)