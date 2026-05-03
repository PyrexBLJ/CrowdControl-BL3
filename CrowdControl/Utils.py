
from mods_base import get_pc, ENGINE, hook #type: ignore
from unrealsdk import find_object, make_struct, find_class, find_all, load_package, construct_object #type: ignore
from unrealsdk.unreal import UObject, BoundFunction, UObject, WrappedStruct,WeakPointer, IGNORE_STRUCT, UStruct #type: ignore
from unrealsdk.hooks import Type #type: ignore
import unrealsdk #type: ignore
from typing import Any, List
from .Effect import *
import math
import json
import base64
import random
from .EnemySpawnerLists import Enemies, Chubbies, lootbois
from .InteractiveObjectLists import InteractiveObjects

blacklist_teams = [
    "NonPlayers",
    "Players",
    "Team_Ghost",
    "Friendly to All",
    "Team_Neutral",
]

def GetPlayerForwardVector(player: UObject) -> UStruct:
    x = math.cos(get_pc().Pawn.Controller.CalcViewRotation.Yaw / 32767 * math.pi) * math.cos(get_pc().Pawn.Controller.CalcViewRotation.Pitch / 32767 * math.pi)
    y = math.sin(get_pc().Pawn.Controller.CalcViewRotation.Yaw / 32767 * math.pi) * math.cos(get_pc().Pawn.Controller.CalcViewRotation.Pitch / 32767 * math.pi)
    z = math.sin(get_pc().Pawn.Controller.CalcViewRotation.Pitch / 32767 * math.pi)
    return unrealsdk.make_struct("Vector", X=x, Y=y, Z=z)

def InFrontOfPlayer(player: UObject, distance: int = 200) -> UStruct:
    x = player.Pawn.Location.X + (GetPlayerForwardVector(player).X * distance)
    y = player.Pawn.Location.Y + (GetPlayerForwardVector(player).Y * distance)
    loc = make_struct("Vector", X=x, Y=y, Z=player.Pawn.Location.Z)
    return loc

def AmIHost() -> bool:
    return get_pc().PlayerReplicationInfo.bIsPartyLeader
    
def GetPlayerCharacter(player: UObject) -> UObject:
    if player.MyWillowPawn != None:
        return player.Pawn
    elif player.Pawn != None:
        return player.Pawn
    else:
        return player.MyWillowPawn
    
def get_player_location() -> UStruct:
    return get_pc().Pawn.Location
    
def SendToHost(effect:Effect) -> None:
    efdict = effect.__dict__
    efdict["pc"] = str(efdict["pc"])
    effectdict: str = json.dumps(efdict)
    b64effectdict = base64.b64encode(bytes(effectdict, 'utf-8'))
    efdict["pc"] = unrealsdk.find_object("Actor", efdict["pc"].split("'")[1])
    effect.pc.ServerSpeech("CrowdControl", efdict["pc"].PlayerReplicationInfo.PlayerId, f"CrowdControl-{effect.effect_name}-{b64effectdict.decode()}")
    return None
    

LootPools = {
    "legendaryweapon": "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary", #quantiy:1
    "purpleweapon": "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_05_VeryRare",
    "blueweapon": "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_04_Rare",
    "greenweapon": "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_02_Uncommon",
    "whiteweapon": "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_01_Common",
}

def SpawnLoot(ItemPoolName:str, Quantity:int, Pawn:UObject):

    ItemPoolData = find_object("ItemPoolDefinition", LootPools[ItemPoolName])

    bsl_obj = unrealsdk.construct_object("Behavior_SpawnLootAroundPoint", ENGINE.Outer)
    items: list = []
    for i in range(Quantity):
        items.append(ItemPoolData)
    bsl_obj.ItemPools = items
    bsl_obj.SpawnVelocityRelativeTo = 0
    bsl_obj.bTorque = False
    bsl_obj.CircularScatterRadius = 50.0
    bsl_obj.CustomLocation = unrealsdk.make_struct("AttachmentLocationData", Location=unrealsdk.make_struct("Vector", X=InFrontOfPlayer(Pawn.Controller).X, Y=InFrontOfPlayer(Pawn.Controller).Y, Z=InFrontOfPlayer(Pawn.Controller).Z + 50), AttachmentBase=None, AttachmentName="")
    bsl_obj.ApplyBehaviorToContext(Pawn.Controller, IGNORE_STRUCT, None, None, None, IGNORE_STRUCT)


