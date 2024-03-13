"""
Robot 2024 — Robot code for the 2023-2024 FRC season.
Copyright (C) 2024  Hangar 84
"""

from commands2 import Subsystem
from phoenix5 import WPI_TalonSRX, WPI_VictorSPX
from wpilib import MotorControllerGroup
from wpilib.drive import DifferentialDrive


class DriveSubsystem(Subsystem):
    """
    Subsystem for controlling the robot's drive base.
    """

    def __init__(self):
        super().__init__()

        self.left_motors = MotorControllerGroup(WPI_TalonSRX(0), WPI_VictorSPX(0))
        self.right_motors = MotorControllerGroup(WPI_TalonSRX(1), WPI_VictorSPX(1))

        self.differential_drive = DifferentialDrive(self.left_motors, self.right_motors)

        self.right_motors.setInverted(True)

    def arcade_drive(self, x_speed: float, z_rotation: float) -> None:
        """
        Wrapper around `DifferentialDrive.arcadeDrive` to allow for drift correction.

        :param x_speed: The speed of the robot in the x direction (forward).
        :param z_rotation: The rotation of the robot around the z-axis.
        :return:
        """
        if abs(z_rotation) < 0.1:
            if x_speed < 0:
                z_rotation = 0.175
            elif x_speed > 0:
                z_rotation = -0.175

        self.differential_drive.arcadeDrive(x_speed, z_rotation)
