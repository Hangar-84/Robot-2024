"""
Robot 2024 — Robot code for the 2023-2024 FRC season.
Copyright (C) 2024  Hangar 84
"""

from dataclasses import dataclass

from commands2 import (
    Command,
    InstantCommand,
    cmd,
    WaitCommand,
    SequentialCommandGroup,
    Command,
    ParallelRaceGroup,
    RepeatCommand,
)
from commands2.button import CommandXboxController

from subsystems.drive_subsystem import DriveSubsystem
from subsystems.launcher_subsystem import LauncherSubsystem


@dataclass
class Subsystems:
    """Dataclass containing all robot subsystems."""

    drive: DriveSubsystem = DriveSubsystem()
    launcher: LauncherSubsystem = LauncherSubsystem()


class RobotContainer:
    """
    Container for the majority of robot logic.
    This class is responsible for connecting subsystems, commands, and/or buttons and autonomous routines.
    """

    def __init__(self):
        self.controller = CommandXboxController(0)

        self.subsystems = Subsystems()

        self.bind_controls()

    def bind_controls(self) -> None:
        """
        Initialize commands related to the robot's controls.

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
                ),
                self.subsystems.drive,
            )
        )

        self.subsystems.launcher.setDefaultCommand(
            cmd.run(
                lambda: self.subsystems.launcher.launcher_motors.set(
                    -self.controller.getLeftTriggerAxis()
                    + self.controller.getRightTriggerAxis()
                ),
                self.subsystems.launcher,
            )
        )

    @property
    def auto_command(self) -> Command:
        """
        Returns the autonomous command to be scheduled when autonomous starts.

        :return: The command to be scheduled.
        """
        # TODO: Add autonomous mode selector to the dashboard.
        return (
            cmd.run(
                lambda: self.subsystems.drive.arcade_drive(0.5, 0.0),
                self.subsystems.drive,
            )
            .withTimeout(2.0)
            .andThen(
                InstantCommand(
                    lambda: self.subsystems.drive.differential_drive.stopMotor(),
                    self.subsystems.drive,
                )
            )
        )
