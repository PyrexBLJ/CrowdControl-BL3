
from mods_base import get_pc, ENGINE, hook
from unrealsdk import find_object, make_struct, find_class
from unrealsdk.unreal import UObject, BoundFunction, UObject, WrappedStruct,WeakPointer
from unrealsdk.hooks import Type
from typing import Any
blacklist_teams = [
    "NonPlayers",
    "Players",
    "Team_Ghost",
    "Friendly to All",
    "Team_Neutral",
]



def InFrontOfPlayer(player: UObject) -> UObject:
    x = player.Pawn.K2_GetActorLocation().X + (player.GetActorForwardVector().X * 200)
    y = player.Pawn.K2_GetActorLocation().Y + (player.GetActorForwardVector().Y * 200)
    loc = make_struct("Vector", X=x, Y=y, Z=player.Pawn.K2_GetActorLocation().Z)
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
    "legendaryweapon": "/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Legendary.ItemPool_Guns_Legendary", #quantiy:1
}
oak_blueprint_library = find_class("OakBlueprintLibrary").ClassDefaultObject

def SpawnLoot(ItemPoolName:str, Quantity:int, Pawn:UObject):

    ItemPoolData = find_object("ItemPoolData", LootPools[ItemPoolName])

    PickupRequest = make_struct("SpawnDroppedPickupLootRequest",
                        ContextActor=Pawn,
                        ItemPools=ItemPoolData,
                        )
    
    for i in range(Quantity): 
        oak_blueprint_library.SpawnLootAsync(Pawn, PickupRequest)


PawnList = []

def GetPawnList(bIncludePlayers = True):
    if bIncludePlayers:
        return [Pawn() for Pawn in PawnList if Pawn()]
    else:
        return [Pawn() for Pawn in PawnList if Pawn() and not Pawn().IsPlayerControlled()]
 
    
@hook("/Script/Engine.Pawn:ReceivePossessed", Type.POST)
def CrowdControl_PawnList_Possessed(obj: UObject,args: WrappedStruct,ret: Any,func: BoundFunction,) -> Any:
    PawnList.append(WeakPointer(obj))
    return


@hook("/Script/Engine.Pawn:ReceiveUnpossessed", Type.PRE)
def CrowdControl_PawnList_Unpossessed(obj: UObject,args: WrappedStruct,ret: Any,func: BoundFunction,) -> Any:
    global PawnList
    PawnsToRemove = []
    for Pawn in PawnList:
        if not Pawn():
            PawnsToRemove.append(Pawn)
            continue

        if Pawn() == obj:
            PawnsToRemove.append(Pawn)
    
    PawnList = [Pawn for Pawn in PawnList if Pawn not in PawnsToRemove and Pawn()]
    return