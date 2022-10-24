"""
辅助功能
"""

import logging


class CaptchaError(Exception):
    """用户可能需要验证"""


class EmptyError(Exception):
    """没有数据"""


logger = logging.getLogger("TreeHole")
"""日志记录器"""
