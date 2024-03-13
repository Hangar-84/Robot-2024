"""
Robot 2024 — Robot code for the 2023-2024 FRC season.
Copyright (C) 2024  Hangar 84
"""

from dataclasses import dataclass

from commands2 import Command, InstantCommand, cmd
from commands2.button import CommandXboxController

from subsystems.drive_subsystem import DriveSubsystem
from subsystems.launcher_subsystem import LauncherSubsystem


@dataclass
class Subsystems:
    drive: DriveSubsystem = DriveSubsystem()
    launcher: LauncherSubsystem = LauncherSubsystem()


class RobotContainer:
    def __init__(self):
        self.controller = CommandXboxController(0)

        self.subsystems = Subsystems()

    def bind_controls(self) -> None:
        """
        Xbox Controller Mapping:
        - Left Stick: Drive (X-Speed, Arcade Drive)
        - Right Stick: Drive (Z-Rotation, Arcade Drive)
        - Left Trigger: Launcher (Intake)
        - Right Trigger: Launcher (Outtake)

        TODO: Add joystick controls.
        :return:
        """
        self.subsystems.drive.setDefaultCommand(
            cmd.run(
                lambda: self.subsystems.drive.arcade_drive(
                    self.controller.getLeftY(), self.controller.getRightX()
                )
            )
        )

        self.subsystems.launcher.setDefaultCommand(
            cmd.run(
                lambda: self.subsystems.launcher.launcher_motors.set(
                    -self.controller.getLeftTriggerAxis()
                    + self.controller.getRightTriggerAxis()
                )
            )
        )

    @property
    def auto_command(self) -> Command:
        # TODO: Add autonomous mode selector to the dashboard.
        return InstantCommand()
