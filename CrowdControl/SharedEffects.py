
from .Effect import Effect
from unrealsdk import find_object, make_struct, find_all, find_class, construct_object #type:ignore
from mods_base import get_pc, ENGINE #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct #type: ignore
from unrealsdk.hooks import Type, add_hook, remove_hook #type: ignore
from typing import Any
from .Utils import SpawnLoot, SpawnEnemy, SpawnEnemyEx, AmIHost, SendToHost
from random import randint


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

            SpawnEnemy(self.args[0], int(self.args[1]), pc)
        else:
            SendToHost(self)
        return super().run_effect()
    

used_names: list = []
buddy_watch_running: bool = False
spawned_friendlies: list = []

class HypeTrain(Effect):
    effect_name = "event-hype-train"
    display_name = "Hype Train"

    possible_enemies = ["Badass CryptoSec Commando", 
                        "Badass Goliath", 
                        "Badass Psycho", 
                        "Badass Jabber", 
                        "Badass Wardog", 
                        "Badass Wraith",  
                        "Badass Major",
                        "Badass Loader",
                        "Super Badass Marauder",
                        "Dark Badass NOG",
                        "Elite Badass Ratch"]
    
    def keep_track_of_friendlies(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
        global used_names, buddy_watch_running, spawned_friendlies
        if str(obj) in spawned_friendlies:
            spawned_friendlies.remove(str(obj))
            try:
                used_names.remove(str(obj.TargetableComponent.TargetUIName.DisplayName))
            except:
                pass
        if len(spawned_friendlies) == 0:
            used_names = []
            print("stopping hype train hook")
            remove_hook("/Script/Engine.Pawn:ReceiveUnpossessed", Type.PRE, "keep_track_of_friendlies_hook")
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

            try:
                actor = SpawnEnemyEx(self.possible_enemies[randint(0, len(self.possible_enemies) - 1)], 1, self.pc)
                if actor == None:
                    return super().run_effect("Failed", respond)
                print(actor)
                spawned_friendlies.append(str(actor))
                lvl = actor.AIBalanceState.GetExperienceLevel()
                actor.AIBalanceState.SetExperienceLevel(lvl + 3)
                name = construct_object("GbxUIName", outer=ENGINE.Outer)

                name_found: bool = False
                all_names_used: bool = False
                i = 0
                while not name_found and not all_names_used:
                    picked_name = possible_names[i]
                    if picked_name in used_names:
                        i += 1
                        if i > len(possible_names):
                            print("all names have been used")
                            all_names_used = True
                            name.DisplayName = possible_names[randint(0, len(possible_names) - 1)]
                    else:
                        name.DisplayName = picked_name
                        used_names.append(picked_name)
                        name_found = True

                actor.SetCharacterUIName(name)
                if buddy_watch_running == False:
                    add_hook("/Script/Engine.Pawn:ReceiveUnpossessed", Type.PRE, "keep_track_of_friendlies_hook", self.keep_track_of_friendlies)
                    buddy_watch_running = True

            except:
                return super().run_effect("Failed", respond)
        else:
            SendToHost(self)


        return super().run_effect(response, respond)