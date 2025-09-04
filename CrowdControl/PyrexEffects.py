from .Effect import Effect
from .Utils import GetPlayerCharacter, AmIHost, SpawnEnemyEx, SendToHost
from .Comms import SetEffectStatus, NotifyEffect
from mods_base import get_pc, ENGINE #type: ignore
import unrealsdk #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct #type: ignore
from unrealsdk.hooks import Type, add_hook, remove_hook #type: ignore
from typing import Any
import random
import time
#
#
#   number of near crash outs trying to get comms and coop working properly: 4
#
#
viewer_badass_cooldown_enabled: bool = False
viewer_badass_cooldown_start_time: float = 0.0


class NoGravity(Effect):
    effect_name = "no_gravity"
    display_name = "No Gravity"

    def run_effect(self, response = "Finished"):
        if AmIHost():
            GetPlayerCharacter(self.pc).OakCharacterMovement.GravityScale = 0.0
        else:
            SendToHost(self)
        return super().run_effect(response)

    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            GetPlayerCharacter(self.pc).OakCharacterMovement.GravityScale = 1.0
        return super().stop_effect(response, respond)
    
class InstantDeath(Effect):
    effect_name = "instant_death"
    display_name = "Instant Death"

    def run_effect(self):
        if AmIHost():
            character = self.pc.OakCharacter
            if character == None:
                self.pc.AcknowledgedPawn.DamageComponent.SetCurrentHealth(0)
                GetPlayerCharacter(self.pc).OakDamageComponent.SetCurrentHealth(0)
                GetPlayerCharacter(self.pc).BPFightForYourLifeComponent.DownStateTimeExpired(self.pc.OakCharacter.BPFightForYourLifeComponent.DownTimeResourcePool)
            elif "IronBear" in str(character):
                self.pc.OakCharacter.OnExiting(True)
                GetPlayerCharacter(self.pc).OakDamageComponent.SetCurrentHealth(0)
                GetPlayerCharacter(self.pc).BPFightForYourLifeComponent.DownStateTimeExpired(self.pc.OakCharacter.BPFightForYourLifeComponent.DownTimeResourcePool)
            else:
                GetPlayerCharacter(self.pc).OakDamageComponent.SetCurrentHealth(0)
                GetPlayerCharacter(self.pc).BPFightForYourLifeComponent.DownStateTimeExpired(self.pc.OakCharacter.BPFightForYourLifeComponent.DownTimeResourcePool)
        else:
            SendToHost(self)
        return super().run_effect()
    
class DropEntireInventory(Effect):
    effect_name = "drop_entire_inventory"
    display_name = "Goodbye Inventory"

    def run_effect(self):
        if AmIHost():
            numofitems: int = len(GetPlayerCharacter(self.pc).GetInventoryComponent().InventoryList.Items)
            dropindex: int = 0
            while numofitems > 0:
                if GetPlayerCharacter(self.pc).GetInventoryComponent().InventoryList.Items[dropindex].PlayerDroppability == 0 and str(GetPlayerCharacter(self.pc).GetInventoryComponent().InventoryList.Items[dropindex].BaseCategoryDefinition) not in ("InventoryCategoryData'/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money'", "InventoryCategoryData'/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium'"):
                    GetPlayerCharacter(self.pc).GetInventoryComponent().ServerDropItem(GetPlayerCharacter(self.pc).GetInventoryComponent().InventoryList.Items[dropindex].Handle, self.pc.Pawn.K2_GetActorLocation(), self.pc.K2_GetActorRotation())
                else:
                    dropindex += 1
                numofitems -= 1
        else:
            SendToHost(self)
        return super().run_effect()
    
class DeleteGroundItems(Effect):
    effect_name = "delete_ground_items"

    def run_effect(self):
        if AmIHost():
            ognumberofitems: int = len(ENGINE.GameViewport.World.GameState.PickupList)
            numberofitems: int = len(ENGINE.GameViewport.World.GameState.PickupList)
            deleteindex: int = 0
            combinedvalue: int = 0
            while numberofitems > 0:
                if "RarityData_00_Mission" not in str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex].AssociatedInventoryRarityData) and "GunRack" not in str(ENGINE.GameViewport.World.GameState.PickupList[deleteindex]):
                    try:
                        combinedvalue += ENGINE.GameViewport.World.GameState.PickupList[deleteindex].CachedInventoryBalanceComponent.MonetaryValue
                    except:
                        pass
                    ENGINE.GameViewport.World.GameState.PickupList[deleteindex].K2_DestroyActor_DEPRECATED()
                    numberofitems -= 1
                else:
                    deleteindex += 1
                    numberofitems -= 1
            
            for player in ENGINE.GameViewport.World.GameState.PlayerArray:
                player.Owner.ServerAddCurrency(combinedvalue, unrealsdk.find_object("InventoryCategoryData", "/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money"))
            self.display_name = f"{ognumberofitems - deleteindex} Items Deleted"
            combinedvalue = 0
        else:
            SendToHost(self)
        return super().run_effect()
    
