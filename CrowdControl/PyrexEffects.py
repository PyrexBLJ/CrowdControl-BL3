from .Effect import Effect
from .Utils import GetPlayerCharacter, AmIHost
from mods_base import get_pc, ENGINE #type: ignore
import unrealsdk #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct #type: ignore
from unrealsdk.hooks import Type, add_hook, remove_hook #type: ignore
from typing import Any


class NoGravity(Effect):
    effect_name = "no_gravity"
    display_name = "No Gravity"

    def run_effect(self):
        if AmIHost():
            GetPlayerCharacter(self.pc).OakCharacterMovement.GravityScale = 0.0
        else:
            self.pc.ServerChangeName(f"CrowdControl-{self.pc.PlayerState.PlayerID}-no_gravity-{self.id}")
        return super().run_effect()

    def stop_effect(self):
        GetPlayerCharacter(self.pc).OakCharacterMovement.GravityScale = 1.0
        return super().stop_effect()
    
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
            self.pc.ServerChangeName(f"CrowdControl-{self.pc.PlayerState.PlayerID}-instant_death-{self.id}")
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
            self.pc.ServerChangeName(f"CrowdControl-{self.pc.PlayerState.PlayerID}-drop_entire_inventory-{self.id}")
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
            self.pc.ServerChangeName(f"CrowdControl-{self.pc.PlayerState.PlayerID}-delete_ground_items-{self.id}")
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
            self.pc.ServerChangeName(f"CrowdControl-{self.pc.PlayerState.PlayerID}-fall_damage-{self.id}")
        return super().run_effect()
    
    def stop_effect(self):
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
            self.pc.ServerChangeName(f"CrowdControl-{self.pc.PlayerState.PlayerID}-drop_held_weapon-{self.id}")
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
            self.pc.ServerChangeName(f"CrowdControl-{self.pc.PlayerState.PlayerID}-drop_equipped_shield-{self.id}")
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
            self.pc.ServerChangeName(f"CrowdControl-{self.pc.PlayerState.PlayerID}-no_ammo-{self.id}")
        return super().run_effect()
    
class ResetSkillTrees(Effect):
    effect_name = "reset_skill_trees"
    display_name = "Reset Skill Trees"

    def run_effect(self):
        if AmIHost():
            GetPlayerCharacter(self.pc).OakPlayerAbilityManager.PurchaseAbilityRespec()
        else:
            self.pc.ServerChangeName(f"CrowdControl-{self.pc.PlayerState.PlayerID}-reset_skill_trees-{self.id}")
        return super().run_effect()