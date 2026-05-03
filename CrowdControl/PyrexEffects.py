from .Effect import Effect
from .Utils import GetPlayerCharacter, AmIHost, SendToHost, SpawnPawn, SpawnChubby, Spawnlootboi, Circle, SpawnIO, InFrontOfPlayer
from .Comms import SetEffectStatus, NotifyEffect
from .EnemySpawnerLists import Chubbies, lootbois
from mods_base import get_pc, ENGINE #type: ignore
import unrealsdk #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct, IGNORE_STRUCT #type: ignore
from unrealsdk.hooks import Type, add_hook, remove_hook, Block #type: ignore
from typing import Any
import random
import time

viewer_badass_cooldown_enabled: bool = False
viewer_badass_cooldown_start_time: float = 0.0

class NoGravity(Effect):
    effect_name = "low_gravity"
    display_name = "Low Player Gravity"

    def run_effect(self, response = "Finished"):
        if AmIHost():
            GetPlayerCharacter(self.pc).CustomGravityScaling = 0.1
        else:
            SendToHost(self)
        self.display_name = "Low Gravity"
        return super().run_effect(response)

    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            GetPlayerCharacter(self.pc).CustomGravityScaling = 1.0
        self.display_name = "Normal Gravity"
        return super().stop_effect(response, respond)
    
class InstantDeath(Effect):
    effect_name = "instant_death"
    display_name = "Instant Death"

    def run_effect(self):
        if AmIHost():
            self.pc.CausePlayerDeath(False)
        else:
            SendToHost(self)
        return super().run_effect()
    
class DropEntireInventory(Effect):
    effect_name = "drop_entire_inventory"
    display_name = "Goodbye Inventory"

    def run_effect(self):
        if AmIHost():
            for item in GetPlayerCharacter(self.pc).EquippedItems:
                if item != None:
                    GetPlayerCharacter(self.pc).InvManager.InventoryUnreadied(item, True)

            # man this is cooked
            for weapon in range(len(GetPlayerCharacter(self.pc).HolsteredWeaponSlots) * 2 + 2):
                GetPlayerCharacter(self.pc).InvManager.InventoryUnreadied(GetPlayerCharacter(self.pc).HolsteredWeaponSlots[0], True)

            GetPlayerCharacter(self.pc).InvManager.InventoryUnreadied(GetPlayerCharacter(self.pc).Weapon, True)
            
            throwindex = 0
            items = len(GetPlayerCharacter(self.pc).InvManager.Backpack)

            while items > 0:
                if GetPlayerCharacter(self.pc).InvManager.Backpack[throwindex].CanThrow():
                    GetPlayerCharacter(self.pc).InvManager.ThrowBackpackInventory(GetPlayerCharacter(self.pc).InvManager.Backpack[throwindex])
                else:
                    throwindex += 1
                items -= 1
            
            
            #this was so much easier in bl3 bruh
        else:
            SendToHost(self)
        return super().run_effect()
    
class DeleteGroundItems(Effect):
    effect_name = "delete_ground_items"

    def run_effect(self):
        if AmIHost():
            willowglobals = unrealsdk.find_class("WillowGlobals").ClassDefaultObject.GetWillowGlobals()
            ognumberofitems: int = len(willowglobals.PickupList)
            numberofitems: int = len(willowglobals.PickupList)
            deleteindex: int = 0
            combinedvalue: int = 0
            while numberofitems > 0:
                if not willowglobals.PickupList[deleteindex].bIsMissionItem:
                    try:
                        combinedvalue += willowglobals.PickupList[deleteindex].Inventory.MonetaryValue
                    except:
                        pass
                    willowglobals.PickupList[deleteindex].Behavior_Destroy()
                    numberofitems -= 1
                else:
                    deleteindex += 1
                    numberofitems -= 1
            
            for player in ENGINE.GetCurrentWorldInfo().GRI.PRIArray:
                player.Currency[0].CurrentAmount += combinedvalue
            self.display_name = f"{ognumberofitems - deleteindex} Items Deleted"
            combinedvalue = 0
        else:
            SendToHost(self)
        return super().run_effect()
    
