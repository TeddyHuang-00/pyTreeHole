from base64 import b64encode
import logging
from typing import Any, Optional, Union

import requests
from requests.compat import urlencode, urljoin

from .models import AttentionHole, Comment, GenericHole, Hole, ListHole, UserName

logger = logging.getLogger("pyTreeHole")


__all__ = ["Client"]


BASE_URL = "https://pkuhelper.pku.edu.cn/services/pkuhole/api.php"
IMG_URL = "https://pkuhelper.pku.edu.cn/services/pkuhole/images/"
REQUEST_HEADER = {
    "accept": "*/*",
    "accept-language": "zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "referer": "https://pkuhelper.pku.edu.cn/hole/",
    "referrerPolicy": "strict-origin-when-cross-origin",
}
BASE_QUERY = {
    "PKUHelperAPI": "3.0",
    "jsapiver": "201027113050-462894",
}


class CaptchaError(Exception):
    """用户可能需要验证"""


class EmptyError(Exception):
    """没有数据"""


class Client:
    """
    树洞交互客户端，低程度封装

    :param token: 用户 token
    :param header: 额外的请求头
    :param base_query: 额外的请求参数
    """

    def __init__(
        self,
        token: str,
        header: Optional[dict[str, str]] = None,
        base_query: Optional[dict[str, str]] = None,
    ) -> None:
        self.__token = token
        self.__header = {**REQUEST_HEADER, **(header or {})}
        self.__base_query = {
            **BASE_QUERY,
            **{"user_token": self.__token},
            **(base_query or {}),
        }
        # Check for token validity
        if len(self.__token) != 32:
            logger.exception("Invalid token found: %s", self.__token)
            raise ValueError("token must be 32 characters long")
        if not self.__token.isalnum():
            logger.exception("Invalid token found: %s", self.__token)
            raise ValueError("token must be alphanumeric")

    @property
    def token(self) -> str:
        """用户 token，只读"""
        return self.__token

    @property
    def header(self) -> dict[str, str]:
        return self.__header

    @property
    def base_query(self) -> dict[str, str]:
        return self.__base_query

    @staticmethod
    def __is_num(pid: Union[int, str]) -> bool:
        try:
            int(pid)
        except ValueError:
            logger.exception("Invalid number: %s", pid)
            return False
        return True

    @staticmethod
    def __process_image_url(hole: GenericHole) -> GenericHole:
        if hole.type == "image":
            hole.url = urljoin(IMG_URL, hole.url)
        return hole

    @staticmethod
    def __is_valid_response(response: requests.Response) -> bool:
        if response.status_code != 200:
            logger.error(
                "Failed to get reponse, status code: %s, response: %s",
                response.status_code,
                response.text.encode("utf-8").decode("unicode_escape"),
            )
            return False
        else:
            return True

    @staticmethod
    def __is_valid_json_code(response: dict[str, Any]) -> bool:
        # TODO: To be tested for exact error
        return response["code"] == 0

    @staticmethod
    def __is_valid_json_captcha(response: dict[str, Any]) -> bool:
        # TODO: To be tested for exact error
        return not response["captcha"]

    def get_hole_image(
        self, hole: GenericHole
    ) -> Union[tuple[bytes, str], tuple[None, None]]:
        """
        获取树洞图片

        :param hole: 树洞
        :return: 图片二进制数据和图片类型
        """
        if hole.type == "image":
            assert hole.url is not None
            response = requests.get(hole.url, headers=self.__header)
            if self.__is_valid_response(response):
                return response.content, response.headers["Content-Type"]
            return (None, None)
        return (None, None)

    def get_comment(
        self, pid: Union[int, str]
    ) -> Union[tuple[list[Comment], int], tuple[None, None]]:
        """
        获取树洞评论

        :param pid: 树洞洞号
        :return: 树洞评论列表，是否已关注
        """

        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        query = {
            **self.__base_query,
            **{"action": "getcomment", "pid": str(pid)},
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.get(url, headers=self.__header)
        if not self.__is_valid_response(response):
            return (None, None)
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            logger.error("Failed to get comment, response: %s", response_dict)
            return (None, None)
        if not self.__is_valid_json_captcha(response_dict):
            logger.warning("Captcha might be required, response: %s", response_dict)
            raise CaptchaError("Captcha might be required")
        return [
            Comment.from_data(comment) for comment in response_dict["data"]
        ], response_dict["attention"]

    def get_hole(
        self, pid: Union[int, str]
    ) -> Union[tuple[Hole, int], tuple[None, None]]:
        """
        获取单个树洞

        :param pid: 树洞洞号
        :return: 树洞主体，查询的时间戳
        """
        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        query = {
            **self.__base_query,
            **{"action": "getone", "pid": str(pid)},
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.get(url, headers=self.__header)
        if not self.__is_valid_response(response):
            return (None, None)
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            logger.error("Failed to get hole, response: %s", response_dict)
            return (None, None)
        return (
            self.__process_image_url(Hole.from_data(response_dict["data"])),
            response_dict["timestamp"],
        )

    def get_holes(
        self, page: Union[int, str] = 1
    ) -> Union[tuple[list[ListHole], int], tuple[None, None]]:
        """
        获取首页树洞

        :param page: 指定页数
        :return: 首页树洞列表，查询的时间戳
        """
        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        query = {
            **self.__base_query,
            **{"action": "getlist", "p": str(page)},
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.get(url, headers=self.__header)
        if not self.__is_valid_response(response):
            return (None, None)
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            logger.error("Failed to get hole list, response: %s", response_dict)
            return (None, None)
        return [
            self.__process_image_url(ListHole.from_data(hole))
            for hole in response_dict["data"]
        ], response_dict["timestamp"]

    def get_attention(
        self, page: Union[int, str] = 1
    ) -> Union[tuple[list[AttentionHole], int], tuple[None, None]]:
        """
        获取关注树洞

        :param page: 指定页数
        :return: 关注树洞列表，查询的时间戳
        """
        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        query = {
            **self.__base_query,
            **{"action": "getattention", "p": str(page)},
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.get(url, headers=self.__header)
        if not self.__is_valid_response(response):
            return (None, None)
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            logger.error(
                "Failed to get attention hole list, response: %s", response_dict
            )
            return (None, None)
        return [
            self.__process_image_url(AttentionHole.from_data(hole))
            for hole in response_dict["data"]
        ], response_dict["timestamp"]

    def get_search(
        self,
        keywords: Union[str, list[str]],
        page: Union[int, str] = 1,
        page_size: int = 50,
    ) -> Optional[list[Hole]]:
        """
        搜索树洞

        :param keywords: 搜索关键词
        :param page: 指定页数
        :return: 检索到的树洞列表
        """
        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        if not self.__is_num(page_size):
            raise ValueError("page size must be an integer or string of interger")
        if isinstance(keywords, str):
            keywords = [keywords]
        query = {
            **self.__base_query,
            **{
                "action": "search",
                "keywords": " ".join(keywords),
                "page": str(page),
                "pagesize": str(page_size),
            },
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.get(url, headers=self.__header)
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            logger.error("Failed to get resource, response: %s", response_dict)
            return None
        return [
            self.__process_image_url(Hole.from_data(hole))
            for hole in response_dict["data"]
        ]

    def post_hole(
        self, text: str = "", image: Optional[Union[bytes, str]] = None
    ) -> Optional[int]:
        """
        发布树洞

        :param content: 树洞内容
        :param image: 树洞图片 (文件名或二进制数据)
        :return: 洞号 (失败则返回 None)
        """
        if not text and not image:
            raise EmptyError("Empty post is not allowed")
        if image is not None:
            if isinstance(image, str):
                try:
                    image = open(image, "rb").read()
                except FileNotFoundError:
                    logger.error(f"File {image} not found")
                    raise FileNotFoundError("File not found")
                except Exception as e:
                    logger.error(f"Unknown error: {e}")
                    raise e
            # load for posting hole with image
            load = {
                "user_token": self.__base_query["user_token"],
                "text": text,
                "type": "image",
                "image": b64encode(image).decode("utf-8"),
            }
        else:
            load = {
                "user_token": self.__base_query["user_token"],
                "text": text,
                "type": "text",
            }
        query = {
            **self.__base_query,
            **{
                "action": "dopost",
            },
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.post(url, headers=self.__header, data=load)
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            logger.exception("Post failed: %s", response_dict["msg"])
            return None
        return int(response_dict["data"])

    def post_comment(
        self,
        pid: Union[int, str],
        text: str,
        reply_to: Optional[Union[int, str]] = None,
    ) -> Optional[int]:
        """
        发布评论

        :param pid: 树洞号
        :param text: 评论内容
        :param reply_to: 回复的用户 (默认为回复洞主)
        :return: 树洞号 (失败则返回 None)
        """
        if not text:
            raise EmptyError("Empty post is not allowed")
        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        if reply_to is not None:
            if isinstance(reply_to, str):
                assert reply_to in UserName, "Invalid reply_to"
                reply_to = " ".join([x.capitalize() for x in reply_to.split()])
            else:
                reply_to = UserName[reply_to]
            text = f"Re {reply_to}: {text}"
        load = {
            "user_token": self.__base_query["user_token"],
            "pid": str(pid),
            "text": text,
        }
        query = {
            **self.__base_query,
            **{
                "action": "docomment",
            },
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.post(url, headers=self.__header, data=load)
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            logger.exception("Comment failed: %s", response_dict["msg"])
            return None
        # Note that this return value is pid, not cid
        # Cannot help with that
        return int(response_dict["data"])

    def post_set_attention(self, pid: Union[int, str]) -> bool:
        """
        关注树洞

        :param pid: 树洞号
        :return: 是否关注成功 (已经订阅的树洞返回 False)
        """
        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        load = {
            "user_token": self.__base_query["user_token"],
            "pid": str(pid),
            "switch": "1",
        }
        query = {
            **self.__base_query,
            **{
                "action": "attention",
            },
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.post(url, headers=self.__header, data=load)
        if not self.__is_valid_response(response):
            return False
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            logger.exception("Subscribe failed: %s", response_dict["msg"])
            # TODO: Test if error would occur other than already subscribed
            return False
        return True

    def post_remove_attention(self, pid: Union[int, str]) -> bool:
        """
        取消关注树洞

        :param pid: 树洞号
        :return: 是否取关成功 (未关注的树洞也返回 True)
        """
        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        load = {
            "user_token": self.__base_query["user_token"],
            "pid": str(pid),
            "switch": "0",
        }
        query = {
            **self.__base_query,
            **{
                "action": "attention",
            },
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.post(url, headers=self.__header, data=load)
        if not self.__is_valid_response(response):
            return False
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            logger.exception("Subscribe failed: %s", response_dict["msg"])
            # TODO: Test if error would occur other than already subscribed
            return False
        return True

    def post_toggle_attention(
        self, pid: Union[int, str], two_factor: bool = False
    ) -> Union[tuple[bool, Optional[int]], tuple[None, None]]:
        """
        切换关注状态

        :param pid: 树洞号
        :param two_factor: 是否二次验证 (默认 False)
        :return: 是否切换成功，当前关注状态
        """
        _, attention = self.get_comment(pid)
        if attention is None:
            logger.exception("Failed to get attention status of pid %s", pid)
            return (None, None)
        if attention:
            success = self.post_remove_attention(pid)
        else:
            success = self.post_set_attention(pid)
        if not two_factor:
            return (success, ((1 - attention) if success else attention))
        _, attention = self.get_comment(pid)
        if attention is None:
            logger.exception("Failed to get attention status of pid %s", pid)
            return (success, None)
        return success, attention

    def post_report(self, pid: Union[int, str], reason: str = "") -> bool:
        """
        举报树洞

        :param pid: 树洞号
        :param reason: 举报理由

        :return: 发送成功与否
        """
        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        load = {
            "user_token": self.__base_query["user_token"],
            "pid": str(pid),
            "reason": reason,
        }
        query = {
            **self.__base_query,
            **{
                "action": "report",
            },
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.post(url, headers=self.__header, data=load)
        if not self.__is_valid_response(response):
            return False
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            logger.exception("Report failed: %s", response_dict["msg"])
            return False
        return True
