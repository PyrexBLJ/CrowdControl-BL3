from .Effect import Effect
from typing import Any
from mods_base import ENGINE,get_pc
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct
from unrealsdk.hooks import Type, add_hook, remove_hook
import math
import random
from unrealsdk import make_struct
from .Utils import AmIHost,SendToHost,Net,Circle,InFrontOfPlayer,GetPlayerCharacter, SpawnIO
from .InteractiveObjectLists import InteractiveObjects


class SuperHot(Effect):
    effect_name = "super_hot"
    display_name = "Super Hot"

    def speed_change(self, obj: UObject, args: WrappedStruct,ret: Any, func: BoundFunction) -> None:
        if str(ENGINE.GetCurrentWorldInfo().GetStreamingPersistentMapName().lower()) not in ["menumap", "loader", "exampleentry"]:
            if "Vehicle" not in str(self.pc.Pawn):
                if 1/720 * self.pc.Pawn.CurrentPawnSpeed <= 0.05:
                    ENGINE.GetCurrentWorldInfo().TimeDilation = 0.05
                else:
                    ENGINE.GetCurrentWorldInfo().TimeDilation = 1/720 * self.pc.Pawn.CurrentPawnSpeed
            else:
                if 1/720 * math.sqrt(self.pc.Pawn.Velocity.X**2 + self.pc.Pawn.Velocity.Y**2 + self.pc.Pawn.Velocity.Z**2) <= 0.05:
                    ENGINE.GetCurrentWorldInfo().TimeDilation = 0.05
                else:
                    ENGINE.GetCurrentWorldInfo().TimeDilation = 1/720 * math.sqrt(self.pc.Pawn.Velocity.X**2 + self.pc.Pawn.Velocity.Y**2 + self.pc.Pawn.Velocity.Z**2)
    
    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            add_hook("WillowGame.WillowGameViewportClient:Tick", Type.POST, "speed_change", self.speed_change)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
    def stop_effect(self, response = "Finished", respond = True):
        remove_hook("WillowGame.WillowGameViewportClient:Tick", Type.POST, "speed_change")
        ENGINE.GetCurrentWorldInfo().TimeDilation = 1
        return super().stop_effect(response, respond)
    
class RedChest(Effect):
    effect_name = "red_chest"
    display_name = "Red Chest"

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            rot = abs(GetPlayerCharacter(self.pc).Controller.Rotation.Yaw % 65535) + 16383
            if rot > 65535:
                rot -= 65535
            PCRot = make_struct("Rotator", Pitch=0, Yaw=rot, Roll=0)
            PCLoc = InFrontOfPlayer(self.pc)
            PCLoc.Z -= 75
            SpawnIO("redchest", 1, self.pc, PCLoc, PCRot)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)

class VendorBox(Effect):
    effect_name = "vendor_box"
    display_name = "Vendor Box, hope you know how to nade jump."

    vendors = ["weaponvendor", "ammovendor", "weaponvendor", "healthvendor"]

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            counter = 0
            PCLoc = Circle(self.pc.Pawn.Location, 1, 0, 4, 90, -75, False)
            for net in PCLoc:
                yaw = 16383*counter + 49149
                if yaw > 65535:
                    yaw -= 65535
                PCRot = make_struct("Rotator", Pitch = 0, Yaw= yaw, Roll= 0)
                SpawnIO(self.vendors[counter], 1, self.pc, net, PCRot)
                counter += 1
        else:
            SendToHost(self)
        return super().run_effect(response, respond)
    
class BarrelNet(Effect):
    effect_name = "barrel_net"
    display_name = "Barrel Net"

    barrels = ["slagbarrel", "corrosivebarrel", "explosivebarrel", "shockbarrel", "firebarrel"]

    def run_effect(self, response = "Success", respond = True):
        if AmIHost():
            PCRot = GetPlayerCharacter(self.pc).Controller.Rotation
            PCLoc = Circle(GetPlayerCharacter(self.pc).Location, 2, 4, 7, 500, 0, False)
            for net in PCLoc:
                SpawnIO(random.choice(self.barrels), 1, self.pc, net, PCRot)
        else:
            SendToHost(self)
        return super().run_effect(response, respond)