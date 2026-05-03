from mods_base import ENGINE, get_pc #type: ignore
from unrealsdk.unreal import UObject #type: ignore
from .Comms import NotifyEffect, effect_instances
import time
import unrealsdk


class Effect:
    registry = {}
    running_effects = []
    effect_name:str
    display_name:str = "Missing Display Name"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Effect.registry[cls.effect_name] = cls()#type:ignore
    
    def __init__(self) -> None:
        self.id: int = -1
        self.effect_name:str
        self.duration:float = 0.0
        self.args:list = []
        self.is_running:bool = False
        self.pc:UObject
        self.start_time: float = time.time()
        self.viewer:str
        self.viewers = None
        self.sourcedetails = None
        self.from_client: bool = False
        self.quantity = None
        

    def run_effect(self, response:str = "Success", respond:bool = True):
        #print(f"running effect {self.effect_name} with id {self.id}. the current args are {self.args} and its duration is {self.duration}")
        hud = self.pc.GetHUDMovie()
        if hud != None:
            hud.ClearTrainingText()
            hud.AddTrainingText(f"{self.display_name}", "Crowd Control", 3.5 * ENGINE.GetCurrentWorldInfo().TimeDilation, unrealsdk.make_struct("Color"), "", False, 0, self.pc.PlayerReplicationInfo, True, 0)
        if not get_pc().PlayerReplicationInfo.bIsPartyLeader:
            respond = False
        if self.duration:
            Effect.running_effects.append(self.effect_name)
            self.is_running = True
            if response == "Finished":
                response = "Success"
            if respond:
                NotifyEffect(self.id, response, self.effect_name, self.pc, self.duration * 1000)
        else:
            global effect_instances
            effect_instances.remove(self)
            if respond:
                NotifyEffect(self.id, response, self.effect_name, self.pc)

    def stop_effect(self, response: str = "Finished", respond:bool = True): #available responses: https://developer.crowdcontrol.live/sdk/simpletcp/structure.html#effect-instance-messages
        self.is_running = False
        Effect.running_effects.remove(self.effect_name)
        if not get_pc().PlayerReplicationInfo.bIsPartyLeader:
            respond = False
        if respond:
            NotifyEffect(self.id, response, self.effect_name, self.pc)
        if self.duration:
            hud = self.pc.GetHUDMovie()
            if hud != None:
                hud.ClearTrainingText()
                hud.AddTrainingText(f"{self.display_name}", "Crowd Control", 3.5 * ENGINE.GetCurrentWorldInfo().TimeDilation, unrealsdk.make_struct("Color"), "", False, 0, self.pc.PlayerReplicationInfo, True, 0)


    def on_map_change(self):
        #runs as soon as the loading screen finishes
        pass

    def map_change_finalized(self):
        #runs once the player can see
        pass