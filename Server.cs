using ConnectorLib.SimpleTCP;
using CrowdControl.Common;
using ConnectorType = CrowdControl.Common.ConnectorType;

namespace CrowdControl.Games.Packs.borderlands3;

public class borderlands3 : SimpleTCPPack<SimpleTCPServerConnector>
{
    public borderlands3(UserRecord player, Func<CrowdControlBlock, bool> responseHandler, Action<object> statusUpdateHandler) : base(player, responseHandler, statusUpdateHandler)
    {
    }

    public override Game Game => new("Borderlands 3", "borderlands3", "PC", ConnectorType.SimpleTCPServerConnector);

    protected override string ProcessName => "Borderlands3.ex";

    public override string Host => "127.0.0.1";

    public override ushort Port => 42069; // pick something within 1024~49151

    public override ISimplePipelinePack.AuthenticationType AuthenticationMode => ISimplePipelinePack.AuthenticationType.None;

    public override EffectList Effects => new Effect[]
    {
        new("1 Health", "1_health"),
        new("No Gravity", "no_gravity") { Duration = 30 },
        new("Oops All Psychos", "oops_all_psychos") { Duration =  300 },
        new("Spawn Legendary Weapon", "spawnloot_legendaryweapon_1") { Category = new EffectGrouping("Spawn Loot") },
        new("Launch Player", "launch_player"),
        new("Clutter Backpack", "clutter_inventory"),
        new("Meet Lilith on the Bridge", "report_to_lilith") { Duration = 30 },
        new("Silly Scales", "silly_scales") { Duration = 300 },
        new("Spawn Loot Tink", "spawnenemy_loottink_1") { Category = new EffectGrouping("Spawn Enemies") },
        new("BEES!", "spawnenemy_ratchswarm_20") { Category = new EffectGrouping("Spawn Enemies") },
        new("Start Bloody Harvest", "harvest_event") { Category = new EffectGrouping("Events") },
        new("Start Revenge Of The Cartels", "cartel_event") { Duration = 300, Category = new EffectGrouping("Events") },
        new("Instant Death", "instant_death"),
        new("Drop Entire Inventory", "drop_entire_inventory"),
        new("Spawn Vehicle", "spawn_vehicle"),
        new("Highs And Lows", "HighsLows"),
        new("Super Hot", "super_hot") { Duration = 60 },
        //new("Size Steal", "size_steal") { Duration = 60 },
        new("Delete Ground Items", "delete_ground_items"),
        new("Enable Fall Damage", "fall_damage") { Duration = 60 },
        new("Hide Weapons", "hide_weapons") { Duration = 60, Category = new EffectGrouping("Player Effects") },
        new("Disable Jumping", "disable_jumping") { Duration = 60, Category = new EffectGrouping("Player Effects") },
        new("Disable Mantling", "disable_mantling") { Duration = 60, Category = new EffectGrouping("Player Effects") },
        new("Disable Crouching", "disable_crouch") { Duration = 60, Category = new EffectGrouping("Player Effects") },
        new("Barrel Net", "barrel_net"),
        new("Drop Held Weapon", "drop_held_weapon"),
        new("Drop Equipped Shield", "drop_equipped_shield"),
        new("Empty Weapon Ammo", "no_ammo"),
        new("Reset Skill Trees", "reset_skill_trees"),
        new("Viewer Badass", "viewer_badass"),
        new("Fast Game Speed", "fast_game_speed") { Duration = 30 },
        new("Slow Game Speed", "slow_game_speed") { Duration = 30 },
        new("Fly", "fly_mode") { Duration = 60 },
        //new("Hype Train (remove this before shipping i think)", "event-hype-train"),
        new("Full Ammo", "full_ammo"),
        new("Vendor Box", "vendor_box"),
        new("Give 5k Eridium", "givecurrency_Eridium_5000"),
        new("Give 5m Cash", "givecurrency_Cash_5000000"),
    };
}
