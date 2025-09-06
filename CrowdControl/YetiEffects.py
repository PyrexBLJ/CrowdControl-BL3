from .Effect import Effect
from typing import Any
from mods_base import ENGINE,get_pc
from unrealsdk import find_object, make_struct, find_all, find_class, load_package
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct,IGNORE_STRUCT
from unrealsdk.hooks import Type, add_hook, remove_hook, prevent_hooking_direct_calls
from .Utils import blacklist_teams,oak_blueprint_library,GetPawnList,AmIHost,SendToHost
import random

class OopsAllPsychos(Effect):
    effect_name = "oops_all_psychos"
    display_name = "Oops All Psychos"

    def set_spawns(self):
        no_spawn = make_struct("GameplayTag",TagName="None")
        for point in find_all("SpawnPoint",False):
            point.SetSpawnStyleTag(no_spawn)
        
        psychos = find_object('SpawnOptionData','/Game/Enemies/_Spawning/CotV/_Mixes/Zone_1/SpawnOptions_CoVPsychosMix_City.SpawnOptions_CoVPsychosMix_City')
        for factory in find_all("SpawnerComponent",False):
            if "Default" in str(factory) or not factory.Spawner:
                continue
            if not factory.Spawner.GetSpawnerTeamComponent().EvaluatedTeam in blacklist_teams and factory.GbxSpawner.Class.Name != "OakMissionSpawner":
                factory.SetSpawnOptions(psychos)


    def oops_psychos_dim(self, obj: UObject, args: WrappedStruct,ret: Any, func: BoundFunction) -> Any:
        self.set_spawns()

    def run_effect(self):
        if AmIHost():
            self.set_spawns()
        else:
            SendToHost(self)
        return super().run_effect()
    
    def on_map_change(self):
        add_hook("/Script/OakGame.GFxExperienceBar:extFinishedDim", Type.PRE, "oops_psychos_dim", self.oops_psychos_dim)
        return super().on_map_change()

    def stop_effect(self):
        if AmIHost():
            remove_hook("/Script/OakGame.GFxExperienceBar:extFinishedDim", Type.PRE, "oops_psychos_dim")
        return super().stop_effect()
    
#r.TextureStreaming.PoolSize
#r.ScreenPercentage

class LaunchPlayer(Effect):
    effect_name = "launch_player"
    display_name = "Launch Player"
    def run_effect(self):
        if AmIHost():
            CurrentVel = self.pc.Pawn.OakCharacterMovement.Velocity
            CurrentVel.Z += 10000
            self.pc.Pawn.LaunchPawn(CurrentVel, True, True)
        else:
            SendToHost(self)
        return super().run_effect()
    

class ClutterInventory(Effect):
    effect_name = "clutter_inventory"
    display_name = "Clutter Backpack"
    def run_effect(self):
        if AmIHost():
            ItemPoolData = find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/Guns/ItemPool_TrialsChests.ItemPool_TrialsChests")
                
            init = find_class("Init_RandomLootCount_LotsAndLots_C")

            for i in range(25):
                oak_blueprint_library.GiveRewardItem(self.pc.Pawn,self.pc.Pawn,ItemPoolData,init)
        else:
            SendToHost(self)
        return super().run_effect()
    

class ReportToLilith(Effect):
    effect_name = "report_to_lilith"
    display_name = "Report To Lilith"
    def run_effect(self):
        Station = find_object('FastTravelStationData','/Game/GameData/FastTravel/FTS_Sanctuary.FTS_Sanctuary')
        FastTravel:UObject
        for travel in find_all("FastTravelStationComponent"):
            if "Default" not in str(travel):
                FastTravel = travel
                break
        FastTravel.FastTravelToStation(self.pc.Pawn, Station, self.pc.Pawn)
        return super().run_effect()
    
    def map_change_finalized(self):
        loc = make_struct("Vector",X= 14727.2,Y=-7662.9,Z=-4.88)
        rot = make_struct("Rotator",Yaw=-45.9)
        self.pc.Pawn.K2_TeleportTo(loc,rot)
        return super().map_change_finalized()
    

