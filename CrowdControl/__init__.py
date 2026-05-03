import socket
import time
import select
import json
import base64
from mods_base import build_mod, hook, ButtonOption, DropdownOption #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct #type: ignore
from unrealsdk.hooks import Type #type: ignore
from typing import Any
from .Utils import AmIHost, CrowdControl_PawnList_Unpossessed, CrowdControl_PawnList_Possessed
from .Comms import *
from .Effect import *
from .OneHealth import *
from .SharedEffects import *
from .YetiEffects import *
from .PyrexEffects import *
from .GarwoodEffects import *
from .EpicEffects import *

__all__ = ["Load", "RequestEffect", "NotifyEffect", "Internal"]

Shared = None

TIMEOUT = 15

client = None

host = "127.0.0.1"
port = 42069

client_socket = None
shutdown = False
do_reset = False
wait_ticks = 0
buffer = b""
connecting = False

ResetConnection: ButtonOption = ButtonOption("Reset Connection To CC App", on_press = lambda _: connect_socket(host, port), description="If you didnt get the \"CrowdControl: Connected!\" message in the console (from opening the game before the cc app for example) click this button to retry the connection.")
ViewerBadassCooldown: DropdownOption = DropdownOption("Viewer Badass Cooldown (mins)", "0", ["0", "5", "10", "15", "30", "60"], description="How many minutes to wait before another viewer badass is allowed to spawn after it dies.")

def connect_socket(host, port):
    global client_socket, do_reset, connecting
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(False)
        s.connect_ex((host, port))
        client_socket = s
        connecting = True
        do_reset = True
        #print(f"CrowdControl: Connecting to {host}:{port}... (leaking this ip is fine you can relax)")
        SetEffectStatus("viewer_badass", 0x82, get_pc()) # failsafe to re-enable the viewer badass effect incase the streamer crashes during the cooldown
    except Exception as e:
        print(f"CrowdControl: Connection failed: {e}")
        client_socket = None
        connecting = False


@hook("WillowGame.WillowGameViewportClient:Tick", Type.PRE)
def CrowdControlSocket(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction,) -> Any:
    global shutdown, do_reset, wait_ticks, client_socket, buffer, connecting

    if client_socket is None:
        if time.time() - wait_ticks > 10:
            wait_ticks = time.time()
            connect_socket(host, port)
        return

    try:
        if connecting:
            _, writable, _ = select.select([], [client_socket], [], 0)
            if writable:
                connecting = False
                print("CrowdControl: Connected!")
            return

        ready, _, _ = select.select([client_socket], [], [], 0)
        if ready:
            chunk = client_socket.recv(1024)
            if not chunk:
                client_socket.close()
                client_socket = None
                print("CrowdControl: Disconnected")
                return

            buffer += chunk
            while True:
                atoms = buffer.split(b'\x00', 2)
                if len(atoms) < 2:
                    break

                message_bytes = atoms[0]
                buffer = atoms[1] if len(atoms) > 1 else b""

                try:
                    message = json.loads(message_bytes.decode('utf-8'))
                except Exception as e:
                    #print(f"CrowdControl: JSON parse error: {e}\n{message_bytes}")
                    continue

                if message["type"] != 253:
                    if str(ENGINE.GetCurrentWorldInfo().GetStreamingPersistentMapName().lower()) in ["menumap", "loader", "exampleentry"]:
                        NotifyEffect(message["id"], "Retry", message["code"], get_pc())
                        print("Crowd Control: Effect redeemed when it was not possible to activate, retrying.")
                        return
                    elif get_pc().bStatusMenuOpen or get_pc().IsPauseMenuOpen():
                        NotifyEffect(message["id"], "Retry", message["code"], get_pc())
                        print("Crowd Control: Effect redeemed while in a menu, retrying.")
                        return

                    eid = message["id"]
                    effect = message["code"]
                    viewer = message.get("viewer", "None")
                    viewers = message.get("viewers", None)
                    sourcedetails = message.get("sourceDetails", None)
                    duration = message.get("duration", None)
                    parameters = message.get("parameters", None)
                    quantity = message.get("quantity", None)

                    if duration:
                        duration /= 1000

                    if duration and parameters:
                        RequestEffect(eid=eid, effect_name=effect, pc=get_pc(), viewer=viewer, viewers=viewers, source=sourcedetails, duration=duration, quant=quantity, args=parameters)
                    elif parameters:
                        RequestEffect(eid=eid, effect_name=effect, pc=get_pc(), viewer=viewer, viewers=viewers, source=sourcedetails, duration=0, args=parameters, quant=quantity)
                    elif duration:
                        RequestEffect(eid=eid, effect_name=effect, pc=get_pc(), viewer=viewer, viewers=viewers, source=sourcedetails, duration=duration, quant=quantity)
                    else:
                        RequestEffect(eid=eid, effect_name=effect, pc=get_pc(), viewer=viewer, viewers=viewers, source=sourcedetails, duration=0, quant=quantity)

    except Exception as e:
        print(f"CrowdControl Socket Error: {e}")
        if client_socket:
            client_socket.close()
        client_socket = None
        connecting = False






