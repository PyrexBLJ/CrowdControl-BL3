import socket
import time
import select
import json
from mods_base import build_mod, hook #type: ignore
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct #type: ignore
from unrealsdk.hooks import Type #type: ignore
from typing import Any
from .Utils import AmIHost, CrowdControl_PawnList_Possessed, CrowdControl_PawnList_Unpossessed
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


def connect_socket(host, port):
    global client_socket, do_reset, connecting
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(False)
        s.connect_ex((host, port))
        client_socket = s
        connecting = True
        do_reset = True
        print(f"CrowdControl: Connecting to {host}:{port}... (leaking this ip is fine you can relax)")
    except Exception as e:
        print(f"CrowdControl: Connection failed: {e}")
        client_socket = None
        connecting = False


@hook("/Script/Engine.HUD:ReceiveDrawHUD", Type.PRE)
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
                    eid = message["id"]
                    effect = message["code"]
                    viewer = message.get("viewer", "None")
                    viewers = message.get("viewers", None)
                    sourcedetails = message.get("sourceDetails", None)
                    duration = message.get("duration", None)
                    parameters = message.get("parameters", None)

                    if duration:
                        duration /= 1000

                    if duration and parameters:
                        RequestEffect(eid, effect, get_pc(), viewer, viewers, sourcedetails, duration, *parameters)
                    elif parameters:
                        RequestEffect(eid, effect, get_pc(), viewer, viewers, sourcedetails, *parameters)
                    elif duration:
                        RequestEffect(eid, effect, get_pc(), viewer, viewers, sourcedetails, duration)
                    else:
                        RequestEffect(eid, effect, get_pc(), viewer, viewers, sourcedetails)

    except Exception as e:
        print(f"CrowdControl Socket Error: {e}")
        if client_socket:
            client_socket.close()
        client_socket = None
        connecting = False






@hook("/Script/Engine.PlayerController:ServerChangeName", Type.PRE)
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
    if "CrowdControl-" in args.S:
        trimmedrequest: str = args.S
        trimmedrequest = trimmedrequest.removeprefix("CrowdControl-")
        b64request: list = trimmedrequest.split("-")
        request = json.loads(base64.b64decode(b64request[1]).decode("utf-8"))
        request["pc"] = obj
        request["from_client"] = True

        if str(get_pc().PlayerState.PlayerID) == str(obj.PlayerState.PlayerID):
            #print("Got a client request from ourself, discard it.")
            return None
        
        eid = request["id"]
        effect = b64request[0]
        viewer = request.get("viewer", "None")
        viewers = request.get("viewers", None)
        sourcedetails = request.get("sourceDetails", None)
        duration = request.get("duration", None)
        parameters = request.get("args", None)

        if duration:
            duration /= 1000

        if duration and parameters:
            RequestEffect(eid, effect, request["pc"], viewer, viewers, sourcedetails, duration, *parameters)
        elif parameters:
            RequestEffect(eid, effect, request["pc"], viewer, viewers, sourcedetails, *parameters)
        elif duration:
            RequestEffect(eid, effect, request["pc"], viewer, viewers, sourcedetails, duration)
        else:
            RequestEffect(eid, effect, request["pc"], viewer, viewers, sourcedetails)

    return None

@hook("/Script/Engine.PlayerController:ClientMessage", Type.PRE)
def ClientMessageHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
#
#   This is where players will get responses from the host
#
#   As im writing this i dont think we will really much more than this, def will have to handle timed events somehow but im not sure yet
#
    if args.type == "CrowdControl":
        if args.MsgLifeTime != float(get_pc().PlayerState.PlayerID) or AmIHost():
            return None
        
        response: list = args.S.split("-")

        NotifyEffect(response[0], response[2], response[1]) #ngl idk the best way to deal with timeremaining yet

    return None


@hook("/Script/Engine.PlayerController:ServerNotifyLoadedWorld", Type.POST)
def CrowdControlLoadedMap(obj: UObject,args: WrappedStruct,ret: Any,func: BoundFunction,) -> Any:
    NewMap = str(args.WorldPackageName)
    if "loader" in NewMap.lower() or "fakeentry" in NewMap.lower():
        return
    
    for inst in Effect.registry.values():
        if inst.is_running:
            inst.on_map_change()

    CrowdControlFinishedDim.enable()


@hook("/Script/OakGame.GFxExperienceBar:extFinishedDim", Type.POST)
def CrowdControlFinishedDim(obj: UObject,args: WrappedStruct,ret: Any,func: BoundFunction,) -> Any:
    for inst in Effect.registry.values():
        if inst.is_running:
            inst.map_change_finalized()
    CrowdControlFinishedDim.disable()


@hook("/Script/Engine.HUD:ReceiveDrawHUD", Type.PRE)
def CrowdControlDrawHUD(obj: UObject,args: WrappedStruct,ret: Any,func: BoundFunction,) -> Any:
    for inst in Effect.registry.values():
        if inst.is_running and inst.duration > 0:
            if (inst.start_time + inst.duration) <= time.time():
                inst.stop_effect()


build_mod()