class SillyScales(Effect):
    effect_name = "silly_scales"
    display_name = "Silly Scales"
    def GetRandomizedScale(self) -> WrappedStruct:
        RandomX = random.uniform(0.1, 2.5)
        RandomY = random.uniform(0.1, 2.5)
        RandomZ = random.uniform(0.5, 1.5)
        return make_struct("Vector", X=RandomX,Y=RandomY,Z=RandomZ)

    def SillyScalesPawnPossessed(self, obj: UObject, args: WrappedStruct,ret: Any, func: BoundFunction) -> Any:
        if not obj.IsPlayerControlled():
            obj.SetActorScale3D(self.GetRandomizedScale())

    def run_effect(self):
        add_hook("/Script/Engine.Pawn:ReceivePossessed", Type.POST, "SillyScalesPawnPossessed", self.SillyScalesPawnPossessed)
        for Pawn in GetPawnList(False):
            Pawn.SetActorScale3D(self.GetRandomizedScale())
        return super().run_effect()
    
    def stop_effect(self):
        remove_hook("/Script/Engine.Pawn:ReceivePossessed", Type.POST, "SillyScalesPawnPossessed")
        return super().stop_effect()
    
gameplay_statics = find_class("GameplayStatics").ClassDefaultObject
class SpawnVehicle(Effect):
    effect_name = "spawn_vehicle"
    display_name = "Spawn Vehicle"
    def run_effect(self):
        if AmIHost():
            ride = gameplay_statics.SpawnObject(find_class("CatchARide"), self.pc)
            platform = gameplay_statics.SpawnObject(find_class("CatchARidePlatform"), self.pc)
            ride.CatchARide_Platform1 = platform

            player_loc = self.pc.Pawn.K2_GetActorLocation()
            player_rot = self.pc.Pawn.K2_GetActorRotation()

            veh_index = self.pc.CurrentSavegame.VehicleLastLoadoutIndex
            car = self.pc.VehicleSpawnerComponent.VehicleLoadouts[veh_index]

            if "revolver" in str(car.body).lower():
                platform.PlatformSafeZone.K2_SetRelativeLocationAndRotation(player_loc, player_rot, False, IGNORE_STRUCT, True)
                platform.PlatformSmallVehicleSafeZone1.K2_SetRelativeLocationAndRotation(player_loc, player_rot, False, IGNORE_STRUCT, True)
                platform.SmallVehicleSpawnSocket1.K2_SetRelativeLocationAndRotation(player_loc, player_rot, False, IGNORE_STRUCT, True)
            else:
                platform.K2_SetActorLocationAndRotation(player_loc, player_rot, False, IGNORE_STRUCT, True)

            self.pc.SpawnVehicleFromConfig(self.pc.Pawn.PlayerBalanceState.GetExperienceLevel(),car,ride)
        else:
            SendToHost(self)
        return super().run_effect()

