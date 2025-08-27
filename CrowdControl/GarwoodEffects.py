from .Effect import Effect
from typing import Any
from mods_base import ENGINE,get_pc
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct
from unrealsdk.hooks import Type, add_hook, remove_hook
import math

class SuperHot(Effect):

    effect_name = "super_hot"
    display_name = "Super Hot"

    def run_effect(self):
        add_hook("/Script/Engine.HUD:ReceiveDrawHUD", Type.PRE, "speed_change", self.speed_change)
        return super().run_effect()

    def speed_change(self, obj: UObject, args: WrappedStruct,ret: Any, func: BoundFunction) -> Any:
        if "MenuMap_P" not in str(ENGINE.GameViewport.World.Name):
            if "Vehicle" in str(self.pc.Pawn):
                if 1/720 * round(self.pc.Pawn.Speed) <= 0.05:
                    ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 0.05
                else:
                    ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 1/720 * round(self.pc.Pawn.Speed)
            else:
                if 1/720 * round(math.sqrt(self.pc.Pawn.GetVelocity().X**2 + self.pc.Pawn.GetVelocity().Y**2 + self.pc.Pawn.GetVelocity().Z**2)) <= 0.05:
                    ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 0.05
                else:
                    ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 1/720 * round(math.sqrt(self.pc.Pawn.GetVelocity().X**2 + self.pc.Pawn.GetVelocity().Y**2 + self.pc.Pawn.GetVelocity().Z**2))

    def stop_effect(self):
        remove_hook("/Script/Engine.HUD:ReceiveDrawHUD", Type.PRE, "speed_change")
        ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = 1
        return super().stop_effect()

class SizeSteal(Effect):

    effect_name = "size_steal"
    display_name = "Size Steal"

    def run_effect(self):
        add_hook("/Script/GbxGameSystemCore.DamageComponent:ReceiveAnyDamage", Type.PRE, "size_steal", self.size_steal)
        return super().run_effect()

    def size_steal(self, obj: UObject, args: WrappedStruct,ret: Any, func: BoundFunction) -> Any:
        obj.GetOwner().SetActorScale3D(unrealsdk.make_struct("Vector" , X = obj.GetOwner().GetActorScale3D().X * (1/1.05), Y = obj.GetOwner().GetActorScale3D().Y * (1/1.05), Z = obj.GetOwner().GetActorScale3D().Z * (1/1.05)))
        args.DamageCauser.GetOwner().SetActorScale3D(unrealsdk.make_struct("Vector" , X = args.DamageCauser.GetOwner().GetActorScale3D().X * 1.05, Y = args.DamageCauser.GetOwner().GetActorScale3D().Y * 1.05, Z = args.DamageCauser.GetOwner().GetActorScale3D().Z * 1.05))

    def stop_effect(self):
        remove_hook("/Script/GbxGameSystemCore.DamageComponent:ReceiveAnyDamage", Type.PRE, "size_steal")
        return super().stop_effect()