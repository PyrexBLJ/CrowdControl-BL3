from random import randint, Random
import time
#from .comms import NotifyEffect


class Effect:
    registry = {}
    running_effects = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Effect.registry[cls.effect_name] = cls()#type:ignore
    
    def __init__(self) -> None:
        self.id: int = -1
        self.effect_name:str = ""
        self.duration:int = 0
        self.args:list = []
        self.is_running:bool = False
        self.thread = None
        self.pc = None
        self.start_time = None

    def run_effect(self):
        print(f"running effect {self.effect_name} with id {self.id}. the current args are {self.args} and its duration is {self.duration}")
        if self.duration:
            Effect.running_effects.append(self.effect_name)
            self.is_running = True
            ...
            #do duration shid

    def stop_effect(self):
        self.is_running = False
        Effect.running_effects.remove(self.effect_name)
        from . import NotifyEffect
        NotifyEffect(self.id, "Finished", self.effect_name, self.pc)

    def on_map_change(self):
        #runs as soon as the loading screen finishes
        pass

    def map_change_finalized(self):
        #runs once the player can see
        pass