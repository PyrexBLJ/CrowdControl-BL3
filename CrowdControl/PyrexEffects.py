from .Effect import Effect
from .Utils import GetPlayerCharacter


class NoGravity(Effect):
    effect_name = "no_gravity"
    display_name = "No Gravity"

    def run_effect(self):
        GetPlayerCharacter(self.pc).OakCharacterMovement.GravityScale = 0.0
        return super().run_effect()

    def stop_effect(self):
        GetPlayerCharacter(self.pc).OakCharacterMovement.GravityScale = 1.0
        return super().stop_effect()