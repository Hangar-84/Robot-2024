"""
Robot 2024 — Robot code for the 2023-2024 FRC season.
Copyright (C) 2024  Hangar 84
"""
from magicbot import MagicRobot
from phoenix5 import WPI_TalonSRX, WPI_VictorSPX
from wpilib import MotorControllerGroup, XboxController, Joystick
from wpilib.drive import DifferentialDrive


class Robot(MagicRobot):
    left_motors: MotorControllerGroup
    right_motors: MotorControllerGroup
    drive: DifferentialDrive
    controller: XboxController | Joystick

    def createObjects(self) -> None:
        self.left_motors = MotorControllerGroup(WPI_TalonSRX(0), WPI_VictorSPX(0))
        self.right_motors = MotorControllerGroup(WPI_TalonSRX(1), WPI_VictorSPX(1))
        self.drive = DifferentialDrive(self.left_motors, self.right_motors)

        self.controller = XboxController(0)

        self.right_motors.setInverted(True)

    def teleopPeriodic(self) -> None:
        match self.controller:
            case XboxController():
                x_speed = self.controller.getRightY()
                y_speed = self.controller.getRightX()

            case Joystick():
                x_speed = self.controller.getY()
                y_speed = self.controller.getX()

            case None:
                raise ValueError("Controller was not initialized!")

            case _:
                raise ValueError("Invalid controller type!")

        self.drive.arcadeDrive(x_speed, y_speed)