PawnList = []

def GetPawnList(bIncludePlayers = True):
    if bIncludePlayers:
        return [Pawn() for Pawn in PawnList if Pawn()]
    else:
        return [Pawn() for Pawn in PawnList if Pawn() and not Pawn().IsHumanControlled()]
 
    
@hook("WillowGame.WillowPawn:PossessedBy", Type.POST)
def CrowdControl_PawnList_Possessed(obj: UObject,args: WrappedStruct,ret: Any,func: BoundFunction,) -> Any:
    PawnList.append(WeakPointer(obj))
    return


@hook("WillowGame.WillowPawn:UnPossessed", Type.PRE)
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

def SpawnPawn(enemytospawn: str, quantity: int, PC: UObject, name: str = "", friendly: bool = False, level_boost: int = 0) -> List[UObject]:
    popmaster = unrealsdk.find_all("WillowPopulationMaster")[-1]
    print(popmaster)
    maptoload = Enemies[enemytospawn][1]

    already_loaded = True
    try:
        unrealsdk.find_object("AIPawnBalanceDefinition", Enemies[enemytospawn][0])
    except:
        already_loaded = False

    if already_loaded == False:
        fullmaplist = None
        for maplist in unrealsdk.find_all("LevelDependencyList"):
            if "transient" in str(maplist).lower():
                fullmaplist = maplist
                break
        loaded = False
        for fullmap in fullmaplist.LevelList:
            if fullmap.PersistentMap == maptoload or maptoload in fullmap.SecondaryMaps:
                unrealsdk.load_package(fullmap.PersistentMap)
                loaded = True
                for map in fullmap.SecondaryMaps:
                    unrealsdk.load_package(map)
                    loaded = True
                break
        if loaded == False:
            unrealsdk.load_package(maptoload)

    factory = unrealsdk.construct_object("PopulationFactoryBalancedAIPawn", ENGINE.Outer)
    if name == "":
        factory.PawnBalanceDefinition = unrealsdk.find_object("AIPawnBalanceDefinition", Enemies[enemytospawn][0])
    else:
        AIPBD = unrealsdk.construct_object("AIPawnBalanceDefinition", ENGINE.Outer, f"CrowdControlAIPBD-{enemytospawn}", 0, unrealsdk.find_object("AIPawnBalanceDefinition", Enemies[enemytospawn][0]))
        for playthru in AIPBD.PlayThroughs:
            playthru.DisplayName = name
        factory.PawnBalanceDefinition = AIPBD

    actors: List[UObject] = []
    for i in range(quantity):
        maxcost = popmaster.MaxActorCost
        popmaster.MaxActorCost = 999999999
        actor = popmaster.SpawnActor(factory, None, InFrontOfPlayer(PC, 500), PC.Pawn.Controller.Rotation, PC.PlayerReplicationInfo.ExpLevel + PC.OverpowerChoiceValue + level_boost, 0)
        popmaster.MaxActorCost = maxcost
        
        if str(actor) != "None":
            if friendly:
                actor.Allegiance = unrealsdk.find_object("PawnAllegiance", "GD_AI_Allegiance.Allegiance_Player")
            else:
                actor.Allegiance = unrealsdk.find_object("PawnAllegiance", "GD_AI_Allegiance.Allegiance_Bot")
        actors.append(actor)

    return actors

