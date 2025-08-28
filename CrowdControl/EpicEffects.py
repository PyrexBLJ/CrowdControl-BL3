import unrealsdk
import random
from mods_base import get_pc, ENGINE
from unrealsdk import find_object, make_struct, find_all, find_class
from ui_utils import show_hud_message
from .Utils import AmIHost, GetPlayerCharacter
from .Effect import Effect


class HighsLows(Effect):
    effect_name = "HighsLows"
    display_name = "Highs And Lows"
    def run_effect(self):
        if AmIHost():
            self.pc.Pawn.K2_GetActorLocation()
            self.pc.Pawn.K2_GetActorRotation()
            loc = make_struct("Vector", X=self.pc.pawn.K2_GetActorLocation().X, Y=self.pc.pawn.K2_GetActorLocation().Y, Z=self.pc.pawn.K2_GetActorLocation().Z + random.randrange(-10000, 75000))
            rot = self.pc.pawn.K2_GetActorRotation()
            self.pc.Pawn.K2_TeleportTo(loc,rot)
        else:
            get_pc().ServerChangeName(f"CrowdControl-{get_pc().PlayerState.PlayerID}-HighsLows-{self.id}")
        return super().run_effect()