@hook("Engine.PlayerController:ServerSpeech", Type.PRE)
def ServerChangeNameHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
#
#   This is where requests for effects will arrive to the host from the other clients in the game.
#   
#   We will have to make sure each request sent to the host contains the string CrowdControl in it, the clients PlayerID from their playerstate, the effect they want to be activated on them,
#   and probably the request id they got from the cc app so we can send it back to them with the status of the effect and their game can report it back to the cc app.
#
#   all of these should be separated by a character that wont be found in any of that data naturally (im guessing with - it might change later if it has to) and presented in the same order so we can easily break it out into what we need
#
#   something like CrowdControl-{PlayerID}-{Effect}-{RequestID}-{args}-{timeremaining}
#
#   you can see an example of this being called in the OneHealth effect
#
    if "CrowdControl" in args.Type:
        trimmedrequest: str = args.Callsign
        trimmedrequest = trimmedrequest.removeprefix("CrowdControl-")
        b64request: list = trimmedrequest.split("-")
        request = json.loads(base64.b64decode(b64request[1]).decode("utf-8"))
        request["pc"] = obj
        request["from_client"] = True
        # get_pc().PlayerReplicationInfo.PlayerID
        if str(get_pc().PlayerReplicationInfo.PlayerID) == str(obj.PlayerReplicationInfo.PlayerID):
            #print("Got a client request from ourself, discard it.")
            return None
        
        eid = request["id"]
        effect = b64request[0]
        viewer = request.get("viewer", "None")
        viewers = request.get("viewers", None)
        sourcedetails = request.get("sourceDetails", None)
        duration = request.get("duration", None)
        parameters = request.get("parameters", None)
        quantity = request.get("quantity", None)

        if duration and parameters:
            RequestEffect(eid=eid, effect_name=effect, pc=request["pc"], viewer=viewer, viewers=viewers, source=sourcedetails, duration=duration, args=parameters, quant=quantity)
        elif parameters:
            RequestEffect(eid=eid, effect_name=effect, pc=request["pc"], viewer=viewer, viewers=viewers, source=sourcedetails, duration=0, args=parameters, quant=quantity)
        elif duration:
            RequestEffect(eid=eid, effect_name=effect, pc=request["pc"], viewer=viewer, viewers=viewers, source=sourcedetails, duration=duration, quant=quantity)
        else:
            RequestEffect(eid=eid, effect_name=effect, pc=request["pc"], viewer=viewer, viewers=viewers, source=sourcedetails, duration=0, quant=quantity)

    return None

@hook("WillowGame.WillowPlayerController:ClientMessage", Type.PRE)
def ClientMessageHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
#
#   This is where players will get responses from the host
#
#   As im writing this i dont think we will really much more than this, def will have to handle timed events somehow but im not sure yet
#
    if args.type == "CrowdControl":
        if args.MsgLifeTime != float(get_pc().PlayerReplicationInfo.PlayerID) or AmIHost():
            return None
        
        response: list = args.S.split("-")

        NotifyEffect(response[0], response[1], response[2], get_pc()) #ngl idk the best way to deal with timeremaining yet
        
    if args.type == "CCEffectStatus":
        response: list = args.S.split("-")
        message = {"id": 0, "code": response[0], "status": int(response[1]), "type": 1}
        try:
            from . import client_socket
            if client_socket:
                #print(f"Status: {message}")
                payload = json.dumps(message).encode("utf-8") + b"\x00"
                client_socket.send(payload)
            else:
                print("CrowdControl: No active socket to send status response.")
        except Exception as e:
            print(f"CrowdControl: Failed to send status reponse: {e}")

    return None


@hook("WillowGame.WillowGameInfo:TeleportToFinalDestinationAfterLoad", Type.POST)
def CrowdControlLoadedMap(obj: UObject,args: WrappedStruct,ret: Any,func: BoundFunction,) -> Any:
    global effect_instances
    for inst in effect_instances:
        if inst.is_running:
            inst.on_map_change()
            inst.map_change_finalized()


