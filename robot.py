"""
Robot 2024 — Robot code for the 2023-2024 FRC season.
Copyright (C) 2024  Hangar 84
"""
from commands2 import TimedCommandRobot, CommandScheduler

from robot_container import RobotContainer


class Robot(TimedCommandRobot):
    container: RobotContainer
    command_scheduler: CommandScheduler

    def robotInit(self):
        self.container = RobotContainer()
        self.command_scheduler = CommandScheduler.getInstance()

    def teleopInit(self):
        self.container.auto_command.cancel()

    def teleopPeriodic(self) -> None:
        pass

    def autonomousInit(self) -> None:
        self.container.auto_command.schedule()

    def testInit(self):
        self.command_scheduler.cancelAll()
