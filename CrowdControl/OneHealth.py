import unrealsdk
from mods_base import get_pc, ENGINE
from ui_utils import show_hud_message
from .Utils import AmIHost, GetPlayerCharacter
from .Effect import Effect


class SetOneHP(Effect):
    id = 0
    effect_name = "1_health"
    def run_effect(self):
        if AmIHost(): # if we are host just do the effect normally, otherwise we have to ask the host to do it for us
            GetPlayerCharacter(get_pc()).OakDamageComponent.SetCurrentShield(0)
            GetPlayerCharacter(get_pc()).OakDamageComponent.SetCurrentHealth(1)
            show_hud_message("Hunt 'Rewards'", "Dont die", 3.5 * ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation)
        else:
            get_pc().ServerChangeName(f"CrowdControl-{get_pc().PlayerState.PlayerID}-1_health-{self.id}")
        return super().run_effect()