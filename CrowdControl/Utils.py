
from mods_base import get_pc, ENGINE, hook #type: ignore
from unrealsdk import find_object, make_struct, find_class, find_all, load_package, construct_object #type: ignore
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
    OakSpawnPoint = construct_object("OakSpawnPoint", outer=ENGINE.GameViewport.World.CurrentLevel.OwningWorld.PersistentLevel)
    OakSpawnPoint.RootComponent.AttachChildren.append(OakSpawnPoint.SpawnPointComponent)
    return OakSpawnPoint.SpawnPointComponent

    
def get_spawner() -> UObject | None:
    for spawner in find_all("OakSpawnerComponent"):
        if spawner.bEnabled and "GEN_VARIABLE" not in str(spawner) and "Default" not in str(spawner):
                return spawner
    return None


EnemiesDict = {
    "loottink": "Loot Tink",
    "ratchswarm": "Ratch Swarm",
}
import random 
def SpawnEnemy(EnemyToSpawn:str, AmountToSpawn:int, PC:UObject, DisplayName = "", is_friendly:bool = False) -> bool:
    EnemyToSpawn = EnemiesDict[EnemyToSpawn]
    Index = EnemyName.index(EnemyToSpawn)
    #for i in range(len(PackageName)):
    #    if str(EnemyToSpawn).lower() in str().lower():
    #        Index = i
    #        break

    if Index == -1:
        return False

    factory = find_class("SpawnFactory_OakAI").ClassDefaultObject

    if is_friendly:
        factory.TeamOverride = unrealsdk.find_object("Team", "/Game/Common/_Design/Teams/Team_Players.Team_Players")
    else:
        factory.TeamOverride = unrealsdk.find_object("Team", "/Game/Common/_Design/Teams/Team_Enemies.Team_Enemies")

    load_package(str(Package[Index]))
    factory.AIActorClass = find_object("BlueprintGeneratedClass", str(PackageName[Index]))

    spawnpoint = get_spawn_point()

    PCLoc = PC.pawn.K2_GetActorLocation()
    PCRot = PC.pawn.K2_GetActorRotation()

    Rotator = make_struct("Rotator", Roll =0, Pitch=0, Yaw=PCRot.Yaw-180)     


    spread_radius = 800

    for i in range(AmountToSpawn):
        if i == 0:
            location = make_struct(
                "Vector",
                X=PCLoc.X + 500 * math.cos(math.radians(PCRot.Yaw)),
                Y=PCLoc.Y + 500 * math.sin(math.radians(PCRot.Yaw)),
                Z=PCLoc.Z
            )
        else:
            offset_x = random.uniform(-spread_radius, spread_radius)
            offset_y = random.uniform(-spread_radius, spread_radius)

            location = make_struct(
                "Vector",
                X=PCLoc.X + offset_x,
                Y=PCLoc.Y + offset_y,
                Z=PCLoc.Z
            )

        spawnpoint.K2_SetWorldLocation(location, True, IGNORE_STRUCT, True)
        spawnpoint.K2_SetWorldRotation(Rotator, True, IGNORE_STRUCT, True)
        actor = library.SpawnActorWithSpawner(PC, factory, spawnpoint, get_spawner(), None)
        if DisplayName:
            name = find_class("GbxUIName").ClassDefaultObject
            name.DisplayName = DisplayName
            actor.TargetableComponent.SetTargetUIName(name)

    factory.TeamOverride = None

    return True

