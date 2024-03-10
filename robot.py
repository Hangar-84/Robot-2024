"""
Robot 2024 — Robot code for the 2023-2024 FRC season.
Copyright (C) 2024  Hangar 84

Xbox Controller Mapping:
- Left Stick: Drive (X-Speed, Arcade Drive)
- Right Stick: Drive (Z-Rotation, Arcade Drive)
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

        self.left_motors.setInverted(True)
        self.launcher_motors.setInverted(True)

    def teleopPeriodic(self) -> None:
        match self.controller:
            case CommandXboxController():
                x_speed = self.controller.getLeftY()
                z_rotation = self.controller.getRightX()

                launcher_speed = -self.controller.getLeftTriggerAxis() + self.controller.getRightTriggerAxis()

            case CommandJoystick():
                x_speed = self.controller.getY()
                z_rotation = self.controller.getX()

                raise NotImplemented("Joystick control of the launcher is not yet implemented!")

            case None:
                raise ValueError("Controller was not initialized!")

            case _:
                raise ValueError("Invalid controller type!")

        # Apply a manual correction to drift due to lack of friction on left wheels when going straight forward/backward
        # TODO: Reduce the correction at slower speeds
        if abs(z_rotation) < 0.1:
            if x_speed > 0:
                z_rotation = 0.175
            elif x_speed < 0:
                z_rotation = -0.175

        self.drive.arcadeDrive(x_speed, -z_rotation)
        self.launcher_motors.set(launcher_speed)
