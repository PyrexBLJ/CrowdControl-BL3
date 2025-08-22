import socket
import time
import threading
import json
import unrealsdk
from mods_base import build_mod, hook
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct
from unrealsdk.hooks import Type
from typing import Any
import random
from .comms import RequestEffect, NotifyEffect
from .Utils import AmIHost
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

shutdown = False

thread = None
class AppSocketThread(threading.Thread):
    #repurposed from:
    # - https://stackoverflow.com/questions/27284358/connect-to-socket-on-localhost
    # - https://stackoverflow.com/questions/51677868/parse-json-message-from-socket-using-python
    host = "127.0.0.1"
    port = 42069
    socket = None

    def __init__(self, name='cc-app-socket-thread'):
        global thread
        super(self.__class__, self).__init__(name=name)
        thread = self
        self.start()

    def run(self):
        global thread, shutdown
        print("CrowdControl: Socket Thread Running!")
        while True:
            if shutdown:
                shutdown = False
                break
            #print(f"CrowdControl: Attempting to connect on {self.host}:{self.port}")
            do_reset = False
            try:
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((self.host,self.port))
                print(f"CrowdControl: Connected on {self.host}:{self.port}")
                do_reset = True
                self.socket = s
                buffer = ''
                while True:
                    if shutdown:
                        shutdown = False
                        break
                    chunk = s.recv(1024)
                    if not chunk:
                        continue
                    buffer += chunk.decode('utf-8')
                    atoms = buffer.split(u'\x00')
                    if len(atoms) > 1:
                        buffer = atoms.pop()
                        for atom in atoms:
                            message = json.loads(atom)
                            print(message)
                            eid = message["id"]
                            #if Shared is None:
                                #print(f"CrowdControl: Need to be loaded into a save to run effects!")
                                #NotifyEffect(eid, "NotReady")
                                #continue
                            effect = message["code"]
                            duration = message.get("duration",None)
                            parameters = message.get("parameters",None)
                            if duration:
                                duration /= 1000
                            if duration and parameters:
                                RequestEffect(thread, eid, effect, get_pc(), duration, *parameters)
                            elif parameters:
                                RequestEffect(thread, eid, effect, get_pc(), *parameters)
                            elif duration:
                                RequestEffect(thread, eid, effect, get_pc(), duration)
                            else:
                                RequestEffect(thread, eid, effect, get_pc())
            except ConnectionResetError:
                print("Connection Reset")
                pass
            except ConnectionRefusedError:
                print("Connection Refused")
                time.sleep(5)
                pass
            except ConnectionAbortedError:
                print("Connection Aborted")
                pass
            finally:
                if do_reset and Shared is not None:
                    #Scribe.Send("CrowdControl: Reset")
                    print("resetting connection")
                    do_reset = False
                time.sleep(5)
                continue

    def shutdown(self):
        self.socket.close()


def Enable() -> None:
    global client
    client = AppSocketThread()
    return None

def Disable() -> None:
    global client, shutdown
    shutdown = True
    if client != None:
        client.shutdown()
        client = None
    return None

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
    global thread
    if "CrowdControl" in args.S:
        request: list = args.S.split("-")

        if str(get_pc().PlayerState.PlayerID) == request[1]:
            #print("Got a client request from ourself, this really shouldnt happen.")
            return None
        
        if request[4] != "None": # request[4] are the args
            RequestEffect(thread, request[3], request[2], obj, request[4])
        else:
            RequestEffect(thread, request[3], request[2], obj)

        #if request[2] == "example_effect":
            # do the effect stuff

            #now we have to tell the client what we did, obj will be the clients player controller
            #obj.ClientMessage(f"{request[3]}-{request[2]}-(Status)", "CrowdControl", float(request[1]))


    return None

@hook("/Script/Engine.PlayerController:ClientMessage", Type.PRE)
def ClientMessageHook(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction) -> None:
#
#   This is where players will get responses from the host
#
#   As im writing this i dont think we will really much more than this, def will have to handle timed events somehow but im not sure yet
#
    global thread
    if args.type == "CrowdControl":
        if args.MsgLifeTime != float(get_pc().PlayerState.PlayerID) or AmIHost():
            return None
        
        response: list = args.S.split("-")

        NotifyEffect(thread, response[0], response[2], response[1]) #ngl idk the best way to deal with timeremaining yet

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


build_mod(on_enable=Enable, on_disable=Disable)