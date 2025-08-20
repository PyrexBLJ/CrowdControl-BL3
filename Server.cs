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
    };
}