def SpawnChubby(quantity: int, PC: UObject) -> List[UObject]:
    popmaster = unrealsdk.find_all("WillowPopulationMaster")[-1]
    actors: List[UObject] = []

    for i in range(quantity):
        chubbytospawn = "bones"
        cm = ENGINE.GetDLCManager()
        if not cm.IsPackageFullyInstalled(cm.GetDownloadablePackageDefinitionFromDLCName("Aster")):
            while chubbytospawn == "bones":
                chubbytospawn = random.choice(list(Chubbies.keys()))
        else:
            chubbytospawn = random.choice(list(Chubbies.keys()))

        maptoload = Chubbies[chubbytospawn][1]

        already_loaded = True
        try:
            unrealsdk.find_object("AIPawnBalanceDefinition", Chubbies[chubbytospawn][0])
        except:
            already_loaded = False

        if already_loaded == False:
            fullmaplist = None
            for maplist in unrealsdk.find_all("LevelDependencyList"):
                if "transient" in str(maplist).lower():
                    fullmaplist = maplist
                    break
            loaded = False
            for fullmap in fullmaplist.LevelList:
                if fullmap.PersistentMap == maptoload or maptoload in fullmap.SecondaryMaps:
                    unrealsdk.load_package(fullmap.PersistentMap)
                    loaded = True
                    for map in fullmap.SecondaryMaps:
                        unrealsdk.load_package(map)
                        loaded = True
                    break
            if loaded == False:
                unrealsdk.load_package(maptoload)

        factory = unrealsdk.construct_object("PopulationFactoryBalancedAIPawn", ENGINE.Outer)
        factory.PawnBalanceDefinition = unrealsdk.find_object("AIPawnBalanceDefinition", Chubbies[chubbytospawn][0])
        
        maxcost = popmaster.MaxActorCost
        popmaster.MaxActorCost = 999999999
        actor = popmaster.SpawnActor(factory, None, InFrontOfPlayer(PC, 500), PC.Pawn.Controller.Rotation, PC.PlayerReplicationInfo.ExpLevel + PC.OverpowerChoiceValue, 0)
        popmaster.MaxActorCost = maxcost

        actor.Allegiance = unrealsdk.find_object("PawnAllegiance", "GD_AI_Allegiance.Allegiance_Bot")
        actors.append(actor)

    return actors

def Spawnlootboi(quantity: int, PC: UObject) -> List[UObject]:
    popmaster = unrealsdk.find_all("WillowPopulationMaster")[-1]
    actors: List[UObject] = []

    for i in range(quantity):
        lootboitospawn = random.choice(list(lootbois.keys()))
        maptoload = lootbois[lootboitospawn][1]

        already_loaded = True
        try:
            unrealsdk.find_object("AIPawnBalanceDefinition", lootbois[lootboitospawn][0])
        except:
            already_loaded = False

        if already_loaded == False:
            fullmaplist = None
            for maplist in unrealsdk.find_all("LevelDependencyList"):
                if "transient" in str(maplist).lower():
                    fullmaplist = maplist
                    break
            loaded = False
            for fullmap in fullmaplist.LevelList:
                if fullmap.PersistentMap == maptoload or maptoload in fullmap.SecondaryMaps:
                    unrealsdk.load_package(fullmap.PersistentMap)
                    loaded = True
                    for map in fullmap.SecondaryMaps:
                        unrealsdk.load_package(map)
                        loaded = True
                    break
            if loaded == False:
                unrealsdk.load_package(maptoload)

        factory = unrealsdk.construct_object("PopulationFactoryBalancedAIPawn", ENGINE.Outer)
        factory.PawnBalanceDefinition = unrealsdk.find_object("AIPawnBalanceDefinition", lootbois[lootboitospawn][0])

        maxcost = popmaster.MaxActorCost
        popmaster.MaxActorCost = 999999999
        actor = popmaster.SpawnActor(factory, None, InFrontOfPlayer(PC, 500), PC.Pawn.Controller.Rotation, PC.PlayerReplicationInfo.ExpLevel + PC.OverpowerChoiceValue, 0)
        popmaster.MaxActorCost = maxcost

        actor.Allegiance = unrealsdk.find_object("PawnAllegiance", "GD_AI_Allegiance.Allegiance_Bot")
        actors.append(actor)

    return actors

