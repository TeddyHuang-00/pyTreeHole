"""
树洞相关数据模型
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, TypeVar, Union

__all__ = ("Hole", "ListHole", "AttentionHole", "Comment", "GenericHole", "UserName")


@dataclass(init=True, repr=False, order=False, unsafe_hash=True, frozen=False)
class Hole:
    """
    树洞基本数据模型
    """

    pid: Optional[int] = None
    """树洞 ID"""
    timestamp: Optional[int] = None
    """树洞创建时间戳"""
    type: Optional[str] = None
    """树洞类型（目前已知仅有：`text` 和 `image` 两种类型）"""
    text: Optional[str] = None
    """树洞文本内容"""
    url: Optional[str] = None
    """树洞图片链接（仅当 `type` 为 `image` 时非空）"""

    reply: Optional[int] = None
    """树洞回复数"""
    likenum: Optional[int] = None
    """树洞关注数"""
    tag: Optional[str] = None
    """树洞标签"""
    extra: Optional[int] = None
    """树洞额外信息（暂不确定其具体含义，可能为带图的洞额外计数）"""

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        """
        从字典数据创建树洞对象
        """
        return cls(
            pid=int(data["pid"]),
            text=data["text"],
            timestamp=int(data["timestamp"]),
            reply=int(data["reply"]),
            likenum=int(data["likenum"]),
            type=data["type"],
            extra=int(data["extra"]),
            url=data["url"],
            tag=data["tag"],
        )

    def __repr__(self):
        return str(self.data)

    @property
    def data(self):
        """
        树洞数据转字典
        """
        return self.__dict__


@dataclass(init=True, repr=False, order=False, unsafe_hash=True, frozen=False)
class Comment:
    """
    树洞回复数据模型
    """

    cid: Optional[int] = None
    """回复 ID"""
    pid: Optional[int] = None
    """树洞 ID"""
    timestamp: Optional[int] = None
    """回复时间戳"""

    name: Optional[str] = None
    """回复者昵称"""
    islz: Optional[int] = None
    """是否为洞主回复（0 为否，1 为是）"""
    text: Optional[str] = None
    """回复文本内容"""

    tag: Optional[str] = None
    """回复标签"""
    # TODO: Figure out the meaning of following field
    anonymous: Optional[int] = None
    """是否为匿名回复（0 为否，1 为是）"""

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        """
        从字典数据创建回复对象
        """
        return cls(
            cid=int(data["cid"]),
            pid=int(data["pid"]),
            text=data["text"],
            timestamp=int(data["timestamp"]),
            tag=data["tag"],
            islz=int(data["islz"]),
            name=data["name"],
            anonymous=int(data["anonymous"]),
        )

    def __repr__(self):
        return str(self.data)

    @property
    def data(self):
        """
        回复数据转字典
        """
        return self.__dict__


@dataclass(init=True, repr=False, order=False, unsafe_hash=True, frozen=False)
class ListHole(Hole):
    """
    树洞数据模型（来自首页）
    """

    hidden: Optional[int] = None
    """树洞是否被隐藏（0 为否，1 为是）"""
    hot: Optional[int] = None
    """热门时间戳（不确定，似乎总与 timestamp 一致）"""

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        """
        从字典数据创建树洞对象
        """
        return cls(
            pid=int(data["pid"]),
            text=data["text"],
            timestamp=int(data["timestamp"]),
            reply=int(data["reply"]),
            likenum=int(data["likenum"]),
            type=data["type"],
            extra=int(data["extra"]),
            url=data["url"],
            tag=data["tag"],
            hidden=int(data["hidden"]),
            hot=int(data["hot"]),
        )


@dataclass(init=True, repr=False, order=False, unsafe_hash=True, frozen=False)
class AttentionHole(Hole):
    """
    树洞数据模型（来自关注）
    """

    attention_tag: Optional[str] = None
    """关注标签（暂不确定其具体含义）"""

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        """
        从字典数据创建树洞对象
        """
        return cls(
            pid=int(data["pid"]),
            text=data["text"],
            timestamp=int(data["timestamp"]),
            reply=int(data["reply"]),
            likenum=int(data["likenum"]),
            type=data["type"],
            extra=int(data["extra"]),
            url=data["url"],
            tag=data["tag"],
            attention_tag=data["attention_tag"],
        )


class UserNameMeta(type):
    prefixes = [
        "",
        "Angry",
        "Baby",
        "Crazy",
        "Diligent",
        "Excited",
        "Fat",
        "Greedy",
        "Hungry",
        "Interesting",
        "Jolly",
        "Kind",
        "Little",
        "Magic",
        "Naïve",
        "Old",
        "Powerful",
        "Quiet",
        "Rich",
        "Superman",
        "THU",
        "Undefined",
        "Valuable",
        "Wifeless",
        "Xiangbuchulai",
        "Young",
        "Zombie",
    ]
    suffixes = [
        "Alice",
        "Bob",
        "Carol",
        "Dave",
        "Eve",
        "Francis",
        "Grace",
        "Hans",
        "Isabella",
        "Jason",
        "Kate",
        "Louis",
        "Margaret",
        "Nathan",
        "Olivia",
        "Paul",
        "Queen",
        "Richard",
        "Susan",
        "Thomas",
        "Uma",
        "Vivian",
        "Winnie",
        "Xander",
        "Yasmine",
        "Zach",
    ]
    overflow = "You Win"

    def __contains__(cls, item: str) -> bool:
        assert isinstance(item, str)
        name_lst = item.split()
        assert 1 <= len(name_lst) <= 3
        if len(name_lst) == 1:
            return name_lst[0].capitalize() in cls.suffixes
        elif len(name_lst) == 2:
            return (
                name_lst[0].capitalize() in cls.prefixes
                and name_lst[1].capitalize() in cls.suffixes
            )
        else:
            return [
                name_lst[0].capitalize(),
                name_lst[1].capitalize(),
            ] == cls.overflow.split() and name_lst[2].isdigit()

    def __getitem__(cls, x: Union[int, str]) -> Union[str, int]:
        if isinstance(x, int):
            if x < len(cls.prefixes) * len(cls.suffixes):
                if x < len(cls.suffixes):
                    return (
                        cls.prefixes[x // len(cls.suffixes)]
                        + cls.suffixes[x % len(cls.suffixes)]
                    )
                else:
                    return (
                        cls.prefixes[x // len(cls.suffixes)]
                        + " "
                        + cls.suffixes[x % len(cls.suffixes)]
                    )
            else:
                return cls.overflow + " " + str(x)
        elif isinstance(x, str):
            if not x in cls:
                raise ValueError(f"Invalid user name: {x}")
            name_lst = x.split()
            if len(name_lst) == 1:
                return cls.suffixes.index(name_lst[0].capitalize())
            elif len(name_lst) == 2:
                return cls.prefixes.index(name_lst[0].capitalize()) * len(
                    cls.suffixes
                ) + cls.suffixes.index(name_lst[1].capitalize())
            else:
                return int(name_lst[2])


class UserName(metaclass=UserNameMeta):
    """
    用户昵称名数据模型

    判断是否为合法昵称（大小写不敏感）：

    ```python
    "Angry alice" in UserName # True
    "Angrya lice" in UserName # False
    ```

    编号与昵称互转（大小写不敏感，下标从 0 开始）：

    ```python
    UserName[48]     # "Angry Winnie"
    UserName["You Win 1234"]  # 1234
    ```
    """


GenericHole = TypeVar("GenericHole", Hole, ListHole, AttentionHole)
"""
泛树洞类型

用于标记函数的参数类型，表示该函数可以接受任意类型的树洞。
"""
