using ConnectorLib.SimpleTCP;
using CrowdControl.Common;
using ConnectorType = CrowdControl.Common.ConnectorType;

namespace CrowdControl.Games.Packs.Borderlands3;

public class Borderlands3 : SimpleTCPPack<SimpleTCPServerConnector>
{
    public Borderlands3(UserRecord player, Func<CrowdControlBlock, bool> responseHandler, Action<object> statusUpdateHandler) : base(player, responseHandler, statusUpdateHandler)
    {
    }

    public override Game Game => new("Borderlands 3", "Borderlands3", "PC", ConnectorType.SimpleTCPServerConnector);

    protected override string ProcessName => "Borderlands3.exe";

    public override string Host => "127.0.0.1";

    public override ushort Port => 42069; // pick something within 1024~49151

    public override ISimplePipelinePack.AuthenticationType AuthenticationMode => ISimplePipelinePack.AuthenticationType.None;

    public override EffectList Effects => new Effect[]
    {
        new("1 Health", "1_health") { Price = 50 },
        new("No Gravity", "no_gravity") { Duration = 30, Price = 75 },
        new("Oops All Psychos", "oops_all_psychos") { Duration = 300, Price = 100 },
        new("Spawn Legendary Weapon", "spawnloot_legendaryweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 250 },
        new("Launch Player", "launch_player") { Price = 150 },
        new("Clutter Backpack", "clutter_inventory") { Price = 500 },
        //new("Meet Lilith on the Bridge", "report_to_lilith") { Duration = 30 },
        new("Silly Scales", "silly_scales") { Duration = 300, Price = 90 },
        new("Spawn Loot Tink", "spawnenemy_loottink_1") { Category = new EffectGrouping("Spawn Enemies"), Price = 300 },
        new("BEES!", "spawnenemy_ratchswarm_20") { Category = new EffectGrouping("Spawn Enemies"), Price = 150 },
        //new("Start Bloody Harvest", "harvest_event") { Category = new EffectGrouping("Events") },
        //new("Start Revenge Of The Cartels", "cartel_event") { Duration = 300, Category = new EffectGrouping("Events") },
        new("Instant Death", "instant_death") { Price = 2000 },
        new("Drop Entire Inventory", "drop_entire_inventory") { Price = 500 },
        new("Spawn Vehicle", "spawn_vehicle") { Price = 125 },
        new("Highs And Lows", "HighsLows") { Price = 750 },
        new("Super Hot", "super_hot") { Duration = 60, Price = 450 },
        //new("Size Steal", "size_steal") { Duration = 60 },
        new("Delete Ground Items", "delete_ground_items") { Price = 1000 },
        new("Enable Fall Damage", "fall_damage") { Duration = 60, Price = 250 },
        new("Hide Weapons", "hide_weapons") { Duration = 60, Category = new EffectGrouping("Player Effects"), Price = 50 },
        new("Disable Jumping", "disable_jumping") { Duration = 60, Category = new EffectGrouping("Player Effects"), Price = 110 },
        new("Disable Mantling", "disable_mantling") { Duration = 60, Category = new EffectGrouping("Player Effects"), Price = 110 },
        new("Disable Crouching", "disable_crouch") { Duration = 60, Category = new EffectGrouping("Player Effects"), Price = 110 },
        new("Barrel Net", "barrel_net") { Price = 1250 },
        new("Drop Held Weapon", "drop_held_weapon") { Price = 150 },
        new("Drop Equipped Shield", "drop_equipped_shield") { Price = 100 },
        new("Empty Weapon Ammo", "no_ammo") { Price = 200 },
        new("Reset Skill Trees", "reset_skill_trees") { Price = 750 },
        new("Viewer Badass", "viewer_badass") { Price = 500 },
        new("Fast Game Speed", "fast_game_speed") { Duration = 30, Price = 350 },
        new("Slow Game Speed", "slow_game_speed") { Duration = 30, Price = 350 },
        new("Fly", "fly_mode") { Duration = 60, Price = 500 },
        //new("Hype Train (remove this before shipping i think)", "event-hype-train"),
        new("Full Ammo", "full_ammo") { Price = 400 },
        new("Vendor Box", "vendor_box") { Price = 850 },
        new("Give 5k Eridium", "givecurrency_Eridium_5000") { Price = 500 },
        new("Give 5m Cash", "givecurrency_Cash_5000000") { Price = 500 },
        new("Splash Immunity", "NoSplash") { Duration = 120, Price = 200 },
        new("Red Chest", "red_chest") { Price = 400 },
        new("Full Ammo", "full_ammo") { Price =  400 },
        new("Vendor Box", "vendor_box") { Price =  850 },
        new("Give 5k Eridium", "givecurrency_Eridium_5000") { Price =  500 },
        new("Give 5m Cash", "givecurrency_Cash_5000000") { Price =  500 },
        new("Splash Immunity", "NoSplash") { Duration = 120, Price =  200 },
        new("Red Chest", "red_chest") { Price =  400 },
        new("Spawn Invincible", "spawn_invincible") { Price =  1000 },
    };
}
