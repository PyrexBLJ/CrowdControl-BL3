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
        new("Barrel Troll", "barrel_troll"),
        new("No Gravity", "no_gravity") { Duration = 30 },
        new("No Ammo", "no_ammo"),
        new("Oops All Psychos", "oops_all_psychos") { Duration =  300 },
        new("Spawn Legendary Weapon", "spawnloot_legendaryweapon_1") { Category = new EffectGrouping("Spawn Loot") },
        new("Launch Player", "launch_player"),
        new("Clutter Backpack", "clutter_inventory"),
        new("Meet Lilith on the Bridge", "report_to_lilith") { Duration = 30 },
        new("Silly Scales", "silly_scales") { Duration = 300 },
        new("Spawn Loot Tink", "spawnenemy_loottink_1") { Category = new EffectGrouping("Spawn Enemies") },
        new("Start Bloody Harvest", "harvest_event") { Category = new EffectGrouping("Events") },
        new("Start Revenge Of The Cartels", "cartel_event") { Duration = 300, Category = new EffectGrouping("Events") },
        new("Instant Death", "instant_death"),
        new("Drop Entire Inventory", "drop_entire_inventory"),
        new("Spawn Vehicle", "spawn_vehicle"),

    };
}
