"""
辅助功能
"""

import logging


class EmptyError(Exception):
    """没有数据"""


class AuthError(Exception):
    """认证错误"""


logger = logging.getLogger("TreeHole")
"""日志记录器"""