def SpawnIO(iotospawn: str, quantity: int, PC: UObject, location: UStruct, rotation: UStruct) -> List[UObject]:
    popmaster = unrealsdk.find_all("WillowPopulationMaster")[-1]
    maptoload = InteractiveObjects[iotospawn][2]

    already_loaded = True
    try:
        unrealsdk.find_object("InteractiveObjectDefinition", InteractiveObjects[iotospawn][0])
    except:
        already_loaded = False

    if already_loaded == False:
        fullmaplist = None
        for maplist in unrealsdk.find_all("LevelDependencyList"):
            if "transient" in str(maplist).lower():
                fullmaplist = maplist
                break
        loaded = False
        for fullmap in fullmaplist.LevelList:
            if fullmap.PersistentMap == maptoload or maptoload in fullmap.SecondaryMaps:
                unrealsdk.load_package(fullmap.PersistentMap)
                loaded = True
                for map in fullmap.SecondaryMaps:
                    unrealsdk.load_package(map)
                    loaded = True
                break
        if loaded == False:
            unrealsdk.load_package(maptoload)

    factory = unrealsdk.construct_object("PopulationFactoryInteractiveObject", ENGINE.Outer)
    factory.ObjectDefinition = unrealsdk.find_object("InteractiveObjectDefinition", InteractiveObjects[iotospawn][0])
    factory.ObjectBalanceDefinition = unrealsdk.find_object("InteractiveObjectBalanceDefinition", InteractiveObjects[iotospawn][1])

    actors: List[UObject] = []
    for i in range(quantity):
        maxcost = popmaster.MaxActorCost
        popmaster.MaxActorCost = 999999999
        actor = popmaster.SpawnActor(factory, None, location, rotation, PC.PlayerReplicationInfo.ExpLevel + PC.OverpowerChoiceValue, 0)
        popmaster.MaxActorCost = maxcost
        #actor.SetRotation(rotation)
        actors.append(actor)

        if "VendingMachine" in str(factory.ObjectDefinition):
            SetupVendingMachine(actor)

    return actors

def SetupVendingMachine(vendor: UObject) -> None:
    if "Weapons" in str(vendor.InteractiveObjectDefinition):
        vendor.ShopType = 0
    elif "GrenadesAndAmmo" in str(vendor.InteractiveObjectDefinition):
        vendor.ShopType = 1
    elif "HealthItems" in str(vendor.InteractiveObjectDefinition):
        vendor.ShopType = 2
    else:
        vendor.ShopType = 0

    vendor.FixedItemCost = -1
    vendor.FixedFeaturedItemCost = -1
    vendor.FormOfCurrency = 0
    
    vendor.CommerceMarkup.InitializationDefinition = unrealsdk.find_object("AttributeInitializationDefinition", "GD_Economy.VendingMachine.Init_MarkupCalc_P1")
    vendor.InventoryConfigurationName = "Inventory"
    vendor.FeaturedItemCommerceMarkup.InitializationDefinition = unrealsdk.find_object("AttributeInitializationDefinition", "GD_Economy.VendingMachine.Init_MarkupCalc_P1")
    vendor.FeaturedItemConfigurationName = "FeaturedItem"
    vendor.FeaturedItemGameStage.InitializationDefinition = unrealsdk.find_object("AttributeInitializationDefinition", "GD_Population_Shopping.Balance.Init_FeaturedItem_GameStage")
    vendor.FeaturedItemAwesomeLevel.InitializationDefinition = unrealsdk.find_object("AttributeInitializationDefinition", "GD_Population_Shopping.Balance.Init_FeaturedItem_AwesomeLevel")

    vendor.ResetInventory()
    return None