class HarvestEvent(Effect):
    effect_name = "harvest_event"
    display_name = "Bloody Harvest"

    def run_effect(self):
        misson_class = None
        for mission in self.pc.PlayerMissionComponent.CachedMissionTracker.MissionList:
            if mission.MissionClass.Name == "Mission_Season_01_Intro_C":
                misson_class = mission.MissionClass
                mission.Status= 1
                mission.ObjectivesProgress= [1, 1, 1, 25, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                mission.ActiveObjectiveSet= find_object('MissionObjectiveSet','/Game/PatchDLC/BloodyHarvest/Missions/Side/Seasonal/Mission_Season_01_Intro.Set_FindLeagueBoss_ObjectiveSet')
                mission.bKickoffPlayed= True

        self.pc.PlayerMissionComponent.ServerSetTrackedMission(misson_class)
        LevelTravelStation = find_object('FastTravelStationData','/Game/PatchDLC/BloodyHarvest/GameData/FastTravel/LevelTravelData/FTS_BloodyHarvest.FTS_BloodyHarvest')
        FastTravel:UObject
        for travel in find_all("FastTravelStationComponent"):
            if "Default" not in str(travel) and "GEN_VARIABLE" not in str(travel):
                FastTravel = travel
                break
        FastTravel.FastTravelToStation(self.pc.Pawn, LevelTravelStation, self.pc.Pawn)
        return super().run_effect()


class CartelEvent(Effect):
    effect_name = "cartel_event"
    display_name = "Revenge Of The Cartels"

    def run_effect(self):
        misson_class = None
        for mission in self.pc.PlayerMissionComponent.CachedMissionTracker.MissionList:
            if mission.MissionClass.Name == "Mission_Season_02_Intro_C":
                misson_class = mission.MissionClass
                mission.Status= 1
                mission.ObjectivesProgress= [1, 1, 0, 0, 0, 30, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                mission.ActiveObjectiveSet= find_object('MissionObjectiveSet','/Game/PatchDLC/Event2/Missions/Side/Seasonal/Mission_Season_02_Intro.Set_GoToLeagueMap_ObjectiveSet')
                mission.bKickoffPlayed= True

        self.pc.PlayerMissionComponent.ServerSetTrackedMission(misson_class)
        
        LevelTravelStation = find_object('FastTravelStationData','/Game/PatchDLC/Event2/GameData/FastTravel/LevelTravelData/FTS_CartelHideout.FTS_CartelHideout')
        FastTravel:UObject
        for travel in find_all("FastTravelStationComponent"):
            if "Default" not in str(travel) and "GEN_VARIABLE" not in str(travel):
                FastTravel = travel
                break

        FastTravel.FastTravelToStation(get_pc().Pawn, LevelTravelStation, get_pc().Pawn)
        return super().run_effect()


WeaponStatics = find_class("WeaponStatics").ClassDefaultObject
class HideWeapons(Effect):
    effect_name = "hide_weapons"
    display_name = "Hide Weapons"

    def run_effect(self):
        if AmIHost():
            WeaponStatics.HideWeapons(self.pc.Pawn, "CrowdControl_Weapons")
        else:
            SendToHost(self)
        return super().run_effect()
    
    def stop_effect(self):
        if AmIHost():
            WeaponStatics.UnhideWeapons(self.pc.Pawn, "CrowdControl_Weapons")
        return super().stop_effect()
    
GbxGameSystemCoreBlueprintLibrary = find_class("GbxGameSystemCoreBlueprintLibrary").ClassDefaultObject
class DisableJumping(Effect):
    effect_name = "disable_jumping"
    display_name = "Disable Jumping"

    def run_effect(self):
        if AmIHost():
            GbxGameSystemCoreBlueprintLibrary.ResourceLockJumping(self.pc.Pawn, "CrowdControl_Jumping")
        else:
            SendToHost(self)
        return super().run_effect()
    
    def stop_effect(self):
        if AmIHost():
            GbxGameSystemCoreBlueprintLibrary.ResourceUnlockJumping(self.pc.Pawn, "CrowdControl_Jumping")
        return super().stop_effect()
    
class DisableMantling(Effect):
    effect_name = "disable_mantling"
    display_name = "Disable Mantling"

    def run_effect(self):
        if AmIHost():
            GbxGameSystemCoreBlueprintLibrary.ResourceLockMantling(self.pc.Pawn, "CrowdControl_Mantle")
        else:
            SendToHost(self)
        return super().run_effect()
    
    def stop_effect(self):
        if AmIHost():
            GbxGameSystemCoreBlueprintLibrary.ResourceUnlockMantling(self.pc.Pawn, "CrowdControl_Mantle")
        return super().stop_effect()    
    
class DisableCrouch(Effect):
    effect_name = "disable_crouch"
    display_name = "Disable Crouching"

    def run_effect(self):
        if AmIHost():
            GbxGameSystemCoreBlueprintLibrary.ResourceLockCrouching(self.pc.Pawn, "CrowdControl_Crouch")
        else:
            SendToHost(self)
        return super().run_effect()
    
    def stop_effect(self):
        if AmIHost():
            GbxGameSystemCoreBlueprintLibrary.ResourceUnlockCrouching(self.pc.Pawn, "CrowdControl_Crouch")
        return super().stop_effect()