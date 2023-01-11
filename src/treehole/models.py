"""
树洞相关数据模型
"""

from dataclasses import dataclass
from typing import Any, Dict, Tuple, Optional, Union

__all__ = ("Hole", "Comment", "UserName")


@dataclass(init=True, repr=True, order=False, unsafe_hash=True, frozen=False)
class Label:
    """
    树洞标签数据模型
    """

    id: Optional[int] = None
    """标签 ID"""
    tag_name: Optional[str] = None
    """标签名称"""
    created_at: Optional[int] = None
    """创建时间"""
    updated_at: Optional[int] = None
    """更新时间"""

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        """
        从字典数据创建标签对象
        """
        return cls(
            id=data.get("id"),
            tag_name=data.get("tag_name"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


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
    image_size: Optional[Tuple[int, int]] = None
    """树洞图片大小（仅当 `type` 为 `image` 时非零）"""
    extra: Optional[int] = None
    """树洞额外信息（暂不确定其具体含义，可能为带图的洞额外计数）"""

    tag: Optional[str] = None
    """树洞标签"""
    label: Optional[int] = None
    """树洞标签分类"""
    label_info: Optional[Label] = None
    """树洞标签信息"""

    reply: Optional[int] = None
    """树洞回复数"""
    likenum: Optional[int] = None
    """树洞关注数"""
    anonymous: Optional[int] = None
    """树洞是否匿名（暂不确定）"""
    status: Optional[int] = None
    """树洞状态（暂不确定）"""
    is_top: Optional[int] = None
    """树洞是否置顶（暂不确定）"""
    is_comment: Optional[int] = None
    """树洞是否可评论（暂不确定）"""
    is_follow: Optional[int] = None
    """树洞是否已关注（暂不确定）"""
    is_protect: Optional[int] = None
    """树洞是否被保护（暂不确定）"""

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        """
        从字典数据创建树洞对象
        """
        return cls(
            pid=data.get("pid"),
            timestamp=data.get("timestamp"),
            type=data.get("type"),
            text=data.get("text"),
            image_size=tuple(data.get("image_size", (0, 0))),
            extra=data.get("extra"),
            tag=data.get("tag"),
            label=data.get("label"),
            label_info=Label.from_data(data.get("label_info", {}))
            if data.get("label_info")
            else None,
            reply=data.get("reply"),
            likenum=data.get("likenum"),
            anonymous=data.get("anonymous"),
            status=data.get("status"),
            is_top=data.get("is_top"),
            is_comment=data.get("is_comment"),
            is_follow=data.get("is_follow"),
            is_protect=data.get("is_protect"),
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
    """是否为匿名回复（暂不确定）"""
    hidden: Optional[int] = None
    """是否为隐藏回复（暂不确定）"""

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        """
        从字典数据创建回复对象
        """
        return cls(
            cid=data.get("cid"),
            pid=data.get("pid"),
            text=data.get("text"),
            timestamp=data.get("timestamp"),
            tag=data.get("tag"),
            islz=data.get("islz"),
            name=data.get("name"),
            anonymous=data.get("anonymous"),
        )

    def __repr__(self):
        return str(self.data)

    @property
    def data(self):
        """
        回复数据转字典
        """
        return self.__dict__


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
