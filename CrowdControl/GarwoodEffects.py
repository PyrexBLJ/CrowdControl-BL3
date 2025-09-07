from .Effect import Effect
from typing import Any
from mods_base import ENGINE,get_pc
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct
from unrealsdk.hooks import Type, add_hook, remove_hook
import math
from unrealsdk import make_struct
from .Utils import SpawnInteractiveObject,AmIHost,SendToHost,Net,Circle,InFrontOfPlayer

class SuperHot(Effect):

    effect_name = "super_hot"
    display_name = "Super Hot"

    def run_effect(self):
        if AmIHost():
            add_hook("/Script/Engine.HUD:ReceiveDrawHUD", Type.PRE, "speed_change", self.speed_change)
        else:
            SendToHost(self)
        return super().run_effect()

    def speed_change(self, obj: UObject, args: WrappedStruct,ret: Any, func: BoundFunction) -> Any:
        if "MenuMap_P" not in str(ENGINE.GameViewport.World.Name):
            if "Vehicle" in str(self.pc.Pawn):
                if 1/720 * self.pc.Pawn.Speed <= 0.05:
                    ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 0.05
                else:
                    ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 1/720 * self.pc.Pawn.Speed
            else:
                if 1/720 * math.sqrt(self.pc.Pawn.GetVelocity().X**2 + self.pc.Pawn.GetVelocity().Y**2 + self.pc.Pawn.GetVelocity().Z**2) <= 0.05:
                    ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 0.05
                else:
                    ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 1/720 * math.sqrt(self.pc.Pawn.GetVelocity().X**2 + self.pc.Pawn.GetVelocity().Y**2 + self.pc.Pawn.GetVelocity().Z**2)

    def stop_effect(self):
        remove_hook("/Script/Engine.HUD:ReceiveDrawHUD", Type.PRE, "speed_change")
        ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 1
        return super().stop_effect()

class SizeSteal(Effect):

    effect_name = "size_steal"
    display_name = "Size Steal"

    def run_effect(self):
        global PlayerListSize
        if AmIHost():
            PlayerListSize = []
            for player in ENGINE.GameViewport.World.GameState.PlayerArray:
                PlayerListSize.append(player.Owner.Pawn.GetActorScale3D())
            add_hook("/Script/GbxGameSystemCore.DamageComponent:ReceiveAnyDamage", Type.PRE, "size_steal", self.size_steal)
        else:
            SendToHost(self)
        return super().run_effect()

    def size_steal(self, obj: UObject, args: WrappedStruct,ret: Any, func: BoundFunction) -> Any:
        obj.GetOwner().SetActorScale3D(make_struct("Vector" , X = obj.GetOwner().GetActorScale3D().X * (1/1.05), Y = obj.GetOwner().GetActorScale3D().Y * (1/1.05), Z = obj.GetOwner().GetActorScale3D().Z * (1/1.05)))
        args.DamageCauser.GetOwner().SetActorScale3D(make_struct("Vector" , X = args.DamageCauser.GetOwner().GetActorScale3D().X * 1.05, Y = args.DamageCauser.GetOwner().GetActorScale3D().Y * 1.05, Z = args.DamageCauser.GetOwner().GetActorScale3D().Z * 1.05))

    def stop_effect(self):
        global PlayerListSize
        I=0
        remove_hook("/Script/GbxGameSystemCore.DamageComponent:ReceiveAnyDamage", Type.PRE, "size_steal")
        for player in ENGINE.GameViewport.World.GameState.PlayerArray:
            player.Owner.Pawn.SetActorScale3D(PlayerListSize[I])
            I+=1
        return super().stop_effect()

class BarrelNet(Effect):

    effect_name = "barrel_net"
    display_name = "Barrel Net"

    def run_effect(self):
        if AmIHost():
            PCRot = self.pc.pawn.K2_GetActorRotation()
            PCLoc = Circle(self.pc.pawn.K2_GetActorLocation(),2,4,7,600,0,False)
            for net in PCLoc:
                actor = SpawnInteractiveObject(0,net,PCRot)
                actor.BPI_SetSimulatePhysics(False)
        else:
            SendToHost(self)
        return super().run_effect()

class VendorBox(Effect):

    effect_name = "vendor_box"
    display_name = "Vendor Box"

    def run_effect(self):
        if AmIHost():
            counter = 1
            PCLoc = Circle(self.pc.pawn.K2_GetActorLocation(),1,0,4,150,-75,False)
            for net in PCLoc:
                PCRot = make_struct("Rotator", Roll =0, Pitch=0, Yaw=90*counter + 180)
                SpawnInteractiveObject(counter,net,PCRot)
                counter += 1
        else:
            SendToHost(self)
        return super().run_effect()

class RedChest(Effect):

    effect_name = "red_chest"
    display_name = "Red Chest"

    def run_effect(self):
        if AmIHost():
            PCRot = make_struct("Rotator", Roll =0, Pitch=0, Yaw=self.pc.Pawn.K2_GetActorRotation().Yaw + 180)
            actor = SpawnInteractiveObject(5,make_struct("Vector", X=self.pc.Pawn.K2_GetActorLocation().X + (self.pc.GetActorForwardVector().X * 200), Y=self.pc.Pawn.K2_GetActorLocation().Y + (self.pc.GetActorForwardVector().Y * 200), Z=self.pc.Pawn.K2_GetActorLocation().Z - 100),PCRot)
        else:
            SendToHost(self)
        return super().run_effect()
