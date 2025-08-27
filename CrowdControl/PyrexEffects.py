from .Effect import Effect
from .Utils import GetPlayerCharacter, AmIHost
from mods_base import get_pc #type: ignore


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