class DropHeldWeapon(Effect):
    effect_name = "drop_held_weapon"
    display_name = "Drop Held Weapon"

    def run_effect(self):
        if AmIHost():
            self.pc.ThrowWeapon()
        else:
            SendToHost(self)
        return super().run_effect()
    
class DropEquippedShield(Effect):
    effect_name = "drop_equipped_shield"
    display_name = "Drop Equipped Shield"

    def run_effect(self):
        if AmIHost():
            shieldToThrow = None
            for item in GetPlayerCharacter(self.pc).EquippedItems:
                if item != None:
                    if "WillowShield" in str(item.Class):
                        shieldToThrow = item.DefinitionData.UniqueId
                        GetPlayerCharacter(self.pc).InvManager.InventoryUnreadied(item, True)
            for thing in GetPlayerCharacter(self.pc).InvManager.Backpack:
                if thing.DefinitionData.UniqueId == shieldToThrow:
                    GetPlayerCharacter(self.pc).InvManager.ThrowBackpackInventory(thing)
        else:
            SendToHost(self)
        return super().run_effect()
    
class NoAmmo(Effect):
    effect_name = "no_ammo"
    display_name = "No Ammo"

    def run_effect(self):
        if AmIHost():
            GetPlayerCharacter(self.pc).Weapon.AmmoPool.Data.SetCurrentValue(0)
        else:
            SendToHost(self)
        return super().run_effect()
    
class ResetSkillTrees(Effect):
    effect_name = "reset_skill_trees"
    display_name = "Reset Skill Trees"

    def run_effect(self):
        if AmIHost():
            self.pc.PlayerReplicationInfo.GeneralSkillPoints += self.pc.ResetSkillTree(True)
        else:
            SendToHost(self)
        return super().run_effect()
    
class FastGameSpeed(Effect):
    effect_name = "fast_game_speed"
    display_name = "4x Speed"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            ENGINE.GetCurrentWorldInfo().TimeDilation = 4.0
        else:
            SendToHost(self)
        self.display_name = "4x Speed"
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            ENGINE.GetCurrentWorldInfo().TimeDilation = 1.0
        self.display_name = "Normal Speed"
        return super().stop_effect(response, respond)
    
class SlowGameSpeed(Effect):
    effect_name = "slow_game_speed"
    display_name = "0.5x Speed"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            ENGINE.GetCurrentWorldInfo().TimeDilation = 0.5
        else:
            SendToHost(self)
            self.display_name = "0.5x Speed"
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            ENGINE.GetCurrentWorldInfo().TimeDilation = 1.0
        self.display_name = "Normal Speed"
        return super().stop_effect(response, respond)
    
class FlyMode(Effect):
    effect_name = "fly_mode"
    display_name = "I can fly!"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            pawn = self.pc.Pawn
            self.pc.Pawn.LandMovementState = "PlayerFlying"
            self.pc.Unpossess()
            self.pc.Possess(pawn, False)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            pawn = self.pc.Pawn
            self.pc.Pawn.LandMovementState = "PlayerWalking"
            self.pc.Unpossess()
            self.pc.Possess(pawn, False)
        self.display_name = "rip flight"
        return super().stop_effect(response, respond)
    
class FullAmmo(Effect):
    effect_name = "full_ammo"
    display_name = "Ammo Refilled!"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            for ammopool in self.pc.ResourcePoolManager.ResourcePools:
                if ammopool is None:
                    continue
                if ammopool.Class.Name in ("AmmoResourcePool") or ammopool.Definition.Resource.Name == "Ammo_Grenade_Protean":
                    if ammopool.Definition.Resource.Name == "Ammo_Rocket_Launcher":
                        ammopool.SetCurrentValue(ammopool.GetMaxValue(False))
                    elif ammopool.Definition.Resource.Name == "Ammo_Grenade_Protean":
                        ammopool.SetCurrentValue(ammopool.GetMaxValue(False))
                    else:
                        ammopool.SetCurrentValue(ammopool.GetMaxValue(False))
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
class SpawnTubby(Effect):
    effect_name = "spawn_chubby"
    display_name = "Spawning Chubby"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            SpawnChubby(self.quantity, self.pc)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
