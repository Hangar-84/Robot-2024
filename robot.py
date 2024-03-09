"""
Robot 2024 — Robot code for the 2023-2024 FRC season.
Copyright (C) 2024  Hangar 84
"""
from commands2.button import CommandXboxController, CommandJoystick
from magicbot import MagicRobot
from phoenix5 import WPI_TalonSRX, WPI_VictorSPX
from wpilib import MotorControllerGroup, XboxController
from wpilib.drive import DifferentialDrive


class Robot(MagicRobot):
    def __init__(self):
        super().__init__()

        self.left_motors: MotorControllerGroup | None = None
        self.right_motors: MotorControllerGroup | None = None
        self.drive: DifferentialDrive | None = None

        self.launcher_motors: MotorControllerGroup | None = None

        self.controller: CommandXboxController | CommandJoystick | None = None

    def createObjects(self) -> None:
        self.left_motors = MotorControllerGroup(WPI_TalonSRX(0), WPI_VictorSPX(0))
        self.right_motors = MotorControllerGroup(WPI_TalonSRX(1), WPI_VictorSPX(1))
        self.drive = DifferentialDrive(self.left_motors, self.right_motors)

        self.controller = XboxController(0)

        self.right_motors.setInverted(True)

    def teleopPeriodic(self) -> None:
        match self.controller:
            case CommandXboxController():
                x_speed = self.controller.getRightY()
                z_rotation = self.controller.getRightX()

            case CommandJoystick():
                x_speed = self.controller.getY()
                z_rotation = self.controller.getX()

            case None:
                raise ValueError("Controller was not initialized!")

            case _:
                raise ValueError("Invalid controller type!")

        self.drive.arcadeDrive(x_speed, z_rotation)
