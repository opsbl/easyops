# -*- coding: utf-8 -*-
#

"""
@Project: easyops
@File:    common
@Author:  boli
@Data:    2022/12/8 10:59
@Describe: 
    Common variables
"""

import logging

logging.debug("Initialize the logger...")

logger = logging.getLogger("easyops")

logging.debug("logger.propagate = True")

logger.propagate = True

log_default_level = logging.WARNING


def set_debug(on):
    if on:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(log_default_level)