class SpawnLootMidget(Effect):
    effect_name = "spawn_lootboi"
    display_name = "Spawning Loot Midget"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            Spawnlootboi(self.quantity, self.pc)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
class OneShotKills(Effect):
    effect_name = "one_shot"
    display_name = "One Shot Kills"

    def instakill(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
        if obj.HealthPool.Data.GetCurrentValue() > 1 and not obj.bIsDead:
            if obj.Allegiance.ConsidersEnemy(unrealsdk.find_object("PawnAllegiance", "GD_AI_Allegiance.Allegiance_Player")):
                obj.HealthPool.Data.SetCurrentValue(0)
        return None

    def run_effect(self):
        if AmIHost():
            add_hook("WillowGame.WillowAIPawn:TakeDamage", Type.POST, "insta_kill_hook", self.instakill)
        else:
            SendToHost(self)
            self.display_name = "One Shot Kills"
        return super().run_effect()
    
    def stop_effect(self):
        if AmIHost():
            remove_hook("WillowGame.WillowAIPawn:TakeDamage", Type.POST, "insta_kill_hook")
            self.display_name = "One Shot Kills Off"
        return super().stop_effect()
    
class DefinitelyRealViewerBadass(Effect):
    effect_name = "viewer_badass"
    display_name = "Summoning Viewer Badass"

    viewer_pawn = None

    possible_enemies = [
        "docmercy",
        "muscles",
        "smashhead",
        "bonehead2",
        "madmike",
        "kingmong",
        "savagelee",
        "sheriffoflynchwood",
        "blackqueen",
        "oldslappy",
        "spycho",
        "ralph",
        "gettle",
        "assassinrouf",
        "tectorhodunk",
    ]

    def cooldown(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
        global viewer_badass_cooldown_enabled, viewer_badass_cooldown_start_time
        if viewer_badass_cooldown_enabled == True:
            from . import ViewerBadassCooldown
            if (viewer_badass_cooldown_start_time + (int(ViewerBadassCooldown.value) * 60)) <= time.time():
                SetEffectStatus("viewer_badass", 0x82, self.pc)
                viewer_badass_cooldown_enabled = False
                remove_hook("WillowGame.WillowGameViewportClient:Tick", Type.PRE, "viewer_badass_cooldown")
        return None
    
    def trackdeaths(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
        if str(obj) == str(self.viewer_pawn):
            global viewer_badass_cooldown_enabled, viewer_badass_cooldown_start_time
            viewer_badass_cooldown_start_time = time.time()
            self.display_name = f"{self.viewer} Died"
            from . import ViewerBadassCooldown
            if int(ViewerBadassCooldown.value) > 0:
                hud = self.pc.GetHUDMovie()
                if hud != None:
                    hud.ClearTrainingText()
                    hud.AddTrainingText(f"{self.display_name}. {ViewerBadassCooldown.value} Minute Cooldown Started.", "Crowd Control", 3.5 * ENGINE.GetCurrentWorldInfo().TimeDilation, unrealsdk.make_struct("Color"), "", False, 0, self.pc.PlayerReplicationInfo, True, 0)
            else:
                hud = self.pc.GetHUDMovie()
                if hud != None:
                    hud.ClearTrainingText()
                    hud.AddTrainingText(f"{self.display_name}.", "Crowd Control", 3.5 * ENGINE.GetCurrentWorldInfo().TimeDilation, unrealsdk.make_struct("Color"), "", False, 0, self.pc.PlayerReplicationInfo, True, 0)
            add_hook("WillowGame.WillowGameViewportClient:Tick", Type.PRE, "viewer_badass_cooldown", self.cooldown)
            remove_hook("Engine.Pawn:UnPossessed", Type.PRE, "viewer_badass_death_check")
        return None
    
    def run_effect(self):
        global viewer_badass_cooldown_enabled
        if viewer_badass_cooldown_enabled:
            NotifyEffect(self.id, "Retry", self.effect_name, self.pc)
            return
        
        if AmIHost():
            self.display_name = f"Summoning {self.viewer}"
            actor = SpawnPawn(self.possible_enemies[random.randint(0, len(self.possible_enemies) - 1)], 1, self.pc, self.viewer, False, 3)
            if actor[0] != None:
                self.viewer_pawn = actor[0]
                SetEffectStatus(self.effect_name, 0x83, self.pc)
                add_hook("Engine.Pawn:UnPossessed", Type.PRE, "viewer_badass_death_check", self.trackdeaths)
                viewer_badass_cooldown_enabled = True
                return super().run_effect()
            else:
                return super().run_effect("Retry")
        else:
            SendToHost(self)
            return super().run_effect()
        
#py get_pc().PostAkEvent(unrealsdk.find_object("AkEvent", "Ake_VO_Episode_15.Ak_Play_VO_Ep15_Pt4_07_echo_Brick")) buzzards nest line

class FallDamage(Effect):
    effect_name = "fall_damage"
    display_name = "Fall Damage"

    def dofalldamage(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
        fallvelocity = min(obj.Velocity.Z * -1, 4000)
        if fallvelocity > 950:
            fallvelocity -= 1000

            totalhp = obj.HealthPool.Data.GetMaxValue() + obj.ShieldArmor.Data.GetMaxValue()
            shield = obj.ShieldArmor.Data.GetCurrentValue()
            health = obj.HealthPool.Data.GetCurrentValue()

            fallpercentage = (fallvelocity / 3000) * 100
            maxfalldamage = totalhp * (50 / 100)
            totaldamage = maxfalldamage * fallpercentage / 100

            if shield - totaldamage < 0:
                print(f"shield damage: {shield}")
                totaldamage -= shield
                print(f"health damage: {totaldamage}")
                obj.ShieldArmor.Data.SetCurrentValue(0)
                obj.HealthPool.Data.SetCurrentValue(health - totaldamage)
            else:
                print(f"shield damage: {totaldamage}")
                obj.ShieldArmor.Data.SetCurrentValue(shield - totaldamage)
        return None
    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            add_hook("WillowGame.WillowPlayerPawn:Landed", Type.PRE, "fall_damage_hook", self.dofalldamage)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            remove_hook("WillowGame.WillowPlayerPawn:Landed", Type.PRE, "fall_damage_hook")
        self.display_name = "No More Fall Damage"
        return super().stop_effect(response, respond)

class GambaTime(Effect):
    effect_name = "gamba_time"
    display_name = "Lets go gambling!"

    slots = ["normalslotmachine", "eridiumslotmachine", "torgueslotmachine"]

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            counter = 0
            for spot in Circle(GetPlayerCharacter(self.pc).Location, 1, 0, 8, 250, -75, False):
                yaw = 49149
                PCRot = unrealsdk.make_struct("Rotator", Pitch = 0, Yaw= yaw, Roll= 0)
                if counter <= 2:
                    SpawnIO(self.slots[counter], 1, self.pc, spot, PCRot)
                counter += 1
        else:
            SendToHost(self)
        return super().run_effect(response, respond)

class StretchTime(Effect):
    effect_name = "stretch_time"
    display_name = "Stretch Time. Look Up!"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            GetPlayerCharacter(self.pc).ViewPitchMax = 65535
            GetPlayerCharacter(self.pc).ViewPitchMin = -65535
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            GetPlayerCharacter(self.pc).ViewPitchMax = 16383
            GetPlayerCharacter(self.pc).ViewPitchMin = -16384
        self.display_name = "aight good stretch"
        return super().stop_effect(response, respond)
    
class PainfulPlants(Effect):
    effect_name = "painful_plants"
    display_name = "Painful Plants"

    plants = ["shockcactus", "firemelon", "acidolus"]

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            PCRot = GetPlayerCharacter(self.pc).Controller.Rotation
            PCLoc = Circle(GetPlayerCharacter(self.pc).Location, 3, 4, 7, 700, 0, False)
            for net in PCLoc:
                SpawnIO(random.choice(self.plants), 1, self.pc, net, PCRot)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
class SpawnCandies(Effect):
    effect_name = "spawn_candy"
    display_name = "Have some candy"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            obj = unrealsdk.construct_object("Behavior_SpawnLootAroundPoint", ENGINE.Outer)
            obj.ItemPools = [unrealsdk.find_object("ItemPoolDefinition", "GD_Flax_ItemPools.Items.ItemPool_Flax_BlueCandy"), 
                                    unrealsdk.find_object("ItemPoolDefinition", "GD_Flax_ItemPools.Items.ItemPool_Flax_GreenCandy"), 
                                    unrealsdk.find_object("ItemPoolDefinition", "GD_Flax_ItemPools.Items.ItemPool_Flax_RedCandy"), 
                                    unrealsdk.find_object("ItemPoolDefinition", "GD_Flax_ItemPools.Items.ItemPool_Flax_YellowCandy"), ]
            obj.SpawnVelocityRelativeTo = 0
            obj.bTorque = False
            obj.CircularScatterRadius = 300
            obj.CustomLocation = unrealsdk.make_struct("AttachmentLocationData", Location=InFrontOfPlayer(self.pc, 200), AttachmentBase=None, AttachmentName="")
            obj.ApplyBehaviorToContext(get_pc(), IGNORE_STRUCT, None, None, None, IGNORE_STRUCT)
        return super().run_effect(response, respond)

class FastMovement(Effect):
    effect_name = "fast_movement"
    display_name = "Fast Movement"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            self.pc.ConsoleCommand("set willowplayerpawn groundspeed 1200")
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            self.pc.ConsoleCommand("set willowplayerpawn groundspeed 440")
        return super().stop_effect(response, respond)
    
class SpawnWisps(Effect):
    effect_name = "spawn_wisps"
    display_name = "Have some wisp jars"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            obj = unrealsdk.construct_object("Behavior_SpawnLootAroundPoint", ENGINE.Outer)
            obj.ItemPools = [unrealsdk.find_object("ItemPoolDefinition", "GD_Flax_ItemPools.Items.ItemPool_Flax_Wisp"), 
                                    unrealsdk.find_object("ItemPoolDefinition", "GD_Flax_ItemPools.Items.ItemPool_Flax_Wisp"), 
                                    unrealsdk.find_object("ItemPoolDefinition", "GD_Flax_ItemPools.Items.ItemPool_Flax_Wisp"), 
                                    unrealsdk.find_object("ItemPoolDefinition", "GD_Flax_ItemPools.Items.ItemPool_Flax_Wisp"), ]
            obj.SpawnVelocityRelativeTo = 0
            obj.bTorque = False
            obj.CircularScatterRadius = 300
            obj.CustomLocation = unrealsdk.make_struct("AttachmentLocationData", Location=InFrontOfPlayer(self.pc, 200), AttachmentBase=None, AttachmentName="")
            obj.ApplyBehaviorToContext(get_pc(), IGNORE_STRUCT, None, None, None, IGNORE_STRUCT)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
class LowWorldGravity(Effect):
    effect_name = "low_world_gravity"
    display_name = "Low World Gravity"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            ENGINE.GetCurrentWorldInfo().WorldGravityZ = -75
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            ENGINE.GetCurrentWorldInfo().WorldGravityZ = -500
        self.display_name = "Normal World Gravity"
        return super().stop_effect(response, respond)