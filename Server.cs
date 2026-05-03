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
        new("1 Health", "1_health") { Price = 50, Category = new EffectGrouping("Player Effects") },
        new("No Gravity", "no_gravity") { Duration = 30, Price = 75, Category = new EffectGrouping("Player Effects") },
        new("Launch Player", "launch_player") { Price = 150, Category = new EffectGrouping("Player Effects") },
        new("Instant Death", "instant_death") { Price = 2000, Category = new EffectGrouping("Player Effects") },
        new("Drop Entire Inventory", "drop_entire_inventory") { Price = 500, Category = new EffectGrouping("Player Effects") },
        new("Highs And Lows", "HighsLows") { Price = 750, Category = new EffectGrouping("Player Effects") },
        new("Super Hot", "super_hot") { Duration = 60, Price = 450, Category = new EffectGrouping("Player Effects") },
        new("Hide Weapons", "hide_weapons") { Duration = 60, Category = new EffectGrouping("Player Effects"), Price = 50 },
        new("Disable Jumping", "disable_jumping") { Duration = 60, Category = new EffectGrouping("Player Effects"), Price = 110 },
        new("Disable Mantling", "disable_mantling") { Duration = 60, Category = new EffectGrouping("Player Effects"), Price = 110 },
        new("Disable Crouching", "disable_crouch") { Duration = 60, Category = new EffectGrouping("Player Effects"), Price = 110 },
        new("Drop Held Weapon", "drop_held_weapon") { Price = 150, Category = new EffectGrouping("Player Effects") },
        new("Drop Equipped Shield", "drop_equipped_shield") { Price = 100, Category = new EffectGrouping("Player Effects") },
        new("Empty Weapon Ammo", "no_ammo") { Price = 200, Category = new EffectGrouping("Player Effects") },
        new("Reset Skill Trees", "reset_skill_trees") { Price = 750, Category = new EffectGrouping("Player Effects") },
        new("Fly", "fly_mode") { Duration = 60, Price = 500, Category = new EffectGrouping("Player Effects") },
        new("Full Ammo", "full_ammo") { Price = 400, Category = new EffectGrouping("Player Effects") },
        new("Give 5k Eridium", "givecurrency_Eridium_5000") { Price = 500, Category = new EffectGrouping("Player Effects") },
        new("Give 5m Cash", "givecurrency_Cash_5000000") { Price = 500, Category = new EffectGrouping("Player Effects") },
        new("Splash Immunity", "NoSplash") { Duration = 120, Price = 200, Category = new EffectGrouping("Player Effects") },
        new("Random Moxxtail Booster", "moxx_tail") { Duration = 120, Price = 50, Category = new EffectGrouping("Player Effects") },
        new("Brain Nanobots (xp) Booster", "csbooster_xp") { Duration = 120, Price = 50, Category = new EffectGrouping("Player Effects") },
        new("Lucky Jabber Foot (cash) Booster", "csbooster_cash") { Duration = 120, Price = 50, Category = new EffectGrouping("Player Effects") },
        new("Caffeine Caplets (speed) Booster", "csbooster_speed") { Duration = 120, Price = 50, Category = new EffectGrouping("Player Effects") },
        new("Jabber-Cola (damage) Booster", "csbooster_damage") { Duration = 120, Price = 50, Category = new EffectGrouping("Player Effects") },
        new("Elemental Powder (elemental proc) Booster", "csbooster_element") { Duration = 120, Price = 50, Category = new EffectGrouping("Player Effects") },
        new("Butt Stallion Milk (loot) Booster", "csbooster_loot") { Duration = 120, Price = 50, Category = new EffectGrouping("Player Effects") },

        new("Silly Scales", "silly_scales") { Duration = 300, Price = 90, Category = new EffectGrouping("World Effects") },
        new("Delete Ground Items", "delete_ground_items") { Price = 1000, Category = new EffectGrouping("World Effects") },
        new("Enable Fall Damage", "fall_damage") { Duration = 60, Price = 250, Category = new EffectGrouping("World Effects") },
        new("Barrel Net", "barrel_net") { Price = 1250, Category = new EffectGrouping("World Effects") },
        new("Fast Game Speed", "fast_game_speed") { Duration = 30, Price = 350, Category = new EffectGrouping("World Effects") },
        new("Slow Game Speed", "slow_game_speed") { Duration = 30, Price = 350, Category = new EffectGrouping("World Effects") },
        new("Vendor Box", "vendor_box") { Price = 850, Category = new EffectGrouping("World Effects") },
        new("Red Chest", "red_chest") { Price = 400, Category = new EffectGrouping("World Effects") },
        new("Oops All Psychos", "oops_all_psychos") { Duration = 300, Price = 100, Category = new EffectGrouping("World Effects") },
        new("Spawn Vehicle", "spawn_vehicle") { Price = 125, Category = new EffectGrouping("World Effects") },
        new("One Shot Kills", "one_shot") { Duration = 30, Price = 250, Category = new EffectGrouping("World Effects") },

        new("Spawn Loot Tink", "spawn-enemy_loottink") { Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Price = 300 },
        new("BEES!", "spawnenemy_ratchswarm_20") { Category = new EffectGrouping("Spawn Enemies"), Price = 150 },
        new("Viewer Badass", "viewer_badass") { Price = 500, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Wotan the Invincible", "spawn_Wotan") { Price = 1000, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Psycho", "spawn-enemy_psycho") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Jabber", "spawn-enemy_jabber") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Skag", "spawn-enemy_skag") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Spiderant", "spawn-enemy_spiderant") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Rakklesnake", "spawn-enemy_rakklesnake") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Ratch", "spawn-enemy_ratch") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Saurian", "spawn-enemy_saurian") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Varkid", "spawn-enemy_varkid") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Wolven", "spawn-enemy_wolven") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Bellik", "spawn-enemy_bellik") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Tink", "spawn-enemy_tink") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Wraith", "spawn-enemy_wraith") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Trooper", "spawn-enemy_trooper") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn NOG", "spawn-enemy_nog") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Heavy", "spawn-enemy_heavy") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Nullhound", "spawn-enemy_nullhound") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Bot", "spawn-enemy_bot") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Loader", "spawn-enemy_loader") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Skrit", "spawn-enemy_skrit") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Rakk", "spawn-enemy_rakk") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Ravager", "spawn-enemy_ravager") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Atomic", "spawnenemy_atomic_1") { Price = 1000, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Hemovorous the Invincible", "spawnenemy_hemo_1") { Price = 1000, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn Tink of Cunning", "spawnenemy_toc_1") { Price = 1000, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn SpongeBoss BulletPants", "spawnenemy_sponge_1") { Price = 1000, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },
        new("Spawn FISH SLAP!", "spawnenemy_fishslap_1") { Price = 1000, Category = new EffectGrouping("Spawn Enemies"), Inactive = true },

        new("Spawn Legendary Weapon", "spawnloot_legendaryweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 250 },
        new("Spawn Purple Weapon", "spawnloot_purpleweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 200 },
        new("Spawn Blue Weapon", "spawnloot_blueweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 150 },
        new("Spawn Green Weapon", "spawnloot_greenweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 100 },
        new("Spawn White Weapon", "spawnloot_whiteweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 50 },
        new("Clutter Backpack", "clutter_inventory") { Price = 500, Category = new EffectGrouping("Spawn Loot") },

        new("Hype Train", "event-hype-train"),

        //new("Start Bloody Harvest", "harvest_event") { Category = new EffectGrouping("Events") },
        //new("Start Revenge Of The Cartels", "cartel_event") { Duration = 300, Category = new EffectGrouping("Events") },
        //new("Meet Lilith on the Bridge", "report_to_lilith") { Duration = 30 },
        //new("Size Steal", "size_steal") { Duration = 60 },
    };
}
