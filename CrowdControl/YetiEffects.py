from .Effect import Effect
from typing import Any
from unrealsdk import find_object, make_struct, find_all
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct
from unrealsdk.hooks import Type, add_hook, remove_hook 
from .Utils import blacklist_teams


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