
from .Effect import Effect
from unrealsdk import find_object, make_struct, find_all, find_class #type:ignore
from mods_base import get_pc
from .Utils import SpawnLoot


class SpawnLootEffect(Effect):
    """
    to add to this effect, add your loot pool to the dict in Utils and make a note on how many should spawn
    """
    effect_name = "spawnloot"

    def run_effect(self):
        if not self.pc:
            pawn = get_pc().Pawn
        else:
            pawn = self.pc.Pawn

        SpawnLoot(self.args[0], int(self.args[1]), pawn)
        return super().run_effect()