import unrealsdk
from mods_base import get_pc, ENGINE
from ui_utils import show_hud_message
from .Utils import AmIHost, GetPlayerCharacter, SendToHost
from .Effect import Effect


class SetOneHP(Effect):
    #id = 0
    effect_name = "1_health"
    display_name = "One Health"
    def run_effect(self):
        if AmIHost(): # if we are host just do the effect normally, otherwise we have to ask the host to do it for us
            for pool in self.pc.ResourcePoolManager.ResourcePools:
                if pool != None:
                    if pool.Class.Name == "ShieldResourcePool":
                        pool.SetCurrentValue(0)
                    if pool.Class.Name == "HealthResourcePool":
                        pool.SetCurrentValue(1)
        else:
            SendToHost(self)
        return super().run_effect()
    
    def stop_effect(self, response = "Finished", respond = True):
        #let it respond like normal
        return super().stop_effect(response, respond)