def SpawnEnemyEx(EnemyToSpawn:str, AmountToSpawn:int, PC:UObject, is_friendly:bool = False) -> UObject:
    Index = EnemyName.index(EnemyToSpawn)

    if Index == -1:
        return None

    factory = find_class("SpawnFactory_OakAI").ClassDefaultObject

    if is_friendly:
        factory.TeamOverride = unrealsdk.find_object("Team", "/Game/Common/_Design/Teams/Team_Players.Team_Players")
    else:
        factory.TeamOverride = unrealsdk.find_object("Team", "/Game/Common/_Design/Teams/Team_Enemies.Team_Enemies")

    load_package(str(Package[Index]))
    factory.AIActorClass = find_object("BlueprintGeneratedClass", str(PackageName[Index]))

    spawnpoint = get_spawn_point()

    PCLoc = PC.pawn.K2_GetActorLocation()
    PCRot = PC.pawn.K2_GetActorRotation()

    Rotator = make_struct("Rotator", Roll =0, Pitch=0, Yaw=PCRot.Yaw-180)     

    for i in range(AmountToSpawn):
        location = make_struct("Vector", X=PCLoc.X + 500 * math.cos(math.radians((PCRot.Yaw))), Y=PCLoc.Y + 500 * math.sin(math.radians((PCRot.Yaw))), Z=PCLoc.Z + (i * 200))
        spawnpoint.K2_SetWorldLocation(location, True, IGNORE_STRUCT, True)
        spawnpoint.K2_SetWorldRotation(Rotator, True, IGNORE_STRUCT, True)
        actor = library.SpawnActorWithSpawner(PC, factory, spawnpoint, get_spawner(), None)
    
    factory.TeamOverride = None

    return actor

def SpawnInteractiveObject(Index: int, Location: None, Rotation: None) -> None:
    factory = find_class("SpawnFactory_OakInteractiveObject").ClassDefaultObject
    load_package(str(PackageInteractive[Index]))
    factory.InteractiveObjectClass = find_object("BlueprintGeneratedClass", str(PackageNameInteractive[Index]))
    spawnpoint = get_spawn_point()
    spawnpoint.K2_SetWorldLocation(Location, True, IGNORE_STRUCT, True)
    spawnpoint.K2_SetWorldRotation(Rotation, True, IGNORE_STRUCT, True)
    actor = library.SpawnActorWithSpawner(get_pc(), factory, spawnpoint, get_spawner(), None)
    return actor

def Net(Location: None, OffSet: 600 , ZOffSet: 300) -> None:
    Netlist: list = [make_struct("Vector", X=Location.X + OffSet, Y=Location.Y + 0, Z=Location.Z+ZOffSet),make_struct("Vector", X=Location.X + -OffSet, Y=Location.Y + 0, Z=Location.Z+ZOffSet),make_struct("Vector", X=Location.X + 0, Y=Location.Y + OffSet, Z=Location.Z+ZOffSet),make_struct("Vector", X=Location.X + 0, Y=Location.Y + -OffSet, Z=Location.Z+ZOffSet),make_struct("Vector", X=Location.X + 0, Y=Location.Y + 0, Z=Location.Z+ZOffSet), make_struct("Vector", X=Location.X + -OffSet, Y=Location.Y + OffSet, Z=Location.Z+ZOffSet), make_struct("Vector", X=Location.X + -OffSet, Y=Location.Y + -OffSet, Z=Location.Z+ZOffSet), make_struct("Vector", X=Location.X + OffSet, Y=Location.Y + -OffSet, Z=Location.Z+ZOffSet), make_struct("Vector", X=Location.X + OffSet, Y=Location.Y + OffSet, Z=Location.Z+ZOffSet)]
    return Netlist

def Circle(Location: None, Layers: 1, LayerIncrease: 2, Baseamount: 6, OffSet: 600, ZOffSet: 300, Center:bool = False) -> None:
    circlenet: list = []
    if Center:
        circlenet.append(make_struct("Vector", X=Location.X, Y=Location.Y, Z=Location.Z + ZOffSet))
    for i in range(Layers):
        for u in range((LayerIncrease * i) + Baseamount):
            circlenet.append(make_struct("Vector", X=Location.X + OffSet * math.cos(2*math.pi*((u+1)/((LayerIncrease * i) + Baseamount))) * (i + 1), Y=Location.Y + OffSet * math.sin(2*math.pi*((u+1)/((LayerIncrease * i) + Baseamount))) * (i + 1), Z=Location.Z + ZOffSet))
    return circlenet
