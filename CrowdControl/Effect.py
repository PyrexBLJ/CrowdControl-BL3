from random import randint, Random
import time
from mods_base import ENGINE
from unrealsdk.unreal import UObject
#from .comms import NotifyEffect


class Effect:
    registry = {}
    running_effects = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Effect.registry[cls.effect_name] = cls()#type:ignore
    
    def __init__(self) -> None:
        self.id: int = -1
        self.effect_name:str
        self.display_name:str = "Missing Display Name"
        self.duration:int = 0
        self.args:list = []
        self.is_running:bool = False
        self.thread = None
        self.pc:UObject
        self.start_time = None
        

    def run_effect(self):
        print(f"running effect {self.effect_name} with id {self.id}. the current args are {self.args} and its duration is {self.duration}")
        self.pc.DisplayRolloutNotification("Crowd Control", f"{self.display_name} Started!", 3.5 * ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation)
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
        if self.duration:
            self.pc.DisplayRolloutNotification("Crowd Control", f"{self.display_name} Ended!", 3.5 * ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation)


    def on_map_change(self):
        #runs as soon as the loading screen finishes
        pass

    def map_change_finalized(self):
        #runs once the player can see
        pass