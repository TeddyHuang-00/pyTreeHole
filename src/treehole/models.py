from dataclasses import dataclass
from typing import Any, Optional, TypeVar, Union

__all__ = ("Hole", "ListHole", "AttentionHole", "Comment", "GenericHole", "UserName")


@dataclass(init=True, repr=False, order=False, unsafe_hash=True, frozen=False)
class Hole:
    """
    树洞基本数据模型

    :param pid: 树洞 ID
    :param timestamp: 时间戳

    :param reply: 树洞回复数
    :param likenum: 树洞关注数

    :param type: 树洞类型 (目前仅有 'text' 或 'image')
    :param text: 树洞文本内容
    :param url: 树洞图像 URL (如果类型为 'image')

    :param extra: 树洞额外信息 (不确定)
    :param tag: 树洞标签 (不确定)
    """

    pid: Optional[str] = None
    timestamp: Optional[int] = None
    # type is either "text" or "image" at the moment
    type: Optional[str] = None
    text: Optional[str] = None
    url: Optional[str] = None

    reply: Optional[int] = None
    likenum: Optional[int] = None
    # Following fields I don't know what they are for
    extra: Optional[str] = None
    tag: Optional[str] = None

    @classmethod
    def from_data(cls, data: dict[str, Any]):
        return cls(
            pid=data["pid"],
            text=data["text"],
            timestamp=int(data["timestamp"]),
            reply=int(data["reply"]),
            likenum=int(data["likenum"]),
            type=data["type"],
            extra=data["extra"],
            url=data["url"],
            tag=data["tag"],
        )

    def __repr__(self):
        return str(self.data)

    @property
    def data(self):
        return self.__dict__


@dataclass(init=True, repr=False, order=False, unsafe_hash=True, frozen=False)
class Comment:
    """
    树洞回复数据模型

    :param cid: 回复 ID
    :param pid: 树洞 ID
    :param timestamp: 时间戳

    :param name: 回复者
    :param text: 回复内容
    :param islz: 是否为洞主

    :param anonymous: 是否匿名 (不确定，是则 1 为匿名)
    :param tag: 回复标签 (不确定)
    """

    cid: Optional[str] = None
    pid: Optional[str] = None
    timestamp: Optional[int] = None

    name: Optional[str] = None
    islz: Optional[int] = None
    text: Optional[str] = None

    tag: Optional[str] = None
    # I don't know what this field is for
    anonymous: Optional[str] = None

    @classmethod
    def from_data(cls, data: dict[str, Any]):
        return cls(
            cid=data["cid"],
            pid=data["pid"],
            text=data["text"],
            timestamp=int(data["timestamp"]),
            tag=data["tag"],
            islz=int(data["islz"]),
            name=data["name"],
            anonymous=data["anonymous"],
        )

    def __repr__(self):
        return str(self.data)

    @property
    def data(self):
        return self.__dict__


@dataclass(init=True, repr=False, order=False, unsafe_hash=True, frozen=False)
class ListHole(Hole):
    """
    树洞数据模型（来自列表）

    :param hidden: 是否隐藏（不确定，是则 1 为隐藏）
    :param hot: 热门时间戳（不确定，看起来与 timestamp 一致）

    :param pid: 树洞 ID
    :param timestamp: 时间戳

    :param reply: 树洞回复数
    :param likenum: 树洞关注数

    :param type: 树洞类型 (目前仅有 'text' 或 'image')
    :param text: 树洞文本内容
    :param url: 树洞图像 URL (如果类型为 'image')

    :param extra: 树洞额外信息 (不确定)
    :param tag: 树洞标签 (不确定)
    """

    hidden: Optional[int] = None
    hot: Optional[int] = None

    @classmethod
    def from_data(cls, data: dict[str, Any]):
        return cls(
            pid=data["pid"],
            text=data["text"],
            timestamp=int(data["timestamp"]),
            reply=int(data["reply"]),
            likenum=int(data["likenum"]),
            type=data["type"],
            extra=data["extra"],
            url=data["url"],
            tag=data["tag"],
            hidden=int(data["hidden"]),
            hot=int(data["hot"]),
        )


@dataclass(init=True, repr=False, order=False, unsafe_hash=True, frozen=False)
class AttentionHole(Hole):
    """
    树洞数据模型（来自关注）

    :param attention_tag: 关注标签（不确定）

    :param pid: 树洞 ID
    :param timestamp: 时间戳

    :param reply: 树洞回复数
    :param likenum: 树洞关注数

    :param type: 树洞类型 (目前仅有 'text' 或 'image')
    :param text: 树洞文本内容
    :param url: 树洞图像 URL (如果类型为 'image')

    :param extra: 树洞额外信息 (不确定)
    :param tag: 树洞标签 (不确定)
    """

    attention_tag: Optional[str] = None

    @classmethod
    def from_data(cls, data: dict[str, Any]):
        return cls(
            pid=data["pid"],
            text=data["text"],
            timestamp=int(data["timestamp"]),
            reply=int(data["reply"]),
            likenum=int(data["likenum"]),
            type=data["type"],
            extra=data["extra"],
            url=data["url"],
            tag=data["tag"],
            attention_tag=data["attention_tag"],
        )


GenericHole = TypeVar("GenericHole", Hole, ListHole, AttentionHole)


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
    用户名数据模型

    用法：

    ```python
    "Angry alice" in UserName # True
    UserName[48]     # "Angry Winnie"
    UserName["You Win 1234"]  # 1234
    ```
    """
