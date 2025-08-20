from mods_base import get_pc, SliderOption
from unrealsdk import find_object,find_class,load_package,make_struct
from unrealsdk.unreal import UObject 
from random import randint, Random
import time
from .comms import NotifyEffect


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

    def run_effect(self):
        print(f"running effect {self.effect_name} with id {self.id}. the current args are {self.args} and its duration is {self.duration}")
        if self.duration:
            Effect.running_effects.append(self.effect_name)
            ...
            #do duration shid

    def stop_effect(self):
        Effect.running_effects.remove(self.effect_name)
        NotifyEffect(self.thread, self.id, "Finished", self.effect_name)

    def on_map_change(self):
        #runs as soon as the loading screen finishes
        pass

    def map_change_finalized(self):
        #runs once the player can see
        pass
        