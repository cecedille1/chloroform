# -*- coding: utf-8 -*-

import logging

from robot.output.logger import LOGGER
from robot.output.loggerhelper import Message


MAP = {
    'WARNING': 'WARN',
}


class RobotRelayHandler(logging.Handler):
    def emit(self, record):
        message = self.format(record)
        level = MAP.get(record.levelname, record.levelname)
        LOGGER.log_message(Message(message, level, False))
