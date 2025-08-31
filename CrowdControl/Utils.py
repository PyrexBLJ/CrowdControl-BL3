
from mods_base import get_pc, ENGINE, hook #type: ignore
from unrealsdk import find_object, make_struct, find_class, find_all, load_package #type: ignore
from unrealsdk.unreal import UObject, BoundFunction, UObject, WrappedStruct,WeakPointer, IGNORE_STRUCT #type: ignore
from unrealsdk.hooks import Type #type: ignore
import unrealsdk #type: ignore
from typing import Any
from .Effect import *
import math
import json
import base64
from .EnemySpawnerLists import Package,PackageName,EnemyName
from .InteractiveObjectLists import PackageInteractive,PackageNameInteractive

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
    


def SendToHost(effect:Effect) -> None:
    efdict = effect.__dict__
    efdict["pc"] = str(efdict["pc"])
    effectdict: str = json.dumps(efdict)
    b64effectdict = base64.b64encode(bytes(effectdict, 'utf-8'))
    efdict["pc"] = unrealsdk.find_object("Actor", efdict["pc"].split("'")[1])
    effect.pc.ServerChangeName(f"CrowdControl-{effect.effect_name}-{b64effectdict.decode()}")
    return None
    

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
            break
    
    PawnList = [Pawn for Pawn in PawnList if Pawn not in PawnsToRemove and Pawn()]
    return



library = find_object("Object", "/Script/GbxSpawn.Default__SpawnerBlueprintLibrary")


def get_spawn_point() -> UObject | None:
    for spawn_point in find_all("OakSpawnPointComponent"):
        if spawn_point.bEnabled and spawn_point.SpawnPoint and "Default" not in str(spawn_point):
            return spawn_point
    return None

    
def get_spawner() -> UObject | None:
    for spawner in find_all("OakSpawnerComponent"):
        if spawner.bEnabled and "GEN_VARIABLE" not in str(spawner) and "Default" not in str(spawner):
                return spawner
    return None


EnemiesDict = {
    "loottink": "Loot Tink"
}

def SpawnEnemy(EnemyToSpawn:str, AmountToSpawn:int, PC:UObject, DisplayName = "") -> bool:
    EnemyToSpawn = EnemiesDict[EnemyToSpawn]
    Index = EnemyName.index(EnemyToSpawn)
    #for i in range(len(PackageName)):
    #    if str(EnemyToSpawn).lower() in str().lower():
    #        Index = i
    #        break

    if Index == -1:
        return False

    factory = find_class("SpawnFactory_OakAI").ClassDefaultObject
    load_package(str(Package[Index]))
    factory.AIActorClass = find_object("BlueprintGeneratedClass", str(PackageName[Index]))

    spawnpoint = get_spawn_point()
    originalstyle = spawnpoint.SpawnPoint.GetSpawnStyleTag()
    no_spawn = make_struct("GameplayTag",TagName="None")
    spawnpoint.SpawnPoint.SetSpawnStyleTag(no_spawn)
    originallocation = spawnpoint.K2_GetComponentLocation()
    spawnpoint.K2_SetWorldLocation(make_struct("Vector", X=100000,Y=100000,Z=500000), True, IGNORE_STRUCT, True)

    PCLoc = PC.pawn.K2_GetActorLocation()
    PCRot = PC.pawn.K2_GetActorRotation()

    location = make_struct("Vector", X=PCLoc.X + 500 * math.cos(math.radians((PCRot.Yaw))), Y=PCLoc.Y + 500 * math.sin(math.radians((PCRot.Yaw))), Z=PCLoc.Z)
    Rotator = make_struct("Rotator", Roll =0, Pitch=0, Yaw=PCRot.Yaw-180)     

    for i in range(AmountToSpawn):
        actor = library.SpawnActorWithSpawner(PC, factory, spawnpoint, get_spawner(), None)
        actor.K2_TeleportTo(location, Rotator)
        if DisplayName:
            name = find_class("GbxUIName").ClassDefaultObject
            name.DisplayName = DisplayName
            actor.TargetableComponent.SetTargetUIName(name)

    spawnpoint.K2_SetWorldLocation(originallocation, True, IGNORE_STRUCT, True)
    spawnpoint.SpawnPoint.SetSpawnStyleTag(originalstyle)
    return True

def SpawnEnemyEx(EnemyToSpawn:str, AmountToSpawn:int, PC:UObject) -> UObject:
    Index = EnemyName.index(EnemyToSpawn)
    #for i in range(len(PackageName)):
    #    if str(EnemyToSpawn).lower() in str().lower():
    #        Index = i
    #        break

    if Index == -1:
        return None

    factory = find_class("SpawnFactory_OakAI").ClassDefaultObject
    load_package(str(Package[Index]))
    factory.AIActorClass = find_object("BlueprintGeneratedClass", str(PackageName[Index]))

    spawnpoint = get_spawn_point()
    originalstyle = spawnpoint.SpawnPoint.GetSpawnStyleTag()
    no_spawn = make_struct("GameplayTag",TagName="None")
    spawnpoint.SpawnPoint.SetSpawnStyleTag(no_spawn)
    originallocation = spawnpoint.K2_GetComponentLocation()
    spawnpoint.K2_SetWorldLocation(make_struct("Vector", X=100000,Y=100000,Z=500000), True, IGNORE_STRUCT, True)

    PCLoc = PC.pawn.K2_GetActorLocation()
    PCRot = PC.pawn.K2_GetActorRotation()

    location = make_struct("Vector", X=PCLoc.X + 500 * math.cos(math.radians((PCRot.Yaw))), Y=PCLoc.Y + 500 * math.sin(math.radians((PCRot.Yaw))), Z=PCLoc.Z)
    Rotator = make_struct("Rotator", Roll =0, Pitch=0, Yaw=PCRot.Yaw-180)     

    for i in range(AmountToSpawn):
        actor = library.SpawnActorWithSpawner(PC, factory, spawnpoint, get_spawner(), None)
        actor.K2_TeleportTo(location, Rotator)

    spawnpoint.K2_SetWorldLocation(originallocation, True, IGNORE_STRUCT, True)
    spawnpoint.SpawnPoint.SetSpawnStyleTag(originalstyle)
    return actor

def SpawnInteractiveObject(Index: int, Location: None, Rotation: None) -> None:
    factory = find_class("SpawnFactory_OakInteractiveObject").ClassDefaultObject
    load_package(str(PackageInteractive[Index]))
    factory.InteractiveObjectClass = find_object("BlueprintGeneratedClass", str(PackageNameInteractive[Index]))
    spawnpoint = get_spawn_point()
    originallocation = spawnpoint.K2_GetComponentLocation()
    originalspawnaction = str(spawnpoint.SpawnAction.TagName)
    spawnpoint.SpawnAction.TagName = "None"
    spawnpoint.K2_SetWorldLocation(Location, True,IGNORE_STRUCT, True)
    spawnpoint.K2_SetWorldRotation(Rotation, True,IGNORE_STRUCT, True)
    actor = library.SpawnActorWithSpawner(get_pc(), factory, spawnpoint, get_spawner(), None)
    spawnpoint.K2_SetWorldLocation(originallocation, True,IGNORE_STRUCT, True)
    spawnpoint.SpawnAction.TagName = originalspawnaction
