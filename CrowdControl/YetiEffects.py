from .Effect import Effect
from unrealsdk import find_object, make_struct, find_all, find_class #type:ignore
from mods_base import get_pc


blacklist_teams = [
    "NonPlayers",
    "Players",
    "Team_Ghost",
    "Friendly to All",
    "Team_Neutral",
]


class OopsAllPsychos(Effect):
    effect_name = "Oops All Psychos"
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


    def run_effect(self):
        self.set_spawns()
        return super().run_effect()
    
    def map_change_finalized(self):
        print("oops psychos map change")
        self.set_spawns()
        return super().map_change_finalized()
    
    
