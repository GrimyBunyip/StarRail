from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class PostOpConversation(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Post-Op Conversation')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ER', description=self.name,
                        amount=0.06 + 0.02 * self.superposition)
            char.addStat('Heal', description=self.name,
                        amount=0.09 + 0.03 * self.superposition,
                        type=['ultimate'])
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    PostOpConversation(**Configuration).print()