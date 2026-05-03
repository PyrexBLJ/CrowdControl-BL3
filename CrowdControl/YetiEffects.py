from .Effect import Effect
from typing import Any
from mods_base import ENGINE, get_pc
from unrealsdk import find_object, make_struct, find_all, find_class, load_package, construct_object
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct, IGNORE_STRUCT
from unrealsdk.hooks import Type, add_hook, remove_hook, prevent_hooking_direct_calls, Block
from .Utils import blacklist_teams, GetPawnList, AmIHost, SendToHost, GetPlayerCharacter
import random

class LaunchPlayer(Effect):
    effect_name = "launch_player"
    display_name = "Launch Player"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            GetPlayerCharacter(self.pc).DoJump(False)
            GetPlayerCharacter(self.pc).Velocity.Z += 100000
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
class SillyScales(Effect):
    effect_name = "silly_scales"
    display_name = "Silly Scales"

    def SetRandomizedScale(self, pawn) -> None:
        RandomX = random.uniform(0.2, 2.5)
        changescale = construct_object("Behavior_ChangeScale", ENGINE.Outer)
        changescale.Scale = RandomX
        changescale.ApplyBehaviorToContext(pawn, IGNORE_STRUCT, None, None, None, IGNORE_STRUCT)
        updatecollision = construct_object("Behavior_UpdateCollision", ENGINE.Outer)
        updatecollision.ApplyBehaviorToContext(pawn, IGNORE_STRUCT, None, None, None, IGNORE_STRUCT)
    
    def SillyScalesPawnPossessed(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> Any:
        if not obj.IsHumanControlled():
            self.SetRandomizedScale(obj)
    
    def run_effect(self, response = "Success", respond = True):
        add_hook("WillowGame.WillowPawn:PossessedBy", Type.POST, "SillyScalesPawnPossessed", self.SillyScalesPawnPossessed)
        for Pawn in GetPawnList(False):
            self.SetRandomizedScale(Pawn)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        remove_hook("WillowGame.WillowPawn:PossessedBy", Type.POST, "SillyScalesPawnPossessed")
        self.display_name = "No more silly scales"
        return super().stop_effect(response, respond)
    
class DisableJumping(Effect):
    effect_name = "disable_jumping"
    display_name = "Disable Jumping"

    def dodisablejumping(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> type[Block] | None:
        return Block, False
    
    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            add_hook("WillowGame.WillowPlayerPawn:CanJump", Type.PRE, "DisableJumping", self.dodisablejumping)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            remove_hook("WillowGame.WillowPlayerPawn:CanJump", Type.PRE, "DisableJumping")
            self.display_name = "Enable Jumping"
        return super().stop_effect(response, respond)
    
class HideWeapons(Effect):
    effect_name = "hide_weapons"
    display_name = "Hide Weapons"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            GetPlayerCharacter(self.pc).SetHidden(True)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            GetPlayerCharacter(self.pc).SetHidden(False)
        return super().stop_effect(response, respond)
    
class ClutterInventory(Effect):
    effect_name = "clutter_inventory"
    display_name = "Clutter Backpack"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            for i in range(25):
                items = []
                _, items = find_class("ItemPool").ClassDefaultObject.SpawnBalancedInventoryFromPool(find_object("ItemPoolDefinition", "GD_Itempools.GeneralItemPools.Pool_GunsAndGear"), self.pc.PlayerReplicationInfo.ExpLevel + self.pc.OverpowerChoiceValue, 2, GetPlayerCharacter(self.pc), [])
                GetPlayerCharacter(self.pc).InvManager.AddInventoryToBackpack(items[0])
        else:
            SendToHost(self)
        return super().run_effect(response, respond)