import unrealsdk
import random
import math
from mods_base import get_pc, ENGINE
from unrealsdk import find_object, make_struct, find_all, find_class
from ui_utils import show_hud_message
from .Utils import AmIHost, GetPlayerCharacter
from .Effect import Effect


class HighsLows(Effect):
    effect_name = "HighsLows"
    display_name = "Highs And Lows"
    def highsandlows(self):
        self.pc.Pawn.K2_GetActorLocation()
        self.pc.Pawn.K2_GetActorRotation()
        loc = make_struct("Vector", X=get_pc().pawn.K2_GetActorLocation().X + 500 * math.cos(math.radians((get_pc().pawn.K2_GetActorRotation().Yaw))), Y=get_pc().pawn.K2_GetActorLocation().Y + 500 * math.sin(math.radians((get_pc().pawn.K2_GetActorRotation().Yaw))), Z=get_pc().pawn.K2_GetActorLocation().Z - 112)
        rot = make_struct("Rotator", Roll =0, Pitch=0, Yaw=get_pc().pawn.K2_GetActorRotation().Yaw-180)
        print(loc)
        self.pc.Pawn.K2_TeleportTo(loc,rot)
        return super().run_effect()