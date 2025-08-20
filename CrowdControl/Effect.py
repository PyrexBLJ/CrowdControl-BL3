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
        Effect.registry[cls.effect_name] = cls#type:ignore
    
    def __init__(self) -> None:
        self.id: int
        self.effect_name:str
        self.duration:int = 0
        self.args:list = []
        self.is_running:bool = False
        self.thread = None

    def run_effect(self):
        Effect.running_effects.append(self.id)
        print(f"running effect {self.effect_name} with id {self.id}. the current args are {self.args} and its duration is {self.duration}")
        if self.duration:
            ...
            #do duration shid

    def stop_effect(self):
        Effect.running_effects.remove(self.id)
        NotifyEffect(self.thread, self.id, "Finished", self.effect_name)

    def on_map_change(self):
        pass
        
        

effect_to_run = Effect.registry.get(0)
if effect_to_run:
    effect_inst = effect_to_run()
    effect_inst.args = ["add args here"]
    effect_inst.duration = 1
    print(f'running {effect_inst.effect_name} with id {effect_inst.id}')
    effect_inst.run_effect()