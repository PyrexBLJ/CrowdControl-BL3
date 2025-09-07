import unrealsdk
import random
from mods_base import get_pc, ENGINE
from unrealsdk import find_object, make_struct, find_all, find_class
from ui_utils import show_hud_message
from .Utils import AmIHost, GetPlayerCharacter, SendToHost
from .Effect import Effect


class HighsLows(Effect):
    effect_name = "HighsLows"
    display_name = "Highs And Lows"
    def run_effect(self):
        if AmIHost():
            self.pc.Pawn.K2_GetActorLocation()
            self.pc.Pawn.K2_GetActorRotation()
            loc = make_struct("Vector", X=self.pc.pawn.K2_GetActorLocation().X, Y=self.pc.pawn.K2_GetActorLocation().Y, Z=self.pc.pawn.K2_GetActorLocation().Z + random.randrange(-60000, 75000))
            rot = self.pc.pawn.K2_GetActorRotation()
            self.pc.Pawn.K2_TeleportTo(loc,rot)
        else:
            SendToHost(self)
        return super().run_effect()

class NoSplash(Effect):
    effect_name = "NoSplash"
    display_name = "No Splash Damage"
    def run_effect(self):
        if AmIHost():
            GetPlayerCharacter(self.pc).OakDamageComponent.RadiusDamageTakenMultiplier.Value = 0
            GetPlayerCharacter(self.pc).OakDamageComponent.RadiusDamageTakenMultiplier.BaseValue = 0
        else:
            SendToHost(self)
        return super().run_effect()
    
    def stop_effect(self):
        if AmIHost():
            GetPlayerCharacter(self.pc).OakDamageComponent.RadiusDamageTakenMultiplier.Value = 1
            GetPlayerCharacter(self.pc).OakDamageComponent.RadiusDamageTakenMultiplier.BaseValue = 1
        return super().stop_effect()
