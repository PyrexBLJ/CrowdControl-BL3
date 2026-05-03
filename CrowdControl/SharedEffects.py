
from .Effect import Effect
from unrealsdk import find_object, make_struct, find_all, find_class, construct_object #type:ignore
from mods_base import get_pc, ENGINE #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct #type: ignore
from unrealsdk.hooks import Type, add_hook, remove_hook #type: ignore
from typing import Any
from .Utils import AmIHost, SendToHost, GetPlayerCharacter, SpawnLoot, SpawnPawn
import random


class SpawnLootEffect(Effect):
    """
    to add to this effect, add your loot pool to the dict in Utils and make a note on how many should spawn
    """
    effect_name = "spawnloot"
    display_name = "Spawning Some Loot"

    def run_effect(self):
        if AmIHost():
            if not self.pc:
                pawn = get_pc().Pawn
            else:
                pawn = self.pc.Pawn

            SpawnLoot(self.args[0], int(self.args[1]), pawn)
        else:
            SendToHost(self)
        return super().run_effect()
    

class SpawnEnemyEffect(Effect):
    """
    to add to this effect add the enemy name to the dict in utils and make a note on how many should spawn
    you can also spawn enemies in your own effects by using the SpawnEnemy function in utils
    """
    effect_name = "spawnenemy"
    display_name = "Spawning an Enemy"

    def run_effect(self):
        if AmIHost():
            if not self.pc:
                pc = get_pc()
            else:
                pc = self.pc

            #SpawnPawn(self.args[0], int(self.args[1]), pc)
        else:
            SendToHost(self)
        return super().run_effect()
    
class SpawnEnemyDupeEffect(Effect):
    """
    to add to this effect add the enemy name to the dict in utils and make a note on how many should spawn
    you can also spawn enemies in your own effects by using the SpawnEnemy function in utils
    """
    effect_name = "spawn-enemy"
    display_name = "Spawning an Enemy"

    def run_effect(self):
        if AmIHost():
            if not self.pc:
                pc = get_pc()
            else:
                pc = self.pc

            SpawnPawn(self.args[0], self.quantity if self.quantity != None else 1, pc)
        else:
            SendToHost(self)
        return super().run_effect()
    
class GiveCurrencyEffect(Effect):
    effect_name = "givecurrency"
    display_name = "Added Currency"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            if self.args[0] == "Eridium":
                currency = 1
            elif self.args[0] == "Cash":
                currency = 0
            elif self.args[0] == "SeraphCrystal":
                currency = 2
            elif self.args[0] == "TorgueToken":
                currency = 4
            else:
                currency = 0 #default to money ig

            self.pc.PlayerReplicationInfo.Currency[currency].CurrentAmount += int(self.args[1])
            self.display_name = f"Gave {str(self.args[1])} {str(self.args[0])}"
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    

used_names: list = []
buddy_watch_running: bool = False
spawned_friendlies: list = []

class HypeTrain(Effect):
    effect_name = "event-hype-train"
    display_name = "Hype Train"

    possible_enemies = [
        "captainflynt",
        "cassius",
        "wilhelm",
        "knuckledragger",
        "steve",
        "savagelee",
        "madmike",
        "sonofmothrakk",
        "kingmong",
        "tumbaa",
    ]
    
    def keep_track_of_friendlies(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
        global used_names, buddy_watch_running, spawned_friendlies
        if str(obj) in spawned_friendlies:
            spawned_friendlies.remove(str(obj))
            try:
                used_names.remove(str(obj.BalanceDefinitionState.AIPawnBalanceDefinition.PlayThroughs[0].DisplayName))
            except:
                pass
        if len(spawned_friendlies) == 0:
            used_names = []
            #print("stopping hype train hook")
            remove_hook("Engine.Pawn:UnPossessed", Type.PRE, "keep_track_of_friendlies_hook")
            buddy_watch_running = False
        return None

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            global used_names, buddy_watch_running, spawned_friendlies
            if self.sourcedetails["level"] == 1:
                self.display_name = "Hype Train Started!"
            else:
                self.display_name = f"Hype Train Has Reached Level {self.sourcedetails["level"]}"

            possible_names: list = []

            for name in self.sourcedetails["top_contributions"]:
                possible_names.append(name["user_name"])

            possible_names.append(self.sourcedetails["last_contribution"]["user_name"])

            final_name = ""

            name_found: bool = False
            all_names_used: bool = False
            i = 0
            while not name_found and not all_names_used:
                picked_name = possible_names[i]
                if picked_name in used_names:
                    i += 1
                    if i > len(possible_names):
                        
                        all_names_used = True
                        final_name = possible_names[random.randint(0, len(possible_names) - 1)]
                else:
                    final_name = picked_name
                    used_names.append(picked_name)
                    name_found = True

            try:
                enemy = self.possible_enemies[random.randint(0, len(self.possible_enemies) - 1)]
                print(f"Spawning {enemy}")
                actor = SpawnPawn(enemy, 1, self.pc, final_name, True, 10)
                print(actor)
                if actor[0] == None:
                    return super().run_effect("Failed", respond)
                
                spawned_friendlies.append(str(actor[0]))

                
                if buddy_watch_running == False:
                    add_hook("Engine.Pawn:UnPossessed", Type.PRE, "keep_track_of_friendlies_hook", self.keep_track_of_friendlies)
                    buddy_watch_running = True

            except:
                return super().run_effect("Failed", respond)
        else:
            SendToHost(self)


        return super().run_effect(response, respond)