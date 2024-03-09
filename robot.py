"""
Robot 2024 — Robot code for the 2023-2024 FRC season.
Copyright (C) 2024  Hangar 84

Xbox Controller Mapping:
- Right Stick: Drive (Arcade Drive)
- Left Trigger: Launcher (Intake)
- Right Trigger: Launcher (Outtake)

Joystick Mapping:
- Main Stick: Drive (Arcade Drive)
- TODO: Add joystick control for the launcher.
"""
from commands2.button import CommandXboxController, CommandJoystick
from magicbot import MagicRobot
from phoenix5 import WPI_TalonSRX, WPI_VictorSPX
# NOTE: `rev` comes from `robotpy`'s `rev` extra. The following inspection is a false positive.
# noinspection PyPackageRequirements
from rev import CANSparkMax, CANSparkLowLevel
from wpilib import MotorControllerGroup
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

        self.launcher_motors = MotorControllerGroup(
            CANSparkMax(1, CANSparkLowLevel.MotorType.kBrushed),
            CANSparkMax(2, CANSparkLowLevel.MotorType.kBrushed),
        )

        self.controller = CommandXboxController(0)

        self.right_motors.setInverted(True)

    def teleopPeriodic(self) -> None:
        match self.controller:
            case CommandXboxController():
                x_speed = self.controller.getRightY()
                z_rotation = self.controller.getRightX()

                launcher_speed = -self.controller.getLeftY() + self.controller.getRightY()

            case CommandJoystick():
                x_speed = self.controller.getY()
                z_rotation = self.controller.getX()

                raise NotImplemented("Joystick control of the launcher is not yet implemented!")

            case None:
                raise ValueError("Controller was not initialized!")

            case _:
                raise ValueError("Invalid controller type!")

        self.drive.arcadeDrive(x_speed, z_rotation)
        self.launcher_motors.set(launcher_speed)
