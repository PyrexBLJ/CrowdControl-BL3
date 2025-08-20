import socket
import time
import threading
import json
import unrealsdk
from mods_base import build_mod
from .comms import RequestEffect, NotifyEffect
from .Effect import *

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
                                RequestEffect(thread, eid, effect, duration, *parameters)
                            elif parameters:
                                RequestEffect(thread, eid, effect, *parameters)
                            elif duration:
                                RequestEffect(thread, eid, effect, duration)
                            else:
                                RequestEffect(thread, eid, effect)
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

build_mod(on_enable=Enable, on_disable=Disable)