class FallDamage(Effect):
    effect_name = "fall_damage"
    display_name = "Fall Damage"

    def dofalldamage(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
        fallvelocity = min(obj.OakCharacterMovement.Velocity.Z * -1, 4000)
        if fallvelocity > 950:
            fallvelocity -= 1000

            totalhp = obj.OakDamageComponent.GetTotalMaxHealth()
            shield = obj.OakDamageComponent.GetCurrentShield()
            health = obj.OakDamageComponent.GetCurrentHealth()

            fallpercentage = (fallvelocity / 3000) * 100
            maxfalldamage = totalhp * (50 / 100)
            totaldamage = maxfalldamage * fallpercentage / 100

            if shield - totaldamage < 0:
                totaldamage -= shield
                obj.OakDamageComponent.SetCurrentShield(0)
                obj.OakDamageComponent.SetCurrentHealth(health - totaldamage)
            else:
                obj.OakDamageComponent.SetCurrentShield(shield - totaldamage)
        return None
    
    def run_effect(self):
        if AmIHost():
            add_hook("/Game/PlayerCharacters/_Shared/_Design/Character/BPChar_Player.BPChar_Player_C:OnLanded", Type.PRE, "fall_damage_hook", self.dofalldamage)
        else:
            SendToHost(self)
        return super().run_effect()
    
    def stop_effect(self):
        if AmIHost():
            remove_hook("/Game/PlayerCharacters/_Shared/_Design/Character/BPChar_Player.BPChar_Player_C:OnLanded", Type.PRE, "fall_damage_hook")
        return super().stop_effect()
    
class DropHeldWeapon(Effect):
    effect_name = "drop_held_weapon"
    display_name = "Drop Held Weapon"

    def run_effect(self):
        if AmIHost():
            for item in GetPlayerCharacter(self.pc).GetInventoryComponent().InventoryList.Items:
                if str(item.StoredActor) == str(GetPlayerCharacter(self.pc).ActiveWeapons.WeaponSlots[0].AttachedWeapon):
                    GetPlayerCharacter(self.pc).GetInventoryComponent().ServerDropItem(item.Handle, self.pc.Pawn.K2_GetActorLocation(), self.pc.K2_GetActorRotation())
        else:
            SendToHost(self)
        return super().run_effect()
    
class DropEquippedShield(Effect):
    effect_name = "drop_equipped_shield"
    display_name = "Drop Equipped Shield"

    def run_effect(self):
        if AmIHost():
            for item in GetPlayerCharacter(self.pc).GetInventoryComponent().InventoryList.Items:
                if str(item.StoredActor) == str(GetPlayerCharacter(self.pc).EquippedInventory.InventorySlots[1].EquippedInventory):
                    GetPlayerCharacter(self.pc).GetInventoryComponent().ServerDropItem(item.Handle, self.pc.Pawn.K2_GetActorLocation(), self.pc.K2_GetActorRotation())
        else:
            SendToHost(self)
        return super().run_effect()
    
class NoAmmo(Effect):
    effect_name = "no_ammo"
    display_name = "No Ammo"

    def run_effect(self):
        if AmIHost():
            for item in GetPlayerCharacter(self.pc).GetInventoryComponent().InventoryList.Items:
                if str(item.StoredActor) == str(GetPlayerCharacter(self.pc).ActiveWeapons.WeaponSlots[0].AttachedWeapon):
                    item.StoredActor.UseModeState[0].AmmoComponent.ResourcePool.PoolManager.ResourcePools[item.StoredActor.UseModeState[0].AmmoComponent.ResourcePool.PoolIndexInManager].CurrentValue = 0
                    item.StoredActor.UseModeState[0].AmmoComponent.LoadedAmmo = 0
        else:
            SendToHost(self)
        return super().run_effect()
    
class ResetSkillTrees(Effect):
    effect_name = "reset_skill_trees"
    display_name = "Reset Skill Trees"

    def run_effect(self):
        if AmIHost():
            GetPlayerCharacter(self.pc).OakPlayerAbilityManager.PurchaseAbilityRespec()
        else:
            SendToHost(self)
        return super().run_effect()
    
class ViewerBadass(Effect):
    effect_name = "viewer_badass"
    display_name = "Summoning Viewer Badass"

    viewer_pawn = None

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

    def cooldown(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
        global viewer_badass_cooldown_enabled, viewer_badass_cooldown_start_time
        if viewer_badass_cooldown_enabled == True:
            if (viewer_badass_cooldown_start_time + (get_pc().CurrentOakProfile.MinTimeBetweenBadassEvents * 60)) <= time.time():
                print("viewer badass cooldown over, reenabling")
                SetEffectStatus("viewer_badass", 0x82, self.pc)
                viewer_badass_cooldown_enabled = False
                remove_hook("/Script/Engine.HUD:ReceiveDrawHUD", Type.PRE, "viewer_badass_cooldown")
        return None

    def trackdeaths(self, obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
        if str(obj) == str(self.viewer_pawn):
            global viewer_badass_cooldown_enabled, viewer_badass_cooldown_start_time
            viewer_badass_cooldown_start_time = time.time()
            viewer_badass_cooldown_enabled = True
            print("starting viewer badass cooldown")
            self.display_name = f"{self.viewer} Died"
            self.pc.DisplayRolloutNotification("CrowdControl", f"{self.display_name}. {get_pc().CurrentOakProfile.MinTimeBetweenBadassEvents} Minute Cooldown Started.", 3.5 * ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation)
            add_hook("/Script/Engine.HUD:ReceiveDrawHUD", Type.PRE, "viewer_badass_cooldown", self.cooldown)
            remove_hook("/Script/Engine.Pawn:ReceiveUnpossessed", Type.PRE, "viewer_badass_death_check")
        return None

    def run_effect(self):
        global viewer_badass_cooldown_enabled
        if viewer_badass_cooldown_enabled:
            NotifyEffect(self.id, "Failure", self.effect_name, self.pc)
            return
        
        if AmIHost():
            self.display_name = f"Summoning {self.viewer}"
            actor = SpawnEnemyEx(self.possible_enemies[random.randint(0, len(self.possible_enemies) - 1)], 1, self.pc)
            if actor != None:
                print(actor)
                sed = unrealsdk.find_class("StreamingEventDispatcher").ClassDefaultObject
                actor.AIBalanceState.SetGameStage(GetPlayerCharacter(self.pc).PlayerBalanceComponent.ExperienceLevel)
                actor.AIBalanceState.SetExperienceLevel(GetPlayerCharacter(self.pc).PlayerBalanceComponent.ExperienceLevel)
                sed.SetEventEnemy(actor)
                sed.SetEventEnemyName(self.viewer)
                actor.AIBalanceState.DropOnDeathItemPools.ItemPoolLists.append(unrealsdk.find_object("ItemPoolListData", "/Game/GameData/Loot/ItemPools/ItemPoolList_MiniBoss.ItemPoolList_MiniBoss"))
                actor.AIBalanceState.DropOnDeathItemPools.ItemPoolLists.append(unrealsdk.find_object("ItemPoolListData", "/Game/GameData/Loot/ItemPools/ItemPoolList_MiniBoss.ItemPoolList_MiniBoss"))
                self.viewer_pawn = actor
                SetEffectStatus(self.effect_name, 0x83, self.pc) # disable viewer badass button in the twitch integration for viewers until cooldown is done https://developer.crowdcontrol.live/sdk/simpletcp/structure.html#effect-class-messages
                add_hook("/Script/Engine.Pawn:ReceiveUnpossessed", Type.PRE, "viewer_badass_death_check", self.trackdeaths)
                return super().run_effect()
            else:
                return super().run_effect("Failure")
        else:
            SendToHost(self)
            return super().run_effect()
        
class FastGameSpeed(Effect):
    effect_name = "fast_game_speed"
    display_name = "4x Speed"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation = 4.0
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation = 1.0
        return super().stop_effect(response, respond)
    
class SlowGameSpeed(Effect):
    effect_name = "slow_game_speed"
    display_name = "0.5x Speed"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation = 0.5
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            ENGINE.GameViewport.World.CurrentLevel.WorldSettings.TimeDilation = 1.0
        return super().stop_effect(response, respond)
    
class FlyMode(Effect):
    effect_name = "fly_mode"
    display_name = "I can fly!"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            GetPlayerCharacter(self.pc).OakCharacterMovement.MovementMode = 5
            GetPlayerCharacter(self.pc).OakDamageComponent.MinimumDamageLaunchVelocity = 9999999999
            GetPlayerCharacter(self.pc).OakCharacterMovement.MaxFlySpeed.Value = 5000
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        if AmIHost():
            GetPlayerCharacter(self.pc).OakCharacterMovement.MovementMode = 1
            GetPlayerCharacter(self.pc).OakDamageComponent.MinimumDamageLaunchVelocity = 370
            GetPlayerCharacter(self.pc).OakCharacterMovement.MaxFlySpeed.Value = 600
        return super().stop_effect(response, respond)