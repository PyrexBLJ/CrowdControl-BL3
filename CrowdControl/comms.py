import json
import threading
import time
from mods_base import get_pc


effects = set()
timed = set()
paused = set()

def getReponseType(status: str) -> int:
    statuses: list = ["Success", "Failure", "Unavailable", "Retry", "Queue", "Running", "Paused", "Resumed", "Finished"]
    try:
        return bytes(statuses.index(status))
    except ValueError:
        return bytes(1) # return a failure when status isnt known

def NotifyEffect(thread, eid, status=None, code=None, pc=None, timeRemaining=None):
    if pc != get_pc():
        pc.ClientMessage(f"{eid}-{code}-{status}", "CrowdControl", float(pc.PlayerState.PlayerID))
        return
    if status is None:
        status = "Success"
    if eid in effects:
        effects.remove(eid)
    
    message = {"id":eid, "status":status, "code":code}
    
    if timeRemaining is None:
        print(f"CrowdControl: Responding with {status} for effect with ID {eid}")
    else:
        print(f"CrowdControl: Responding with {status} with {timeRemaining} seconds remaining for effect with ID {eid}")
        if eid not in timed:
            timed.add(eid)
        message["timeRemaining"] = timeRemaining

    message["type"] = 0
        
    if status == "Finished":
        if eid in timed:
            timed.remove(eid)
        if eid in paused:
            paused.remove(eid)
    elif status == "Paused":
        if eid not in timed:
            timed.add(eid)
        if eid not in paused:
            paused.add(eid)
    try:
        #print("trying response")
        if thread.socket:
            #print(f"responding from thread {thread} on socket {thread.socket}")
            #print(message)
            print(json.dumps(message).encode('utf-8')+b'\x00')
            #print(str(json.dumps(message).encode('utf-8')+b'\x00'))
            thread.socket.send(json.dumps(message).encode('utf-8')+b'\x00')
    except ConnectionAbortedError:
        print("ConnectionAbortedError")
        pass


def RequestEffect(thread, eid, effect_name, pc, *args):
    
    spawnloot_args = []
    if 'spawnloot' in effect_name:
        split_name = effect_name.split("_")
        spawnloot_args.append(split_name[1])
        spawnloot_args.append(split_name[2])
        effect_name = 'spawnloot'
        
    print(f"CrowdControl: Requesting effect {effect_name} with ID {eid}")
    from .Effect import Effect
    effect_cls = Effect.registry.get(effect_name)
    if not effect_cls:
        print(f"CrowdControl: Effect {effect_name} not found.")
        NotifyEffect(thread, eid, "Unavailable", effect_name)
        return
    
    effect_cls.id = eid
    effect_cls.args = list(args)
    effect_cls.thread = thread
    effect_cls.pc = pc

    for arg in spawnloot_args:
        effect_cls.args.append(arg)

    try:
        effect_cls.duration = int(args[0]) if args else 0
    except ValueError:
        effect_cls.duration = 0

    effects.add(eid)

    effect_cls.run_effect()

    if effect_cls.duration > 0:
        NotifyEffect(thread, eid, "Started", effect_name, pc, (effect_cls.duration * 1000))
        effect_cls.start_time = time.time()
        #threading.Timer(effect_cls.duration, effect_cls.stop_effect).start()
    else:
        NotifyEffect(thread, eid, "Finished", effect_name, pc)