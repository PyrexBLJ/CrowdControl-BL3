from .Effect import Effect
from .Utils import GetPlayerCharacter
import unrealsdk
from mods_base import get_pc


class NoGravity(Effect):
    effect_name = "no_gravity"

    def run_effect(self):
        GetPlayerCharacter(self.pc).OakCharacterMovement.GravityScale = 0.0
        return super().run_effect()

    def stop_effect(self):
        GetPlayerCharacter(self.pc).OakCharacterMovement.GravityScale = 1.0
        return super().stop_effect()