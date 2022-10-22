import logging
from typing import Any, Optional, TypeVar, Union

import requests
from requests.compat import urlencode, urljoin

from .models import AttentionHole, Comment, Hole, ListHole

GenericHole = TypeVar("GenericHole", Hole, ListHole, AttentionHole)

logger = logging.getLogger("pyTreeHole")


class Actions:
    GET_ONE: str = "getone"
    GET_COMMENT: str = "getcomment"
    GET_LIST: str = "getlist"
    GET_ATTENTION: str = "getattention"
    SEARCH: str = "search"


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
        if response["code"] != 0:
            # TODO: To be tested for exact error
            logger.error("Failed to get comment, response: %s", response)
            return False
        return True

    @staticmethod
    def __is_valid_json_captcha(response: dict[str, Any]) -> bool:
        if response["captcha"]:
            # TODO: To be tested for exact error
            logger.warning("Captcha might be required, response: %s", response)
            return False
        return True

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
            **{"action": Actions.GET_COMMENT, "pid": str(pid)},
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.get(url, headers=self.__header)
        if not self.__is_valid_response(response):
            return (None, None)
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            return (None, None)
        if not self.__is_valid_json_captcha(response_dict):
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
            **{"action": Actions.GET_ONE, "pid": str(pid)},
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.get(url, headers=self.__header)
        if not self.__is_valid_response(response):
            return (None, None)
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
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
            **{"action": Actions.GET_LIST, "p": str(page)},
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.get(url, headers=self.__header)
        if not self.__is_valid_response(response):
            return (None, None)
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
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
            **{"action": Actions.GET_ATTENTION, "p": str(page)},
        }
        url = f"{BASE_URL}?{urlencode(query)}"
        response = requests.get(url, headers=self.__header)
        if not self.__is_valid_response(response):
            return (None, None)
        response_dict = response.json()
        if not self.__is_valid_json_code(response_dict):
            return (None, None)
        return [
            self.__process_image_url(AttentionHole.from_data(hole))
            for hole in response_dict["data"]
        ], response_dict["timestamp"]

    def search(
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
                "action": Actions.SEARCH,
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
            return None
        return [
            self.__process_image_url(Hole.from_data(hole))
            for hole in response_dict["data"]
        ]
