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
            GetPlayerCharacter(self.pc).OakDamageComponent.SetCurrentShield(0)
            GetPlayerCharacter(self.pc).OakDamageComponent.SetCurrentHealth(1)
            #self.pc.DisplayRolloutNotification("Crowd Control", "Dont die", 3.5 * ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation)
        else:
            SendToHost(self)
        return super().run_effect()