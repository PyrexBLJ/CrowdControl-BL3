from mods_base import get_pc, ENGINE #type: ignore
from unrealsdk.unreal import UObject #type: ignore
import json
import time
import socket
from copy import deepcopy

effects = set()
timed = set()
paused = set()
effect_instances = set()


def SetEffectStatus(code, status, pc:UObject):
    if pc.PlayerState == ENGINE.GameViewport.World.GameState.HostPlayerState:
        message = {"id": 0, "code": code, "status": status, "type": 1}
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
    else:
        pc.ClientMessage(f"{code}-{status}", "CCEffectStatus", float(pc.PlayerState.PlayerID))
    return


def NotifyEffect(eid, status=None, code=None, pc=None, timeRemaining=None):

    if pc != get_pc():
        pc.ClientMessage(f"{eid}-{status}-{code}", "CrowdControl", float(pc.PlayerState.PlayerID))
        return

    if status is None:
        status = "Success"

    if eid in effects:
        effects.remove(eid)

    message = {"id": eid, "status": status, "code": code, "type": 0}

    if timeRemaining is not None:
        #print(f"CrowdControl: Responding with {status} with {timeRemaining} seconds remaining for effect with ID {eid}")
        #message["timeRemaining"] = timeRemaining
        timed.add(eid)
    #else:
        #print(f"CrowdControl: Responding with {status} for effect with ID {eid}")

    if status == "Finished":
        timed.discard(eid)
        paused.discard(eid)
    elif status == "Paused":
        timed.add(eid)
        paused.add(eid)

    try:
        from . import client_socket
        if client_socket:
            #print(f"Response: {message}")
            payload = json.dumps(message).encode("utf-8") + b"\x00"
            client_socket.send(payload)
        else:
            print("CrowdControl: No active socket to send response.")
    except Exception as e:
        print(f"CrowdControl: Failed to send response: {e}")


def RequestEffect(eid, effect_name, pc, viewer, viewers, source, *args):
    extra_args = []
    
    if "spawnloot" in effect_name:
        split_name = effect_name.split("_")
        extra_args.extend(split_name[1:3])
        effect_name = "spawnloot"
    
    if "spawnenemy" in effect_name:
        split_name = effect_name.split("_")
        extra_args.extend(split_name[1:3])
        effect_name = "spawnenemy"

    if "givecurrency" in effect_name:
        split_name = effect_name.split("_")
        extra_args.extend(split_name[1:3])
        effect_name = "givecurrency"
    
    if "csbooster" in effect_name:
        split_name = effect_name.split("_")
        extra_args.extend(split_name[1:2])
        effect_name = "csbooster"

    effect_cls = None
    #print(f"CrowdControl: Requesting effect {effect_name} with ID {eid} and args viewer: {viewer}, viewers: {viewers}, source: {source}")
    from .Effect import Effect
    for c in Effect.registry.values():
        if c.effect_name == effect_name:
            effect_cls = deepcopy(c)
    #effect_cls = Effect.registry.get(effect_name).__new__()

    if not effect_cls:
        print(f"CrowdControl: Effect {effect_name} not found.")
        NotifyEffect(eid, "Unavailable", effect_name, pc)
        return

    effect_cls.id = eid
    effect_cls.args = list(args) + extra_args
    effect_cls.pc = pc
    effect_cls.viewer = viewer
    effect_cls.viewers = viewers
    effect_cls.sourcedetails = source

    try:
        effect_cls.duration = int(args[0]) if args else 0
    except Exception:
        effect_cls.duration = 0

    effect_instances.add(effect_cls)
    effects.add(eid)
    effect_cls.run_effect()

    if effect_cls.duration > 0:
        effect_cls.start_time = time.time()