from .Effect import Effect
from typing import Any
from unrealsdk import find_object, make_struct, find_all, find_class
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct
from unrealsdk.hooks import Type, add_hook, remove_hook 
from .Utils import blacklist_teams,oak_blueprint_library,GetPawnList
import random

class OopsAllPsychos(Effect):
    effect_name = "oops_all_psychos"
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
        self.set_spawns()
        return super().run_effect()
    
    def on_map_change(self):
        add_hook("/Script/OakGame.GFxExperienceBar:extFinishedDim", Type.PRE, "oops_psychos_dim", self.oops_psychos_dim)
        return super().on_map_change()

    def stop_effect(self):
        remove_hook("/Script/OakGame.GFxExperienceBar:extFinishedDim", Type.PRE, "oops_psychos_dim")
        return super().stop_effect()
    
#r.TextureStreaming.PoolSize
#r.ScreenPercentage

class LaunchPlayer(Effect):
    effect_name = "launch_player"
    def run_effect(self):
        CurrentVel = self.pc.Pawn.OakCharacterMovement.Velocity
        CurrentVel.Z += 10000
        self.pc.Pawn.LaunchPawn(CurrentVel, True, True)
        return super().run_effect()
    

class ClutterInventory(Effect):
    effect_name = "clutter_inventory"

    def run_effect(self):
        ItemPoolData = find_object("ItemPoolData", "/Game/GameData/Loot/ItemPools/Guns/ItemPool_TrialsChests.ItemPool_TrialsChests")
            
        init = find_class("Init_RandomLootCount_LotsAndLots_C")

        for i in range(25):
            oak_blueprint_library.GiveRewardItem(self.pc.Pawn,self.pc.Pawn,ItemPoolData,init)
        return super().run_effect()
    

class ReportToLilith(Effect):
    effect_name = "report_to_lilith"

    def run_effect(self):
        Station = find_object('FastTravelStationData','/Game/GameData/FastTravel/FTS_Sanctuary.FTS_Sanctuary')
        FastTravel = find_class("FastTravelStationComponent").ClassDefaultObject
        FastTravel.FastTravelToStation(self.pc.Pawn, Station, self.pc.Pawn)
        return super().run_effect()
    
    def map_change_finalized(self):
        loc = make_struct("Vector",X= 14727.2,Y=-7662.9,Z=-4.88)
        rot = make_struct("Rotator",Yaw=-45.9)
        self.pc.Pawn.K2_TeleportTo(loc,rot)
        return super().map_change_finalized()
    
class SillyScales(Effect):
    effect_name = "silly_scales"

    def GetRandomizedScale(self) -> WrappedStruct:
        RandomScale = random.uniform(0.1, 2.5)
        return make_struct("Vector", X=RandomScale,Y=RandomScale,Z=RandomScale)

    def run_effect(self):
        for Pawn in GetPawnList():
            Pawn.SetActorScale3D(self.GetRandomizedScale())
        return super().run_effect()