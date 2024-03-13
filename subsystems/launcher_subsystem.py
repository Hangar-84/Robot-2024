"""
Robot 2024 — Robot code for the 2023-2024 FRC season.
Copyright (C) 2024  Hangar 84
"""

from commands2 import Subsystem
from rev import CANSparkMax, CANSparkLowLevel
from wpilib import MotorControllerGroup


class LauncherSubsystem(Subsystem):
    # TODO: Add `launch` and `intake` commands for use with autonomous.
    def __init__(self):
        super().__init__()

        self.launcher_motors = MotorControllerGroup(
            CANSparkMax(1, CANSparkLowLevel.MotorType.kBrushed),
            CANSparkMax(2, CANSparkLowLevel.MotorType.kBrushed),
        )
