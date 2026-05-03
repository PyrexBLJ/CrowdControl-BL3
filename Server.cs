using ConnectorLib.SimpleTCP;
using CrowdControl.Common;
using ConnectorType = CrowdControl.Common.ConnectorType;

namespace CrowdControl.Games.Packs.Borderlands2;

public class Borderlands2 : SimpleTCPPack<SimpleTCPServerConnector>
{
    public Borderlands2(UserRecord player, Func<CrowdControlBlock, bool> responseHandler, Action<object> statusUpdateHandler) : base(player, responseHandler, statusUpdateHandler)
    {
    }

    public override Game Game => new("Borderlands 2", "Borderlands2", "PC", ConnectorType.SimpleTCPServerConnector);

    protected override string ProcessName => "Borderlands2.exe";

    public override string Host => "127.0.0.1";

    public override ushort Port => 42069; // pick something within 1024~49151

    public override ISimplePipelinePack.AuthenticationType AuthenticationMode => ISimplePipelinePack.AuthenticationType.None;

    public override EffectList Effects => new Effect[]
    {
        new("1 Health", "1_health") { Price = 50, Category = new EffectGrouping("Player Effects") },
        new("Low Gravity", "low_gravity") { Duration = 30, Price = 75, Category = new EffectGrouping("Player Effects") },
        new("Launch Player", "launch_player") { Price = 150, Category = new EffectGrouping("Player Effects") },
        new("Instant Death", "instant_death") { Price = 2000, Category = new EffectGrouping("Player Effects") },
        new("Drop Entire Inventory", "drop_entire_inventory") { Price = 500, Category = new EffectGrouping("Player Effects") },
        new("Super Hot", "super_hot") { Duration = 60, Price = 450, Category = new EffectGrouping("Player Effects") },
        new("Hide Weapons", "hide_weapons") { Duration = 60, Category = new EffectGrouping("Player Effects"), Price = 50 },
        new("Disable Jumping", "disable_jumping") { Duration = 60, Category = new EffectGrouping("Player Effects"), Price = 110 },
        new("Drop Held Weapon", "drop_held_weapon") { Price = 150, Category = new EffectGrouping("Player Effects") },
        new("Drop Equipped Shield", "drop_equipped_shield") { Price = 100, Category = new EffectGrouping("Player Effects") },
        new("Empty Weapon Ammo", "no_ammo") { Price = 200, Category = new EffectGrouping("Player Effects") },
        new("Reset Skill Trees", "reset_skill_trees") { Price = 750, Category = new EffectGrouping("Player Effects") },
        new("Fly", "fly_mode") { Duration = 60, Price = 150, Category = new EffectGrouping("Player Effects") },
        new("Full Ammo", "full_ammo") { Price = 100, Category = new EffectGrouping("Player Effects") },
        new("Give 500 Eridium", "givecurrency_Eridium_500") { Price = 100, Category = new EffectGrouping("Player Effects") },
        new("Give 5m Cash", "givecurrency_Cash_5000000") { Price = 100, Category = new EffectGrouping("Player Effects") },
        new("Give 120 Seraph Crystals", "givecurrency_SeraphCrystal_120") { Price = 100, Category = new EffectGrouping("Player Effects") },
        new("Give 613 Torgue Tokens", "givecurrency_TorgueToken_613") { Price = 100, Category = new EffectGrouping("Player Effects") },
        new("Stretch Time", "stretch_time") { Duration = 60, Price = 50, Category = new EffectGrouping("Player Effects") },
        new("Fast Movement", "fast_movement") { Duration = 60, Price = 75, Category = new EffectGrouping("Player Effects") },


        new("Silly Scales", "silly_scales") { Duration = 300, Price = 90, Category = new EffectGrouping("World Effects") },
        new("Delete Ground Items", "delete_ground_items") { Price = 1000, Category = new EffectGrouping("World Effects") },
        new("Enable Fall Damage", "fall_damage") { Duration = 60, Price = 250, Category = new EffectGrouping("World Effects") },
        new("Barrel Net", "barrel_net") { Price = 500, Category = new EffectGrouping("World Effects") },
        new("Fast Game Speed", "fast_game_speed") { Duration = 30, Price = 350, Category = new EffectGrouping("World Effects") },
        new("Slow Game Speed", "slow_game_speed") { Duration = 30, Price = 350, Category = new EffectGrouping("World Effects") },
        new("Vendor Box", "vendor_box") { Price = 850, Category = new EffectGrouping("World Effects") },
        new("Red Chest", "red_chest") { Price = 400, Category = new EffectGrouping("World Effects") },
        new("One Shot Kills", "one_shot") { Duration = 30, Price = 250, Category = new EffectGrouping("World Effects") },
        new("Gamba Time", "gamba_time") { Price = 400, Category = new EffectGrouping("World Effects") },
        new("Painful Plants", "painful_plants") { Price = 500, Category = new EffectGrouping("World Effects") },
        new("Low World Gravity", "low_world_gravity") { Duration = 60, Price = 150, Category = new EffectGrouping("World Effects") },

        new("Viewer Badass", "viewer_badass") { Price = 500, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Doc Mercy", "spawn-enemy_docmercy") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Badass Creeper", "spawn-enemy_badasscreeper") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Hunter Hellquist", "spawn-enemy_hunterhellquist") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Foreman Rusty", "spawn-enemy_foremanrusty") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Gettle", "spawn-enemy_gettle") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Mobley", "spawn-enemy_mobley") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Smash Head", "spawn-enemy_smashhead") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Bone Head", "spawn-enemy_bonehead2") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Assassin Wot", "spawn-enemy_assassinwot") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Assassin Oney", "spawn-enemy_assassinoney") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Assassin Reeth", "spawn-enemy_assassinreeth") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Assassin Rouf", "spawn-enemy_assassinrouf") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Mick Zafford", "spawn-enemy_mickzaford") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Tector Hodunk", "spawn-enemy_tectorhodunk") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Bad Maw", "spawn-enemy_badmaw") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Mad Mike", "spawn-enemy_madmike") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Prospector Zeke", "spawn-enemy_prospectorzeke") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Donkey Mong", "spawn-enemy_donkeymong") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn King Mong", "spawn-enemy_kingmong") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Midgemong", "spawn-enemy_midgemong") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Incinerator Clayton", "spawn-enemy_incineratorclayton") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Mad Dog", "spawn-enemy_maddog") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn McNally", "spawn-enemy_mcnally") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Rakkman", "spawn-enemy_rakkman") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Savage Lee", "spawn-enemy_savagelee") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Son of Mothrakk", "spawn-enemy_sonofmothrakk") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Dan", "spawn-enemy_dan") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Lee", "spawn-enemy_lee") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Mick", "spawn-enemy_mick") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Ralph", "spawn-enemy_ralph") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Flinter", "spawn-enemy_flinter") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Laney White", "spawn-enemy_laneywhite") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Mortar", "spawn-enemy_mortar") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Sheriff of Lynchwood", "spawn-enemy_sheriffoflynchwood") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Dukino's Mom", "spawn-enemy_dukinosmom") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Pimon", "spawn-enemy_pimon") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Tumbaa", "spawn-enemy_tumbaa") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Black Queen", "spawn-enemy_blackqueen") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Scorch", "spawn-enemy_scorch") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Henry", "spawn-enemy_henry") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Old Slappy", "spawn-enemy_oldslappy") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Boll", "spawn-enemy_boll") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Madame Von Bartlesby", "spawn-enemy_madamevonbartlesby") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Spycho", "spawn-enemy_spycho") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn W4R-D3N", "spawn-enemy_w4rd3n") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Blue", "spawn-enemy_blue") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Warlord Grug", "spawn-enemy_warlordgrug") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Warlord Slog", "spawn-enemy_warlordslog") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Warlord Turge", "spawn-enemy_warlordturge") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Spiderpants", "spawn-enemy_spiderpants") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Lt Bolson", "spawn-enemy_ltbolson") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Lt Angvar", "spawn-enemy_ltangvar") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Lt Hoffman", "spawn-enemy_lthoffman") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Lt Tetra", "spawn-enemy_lttetra") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Sparky, Son of Flynt", "spawn-enemy_sonofflynt") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Sully The Stabber", "spawn-enemy_sullythestabber") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn No Beard", "spawn-enemy_nobeard") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Roscoe", "spawn-enemy_roscoe") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Clark the Combusted Cryptkeeper", "spawn-enemy_clark") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Sully the Blacksmith", "spawn-enemy_sullytheblacksmith") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Arizona", "spawn-enemy_arizona") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Bulstoss", "spawn-enemy_bulstoss") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Rouge", "spawn-enemy_rouge") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Der Monstrositat", "spawn-enemy_dermonstrositat") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Rakkanoth", "spawn-enemy_rakkanoth") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Dribbles", "spawn-enemy_dribbles") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Bloodtail", "spawn-enemy_bloodtail") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Chubby", "spawn_chubby") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },
        new("Spawn Loot Midget", "spawn_lootboi") { Price = 100, Quantity = 25, Category = new EffectGrouping("Spawn Enemies") },

        new("Spawn Knuckledragger", "spawn-enemy_knuckledragger") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Boom", "spawn-enemy_boom") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Bewm", "spawn-enemy_bewm") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Captain Flynt", "spawn-enemy_captainflynt") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Wilhelm", "spawn-enemy_wilhelm") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Saturn", "spawn-enemy_saturn") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn BNK-3R", "spawn-enemy_bnk3r") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Mr Boney Pants Guy", "spawn-enemy_mrboneypantsguy") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Skeleton King", "spawn-enemy_skeletonking") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Hector", "spawn-enemy_hector") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Cassius", "spawn-enemy_cassius") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Uranus", "spawn-enemy_uranus") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Pistons Blimp", "spawn-enemy_blimp") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Motor Mama", "spawn-enemy_motormama") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Piston", "spawn-enemy_piston") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn H3RL-E", "spawn-enemy_herle") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Pumpkin Kingpin", "spawn-enemy_pumpkinkingpin") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        new("Spawn Tinder Snowflake", "spawn-enemy_tindersnowflake") { Price = 250, Quantity = 25, Category = new EffectGrouping("Spawn Bosses") },
        
        new("Spawn Vermivorous the Invincible", "spawn-enemy_vermi") { Price = 500, Category = new EffectGrouping("Spawn Raid Bosses") },
        new("Spawn Terramorphous the Invincible", "spawn-enemy_terra") { Price = 500, Category = new EffectGrouping("Spawn Raid Bosses") },
        new("Spawn Healianth the Invincible", "spawn-enemy_bluedragon") { Price = 500, Category = new EffectGrouping("Spawn Raid Bosses") },
        new("Spawn Incinerator the Invincible", "spawn-enemy_reddragon") { Price = 500, Category = new EffectGrouping("Spawn Raid Bosses") },
        new("Spawn Brood the Invincible", "spawn-enemy_greendragon") { Price = 500, Category = new EffectGrouping("Spawn Raid Bosses") },
        new("Spawn Boost the Invincible", "spawn-enemy_purpledragon") { Price = 500, Category = new EffectGrouping("Spawn Raid Bosses") },
        new("Spawn Pyro Pete the Invincible", "spawn-enemy_pyropete") { Price = 500, Category = new EffectGrouping("Spawn Raid Bosses") },
        new("Spawn 010011110100110101000111-010101110101010001001000", "spawn-enemy_omgwth") { Price = 500, Category = new EffectGrouping("Spawn Raid Bosses") },
        new("Spawn Dexiduous the Invincible", "spawn-enemy_dexi") { Price = 500, Category = new EffectGrouping("Spawn Raid Bosses") },
        

        new("Spawn Legendary Weapon", "spawnloot_legendaryweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 250 },
        new("Spawn Purple Weapon", "spawnloot_purpleweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 200 },
        new("Spawn Blue Weapon", "spawnloot_blueweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 150 },
        new("Spawn Green Weapon", "spawnloot_greenweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 100 },
        new("Spawn White Weapon", "spawnloot_whiteweapon_1") { Category = new EffectGrouping("Spawn Loot"), Price = 50 },
        new("Clutter Backpack", "clutter_inventory") { Price = 500, Category = new EffectGrouping("Spawn Loot") },
        new("Spawn Candy", "spawn_candy") { Category = new EffectGrouping("Spawn Loot"), Price = 50 },
        new("Spawn Wisps", "spawn_wisps") { Category = new EffectGrouping("Spawn Loot"), Price = 50 },

        new("Hype Train", "event-hype-train"),
    };
}
