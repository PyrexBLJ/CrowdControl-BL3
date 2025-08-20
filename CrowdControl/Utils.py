import unrealsdk
from mods_base import get_pc, ENGINE, make_struct, find_object, find_class
from unrealsdk.unreal import UObject, WrappedStruct




def InFrontOfPlayer(player: UObject) -> UObject:
    x = player.Pawn.K2_GetActorLocation().X + (player.GetActorForwardVector().X * 200)
    y = player.Pawn.K2_GetActorLocation().Y + (player.GetActorForwardVector().Y * 200)
    loc = unrealsdk.make_struct("Vector", X=x, Y=y, Z=player.Pawn.K2_GetActorLocation().Z)
    return loc

def AmIHost() -> bool:
    if get_pc().PlayerState == ENGINE.GameViewport.World.GameState.HostPlayerState:
        return True
    else:
        return False
    
def GetPlayerCharacter(player: UObject) -> UObject:
    if player.OakCharacter == None:
        return player.PrimaryCharacter
    if "IronBear" in str(player.OakCharacter):
        return player.OakCharacter.Gunner
    else:
        return player.OakCharacter
    

LootPools = {
    "Legendary Weapon": '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Legendary.ItemPool_Guns_Legendary',
}

oak_blueprint_library = find_class("OakBlueprintLibrary").ClassDefaultObject

def SpawnLoot(ItemPoolName:str, Pawn:UObject):
    ItemPoolData = find_object("ItemPoolData", LootPools[ItemPoolName])

    PickupRequest = make_struct("SpawnDroppedPickupLootRequest",
                        ContextActor=Pawn,
                        ItemPools=ItemPoolData,
                        )
    
    oak_blueprint_library.SpawnLootAsync(Pawn, PickupRequest)