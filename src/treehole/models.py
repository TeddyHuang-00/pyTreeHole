from dataclasses import dataclass
from typing import Any, Optional

__all__ = ("Hole", "ListHole", "AttentionHole", "Comment")


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