@hook("WillowGame.WillowGameViewportClient:Tick", Type.PRE, hook_identifier="MainCCDrawHUDHook") #/Script/Engine.HUD:ReceiveDrawHUD
def CrowdControlDrawHUD(obj: UObject,args: WrappedStruct,ret: Any,func: BoundFunction,) -> Any:
    global effect_instances
    effects_to_remove: list = []
    for inst in effect_instances:
        if inst.is_running and inst.duration > 0:
            if (inst.start_time + inst.duration) <= time.time():
                #print("stopping timed effect")
                effects_to_remove.append(inst)
                inst.stop_effect()
    for e in effects_to_remove:
        effect_instances.remove(e)

@hook("Engine.PlayerController:SetLobbyShown", Type.POST)
def CheckInstalledDLCs(obj: UObject,args: WrappedStruct,ret: Any,func: BoundFunction) -> None:
    cm = ENGINE.GetDLCManager()
    AsterResult = cm.IsPackageFullyInstalled(cm.GetDownloadablePackageDefinitionFromDLCName("Aster"))
    print(f"Aster Installed: {AsterResult}")
    if not AsterResult: # disable the effects spawning stuff from dlcs that arent installed
        SetEffectStatus("spawn-enemy_warlordgrug", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_warlordslog", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_warlordturge", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_spiderpants", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_mrboneypantsguy", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_skeletonking", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_bluedragon", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_reddragon", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_greendragon", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_purpledragon", 0x83, get_pc())

    AnemoneResult = cm.IsPackageFullyInstalled(cm.GetDownloadablePackageDefinitionFromDLCName("Anemone"))
    print(f"Anemone Installed: {AnemoneResult}")
    if not AnemoneResult:
        SetEffectStatus("spawn-enemy_ltbolson", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_ltangvar", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_lthoffman", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_lttetra", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_hector", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_cassius", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_uranus", 0x83, get_pc())

    IrisResult = cm.IsPackageFullyInstalled(cm.GetDownloadablePackageDefinitionFromDLCName("Iris"))
    print(f"Iris Installed: {IrisResult}")
    if not IrisResult:
        SetEffectStatus("spawn-enemy_sullythestabber", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_blimp", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_motormama", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_piston", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_pyropete", 0x83, get_pc())

    OrchidResult = cm.IsPackageFullyInstalled(cm.GetDownloadablePackageDefinitionFromDLCName("Orchid"))
    print(f"Orchid Installed: {OrchidResult}")
    if not OrchidResult:
        SetEffectStatus("spawn-enemy_nobeard", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_roscoe", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_herle", 0x83, get_pc())

    FlaxResult = cm.IsPackageFullyInstalled(cm.GetDownloadablePackageDefinitionFromDLCName("Flax"))
    print(f"Flax Installed: {FlaxResult}")
    if not FlaxResult:
        SetEffectStatus("spawn-enemy_clark", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_sullytheblacksmith", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_pumpkinkingpin", 0x83, get_pc())
        SetEffectStatus("spawn_candy", 0x83, get_pc())
        SetEffectStatus("spawn_wisps", 0x83, get_pc())

    AlliumResult = cm.IsPackageFullyInstalled(cm.GetDownloadablePackageDefinitionFromDLCName("Allium"))
    print(f"Allium Installed: {AlliumResult}")
    if not AlliumResult:
        SetEffectStatus("spawn-enemy_tindersnowflake", 0x83, get_pc())

    LobeliaResult = cm.IsPackageFullyInstalled(cm.GetDownloadablePackageDefinitionFromDLCName("Lobelia"))
    print(f"Lobelia Installed: {LobeliaResult}")
    if not LobeliaResult:
        SetEffectStatus("spawn-enemy_omgwth", 0x83, get_pc())

    SageResult = cm.IsPackageFullyInstalled(cm.GetDownloadablePackageDefinitionFromDLCName("Sage"))
    print(f"Sage Installed: {SageResult}")
    if not SageResult:
        SetEffectStatus("spawn-enemy_arizona", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_bulstoss", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_rouge", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_dermonstrositat", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_rakkanoth", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_dribbles", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_bloodtail", 0x83, get_pc())
        SetEffectStatus("spawn-enemy_dexi", 0x83, get_pc())

    if not AsterResult or not IrisResult:
        SetEffectStatus("gamba_time", 0x83, get_pc())

    CheckInstalledDLCs.disable()

    return None


build_mod()