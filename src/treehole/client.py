"""
树洞客户端，处理收发请求
"""
from functools import cache
from typing import Dict, List, Optional, Tuple, Union

import aiofiles
import aiohttp
import requests
from requests.compat import urljoin

from .models import Comment, Hole, UserName
from .utils import AuthError, EmptyError, logger

__all__ = ["TreeHoleClient"]

BASE_URL = "https://treehole.pku.edu.cn/api/"
REQUEST_HEADER = {}
BASE_QUERY = {}


class TreeHoleClient:
    """
    树洞交互客户端，低程度封装
    """

    def __init__(
        self,
        token: Optional[str] = None,
        uid: Optional[Union[int, str]] = None,
        password: Optional[str] = None,
        header: Optional[Dict[str, str]] = None,
        base_param: Optional[Dict[str, str]] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        - token:
            用户 token（可在树洞 cookies 中 pku_token 字段中获取）
        - uid:
            IAAA 账号 ID（可选的登录方式）
        - password:
            IAAA 账号密码（可选的登录方式）
        - header:
            额外的请求头，可选
        - base_param:
            额外的请求参数，可选
        - base_url:
            其他树洞 API 地址，可选
        """
        self.__base_url = base_url or BASE_URL
        if token:
            self.__token = token
        elif uid and password:
            __token = self.__auth(uid, password)
            if not __token:
                raise AuthError("Failed to login")
            self.__token = __token
        else:
            raise AuthError("No token or uid and password provided")
        self.__header = {
            **REQUEST_HEADER,
            **{"authorization": "Bearer " + self.__token},
            **(header or {}),
        }
        self.__base_param = {
            **BASE_QUERY,
            **(base_param or {}),
        }

    def __auth(self, uid: Union[int, str], password: str) -> Optional[str]:
        """
        登录，获取 token

        Parameters
        ----------
        - uid: IAAA 账号 ID
        - password: IAAA 账号密码

        Returns
        -------
        1. token，登录失败则返回 `None`
        """

        if not self.__is_num(uid):
            raise ValueError("uid must be an integer or string of interger")
        auth_data = {"uid": uid, "password": password}
        response = requests.post(
            self.login_url,
            data=auth_data,
        )
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not response_dict["success"]:
            logger.error("Failed to login, response: %s", response_dict)
            return None
        return response_dict["data"]["jwt"]

    @property
    def token(self) -> str:
        """用户 token，只读"""
        return self.__token

    @property
    def header(self) -> Dict[str, str]:
        """请求头，只读"""
        return self.__header

    @property
    def base_param(self) -> Dict[str, str]:
        """请求参数，只读"""
        return self.__base_param

    @property
    def base_url(self) -> str:
        """请求地址，只读"""
        return self.__base_url

    @property
    @cache
    def login_url(self) -> str:
        """登陆请求地址，只读"""
        return urljoin(self.base_url, "login/")

    @property
    @cache
    def hole_url(self) -> str:
        """树洞请求地址，只读"""
        return urljoin(self.base_url, "pku/")

    @property
    @cache
    def holes_url(self) -> str:
        """首页及搜索树洞请求地址，只读"""
        return urljoin(self.base_url, "pku_hole/")

    @property
    @cache
    def comment_url(self) -> str:
        """树洞评论请求地址，只读"""
        return urljoin(self.base_url, "pku_comment/")

    @property
    @cache
    def follow_url(self) -> str:
        """关注列表请求地址，只读"""
        return urljoin(self.base_url, "follow/")

    @property
    @cache
    def image_url(self) -> str:
        """树洞图片请求地址，只读"""
        return urljoin(self.base_url, "pku_image/")

    @property
    @cache
    def attention_url(self) -> str:
        """设置关注请求地址，只读"""
        return urljoin(self.base_url, "pku_attention/")

    @property
    @cache
    def report_url(self) -> str:
        """举报请求地址，只读"""
        return urljoin(self.base_url, "pku_report/")

    @property
    @cache
    def store_url(self) -> str:
        """举报请求地址，只读"""
        return urljoin(self.base_url, "pku_store")

    @staticmethod
    def __is_num(pid: Union[int, str]) -> bool:
        try:
            int(pid)
        except ValueError:
            logger.exception("Invalid number: %s", pid)
            return False
        return True

    @staticmethod
    def __is_valid_response(response: requests.Response) -> bool:
        if response.status_code != 200:
            logger.error(
                "Failed to get reponse, status code: %s, response: %s",
                response.status_code,
                response.reason,
            )
            return False
        else:
            return True

    @staticmethod
    def __is_valid_client_response(response: aiohttp.ClientResponse) -> bool:
        if response.status != 200:
            logger.error(
                "Failed to get reponse, status code: %s, response: %s",
                response.status,
                response.reason,
            )
            return False
        else:
            return True

    def get_hole_image(self, hole: Hole) -> Union[Tuple[bytes, str], Tuple[None, None]]:
        """
        获取树洞图片

        Parameters
        ----------
        - hole:
            任一树洞类

        Returns
        -------
        1. 图片二进制数据，不包含图片或请求错误则返回 `None`
        2. 图片类型，不包含图片或请求错误则返回 `None`
        """

        if hole.type == "image":
            response = requests.get(
                urljoin(self.image_url, str(hole.pid)), headers=self.header
            )
            if self.__is_valid_response(response):
                return response.content, response.headers["Content-Type"]
        return (None, None)

    async def get_hole_image_async(
        self, hole: Hole
    ) -> Union[Tuple[bytes, str], Tuple[None, None]]:
        """
        异步获取树洞图片

        Parameters
        ----------
        - hole: 任一树洞类

        Returns
        -------
        1. 图片二进制数据，不包含图片或请求错误则返回 `None`
        2. 图片类型，不包含图片或请求错误则返回 `None`
        """

        if hole.type == "image":
            async with aiohttp.request(
                "GET",
                urljoin(self.image_url, str(hole.pid)),
                headers=self.header,
            ) as response:
                if self.__is_valid_client_response(response):
                    return (
                        await response.content.read(),
                        response.headers["Content-Type"],
                    )
        return (None, None)

    def get_comment(
        self,
        pid: Union[int, str],
        page: Union[int, str] = 1,
        page_size: Union[int, str] = 500,
    ) -> Optional[List[Comment]]:
        """
        获取树洞评论

        Parameters
        ----------
        - pid: 树洞 ID
        - page: 页码，默认为 1
        - page_size: 每页评论数，默认为 500

        Returns
        -------
        1. 评论列表，请求错误则返回 `None`
        """

        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        if not self.__is_num(page_size):
            raise ValueError("page_size must be an integer or string of interger")
        param = {
            **self.base_param,
            **{"page": str(page), "limit": str(page_size)},
        }
        response = requests.get(
            urljoin(self.comment_url, str(pid)), params=param, headers=self.header
        )
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not response_dict["success"]:
            logger.error("Failed to get comment, response: %s", response_dict)
            return None
        return list(map(Comment.from_data, response_dict["data"]["data"]))

    async def get_comment_async(
        self,
        pid: Union[int, str],
        page: Union[int, str] = 1,
        page_size: Union[int, str] = 500,
    ) -> Optional[List[Comment]]:
        """
        异步获取树洞评论

        Parameters
        ----------
        - pid: 树洞 ID
        - page: 页码，默认为 1
        - page_size: 每页评论数，默认为 500

        Returns
        -------
        1. 评论列表，请求错误则返回 `None`
        """

        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        if not self.__is_num(page_size):
            raise ValueError("page_size must be an integer or string of interger")
        param = {
            **self.base_param,
            **{"page": str(page), "limit": str(page_size)},
        }
        async with aiohttp.request(
            "GET",
            urljoin(self.comment_url, str(pid)),
            params=param,
            headers=self.header,
        ) as response:
            if not self.__is_valid_client_response(response):
                return None
            response_dict = await response.json()
            if not response_dict["success"]:
                logger.error("Failed to get comment, response: %s", response_dict)
                return None
            return list(map(Comment.from_data, response_dict["data"]["data"]))

    def get_hole(self, pid: Union[int, str]) -> Optional[Hole]:
        """
        获取单个树洞

        Parameters
        ----------
        - pid: 树洞 ID

        Returns
        -------
        1. 树洞，请求错误则返回 `None`
        """

        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        response = requests.get(
            urljoin(self.hole_url, str(pid)),
            params=self.base_param,
            headers=self.header,
        )
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not response_dict["success"]:
            logger.error("Failed to get hole, response: %s", response_dict)
            return None
        return Hole.from_data(response_dict["data"])

    async def get_hole_async(self, pid: Union[int, str]) -> Optional[Hole]:
        """
        异步获取单个树洞

        Parameters
        ----------
        - pid: 树洞 ID

        Returns
        -------
        1. 树洞，请求错误则返回 `None`
        """

        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        async with aiohttp.request(
            "GET",
            urljoin(self.hole_url, str(pid)),
            params=self.base_param,
            headers=self.header,
        ) as response:
            if not self.__is_valid_client_response(response):
                return None
            response_dict = await response.json()
            if not response_dict["success"]:
                logger.error("Failed to get hole, response: %s", response_dict)
                return None
            return Hole.from_data(response_dict["data"])

    def get_holes(
        self, page: Union[int, str] = 1, page_size: Union[int, str] = 25
    ) -> Optional[List[Hole]]:
        """
        获取首页树洞

        Parameters
        ----------
        - page: 列表页码，默认为 1
        - page_size: 每页数量，默认为 25

        Returns
        -------
        1. 首页树洞列表，请求错误则返回 `None`
        """

        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        if not self.__is_num(page_size):
            raise ValueError("page_size must be an integer or string of interger")
        param = {
            **self.base_param,
            **{"page": str(page), "limit": str(page_size)},
        }
        response = requests.get(self.holes_url, params=param, headers=self.header)
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not response_dict["success"]:
            logger.error("Failed to get hole list, response: %s", response_dict)
            return None
        return list(map(Hole.from_data, response_dict["data"]["data"]))

    async def get_holes_async(
        self, page: Union[int, str] = 1, page_size: Union[int, str] = 25
    ) -> Optional[List[Hole]]:
        """
        异步获取首页树洞

        Parameters
        ----------
        - page: 列表页码，默认为 1
        - page_size: 每页数量，默认为 25

        Returns
        -------
        1. 首页树洞列表，请求错误则返回 `None`
        """

        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        if not self.__is_num(page_size):
            raise ValueError("page_size must be an integer or string of interger")
        param = {
            **self.base_param,
            **{"page": str(page), "limit": str(page_size)},
        }
        async with aiohttp.request(
            "GET", self.holes_url, params=param, headers=self.header
        ) as response:
            if not self.__is_valid_client_response(response):
                return None
            response_dict = await response.json()
            if not response_dict["success"]:
                logger.error("Failed to get hole list, response: %s", response_dict)
                return None
            return list(map(Hole.from_data, response_dict["data"]["data"]))

    def get_followed(
        self, page: Union[int, str] = 1, page_size: Union[int, str] = 25
    ) -> Optional[List[Hole]]:
        """
        获取关注树洞

        Parameters
        ----------
        - page: 列表页码，默认为 1
        - page_size: 每页数量，默认为 25

        Returns
        -------
        1. 关注树洞列表，请求错误则返回 `None`
        """

        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        if not self.__is_num(page_size):
            raise ValueError("page_size must be an integer or string of interger")
        param = {
            **self.base_param,
            **{"page": str(page), "limit": str(page_size)},
        }
        response = requests.get(self.follow_url, params=param, headers=self.header)
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not response_dict["success"]:
            logger.error(
                "Failed to get followed hole list, response: %s", response_dict
            )
            return None
        return list(map(Hole.from_data, response_dict["data"]["data"]))

    async def get_followed_async(
        self, page: Union[int, str] = 1, page_size: Union[int, str] = 25
    ) -> Optional[List[Hole]]:
        """
        异步获取关注树洞

        Parameters
        ----------
        - page: 列表页码，默认为 1
        - page_size: 每页数量，默认为 25

        Returns
        -------
        1. 关注树洞列表，请求错误则返回 `None`
        """

        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        if not self.__is_num(page_size):
            raise ValueError("page_size must be an integer or string of interger")
        param = {
            **self.base_param,
            **{"page": str(page), "limit": str(page_size)},
        }
        async with aiohttp.request(
            "GET", self.follow_url, params=param, headers=self.header
        ) as response:
            if not self.__is_valid_client_response(response):
                return None
            response_dict = await response.json()
            if not response_dict["success"]:
                logger.error(
                    "Failed to get followed hole list, response: %s", response_dict
                )
                return None
            return list(map(Hole.from_data, response_dict["data"]["data"]))

    def get_search(
        self,
        keywords: Union[str, List[str]],
        page: Union[int, str] = 1,
        page_size: Union[int, str] = 50,
    ) -> Optional[List[Hole]]:
        """
        搜索树洞

        Parameters
        ----------
        - keywords: 搜索关键词
        - page: 列表页码，默认为 1
        - page_size: 每页数量，默认为 50

        Returns
        -------
        1. 搜索结果，请求错误则返回 `None`
        """
        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        if not self.__is_num(page_size):
            raise ValueError("page size must be an integer or string of interger")
        if isinstance(keywords, str):
            keywords = [keywords]
        param = {
            **self.base_param,
            **{
                "page": str(page),
                "limit": str(page_size),
                "keyword": " ".join(keywords),
            },
        }
        response = requests.get(self.holes_url, params=param, headers=self.header)
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not response_dict["success"]:
            logger.error("Failed to get search result, response: %s", response_dict)
            return None
        return list(map(Hole.from_data, response_dict["data"]["data"]))

    async def get_search_async(
        self,
        keywords: Union[str, List[str]],
        page: Union[int, str] = 1,
        page_size: Union[int, str] = 50,
    ) -> Optional[List[Hole]]:
        """
        异步搜索树洞

        Parameters
        ----------
        - keywords: 搜索关键词
        - page: 列表页码，默认为 1
        - page_size: 每页数量，默认为 50

        Returns
        -------
        1. 搜索结果，请求错误则返回 `None`
        """
        if not self.__is_num(page):
            raise ValueError("page must be an integer or string of interger")
        if not self.__is_num(page_size):
            raise ValueError("page size must be an integer or string of interger")
        if isinstance(keywords, str):
            keywords = [keywords]
        param = {
            **self.base_param,
            **{
                "page": str(page),
                "limit": str(page_size),
                "keyword": " ".join(keywords),
            },
        }
        async with aiohttp.request(
            "GET", self.holes_url, params=param, headers=self.header
        ) as response:
            if not self.__is_valid_client_response(response):
                return None
            response_dict = await response.json()
            if not response_dict["success"]:
                logger.error("Failed to get search result, response: %s", response_dict)
                return None
            return list(map(Hole.from_data, response_dict["data"]["data"]))

    def post_hole(
        self, text: str = "", image: Optional[Union[bytes, str]] = None
    ) -> Optional[bool]:
        """
        发布树洞

        Parameters
        ----------
        - text: 树洞内容
        - image: 树洞图片 (二进制数据或文件名)

        Returns
        -------
        1. 是否发布成功，请求错误则返回 `None`
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
                "text": text,
                "type": "image",
            }
            file = {"data": image}
        else:
            load = {
                "text": text,
                "type": "text",
            }
            file = {}
        response = requests.post(
            self.store_url,
            params=self.base_param,
            headers=self.header,
            data=load,
            files=file,
        )
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not response_dict["success"]:
            logger.exception("Post failed: %s", response_dict["messsage"])
        return response_dict["success"]

    async def post_hole_async(
        self, text: str = "", image: Optional[Union[bytes, str]] = None
    ) -> Optional[bool]:
        """
        异步发布树洞

        Parameters
        ----------
        - text: 树洞内容
        - image: 树洞图片 (二进制数据或文件名)

        Returns
        -------
        1. 是否发布成功，请求错误则返回 `None`
        """
        if not text and not image:
            raise EmptyError("Empty post is not allowed")
        if image is not None:
            if isinstance(image, str):
                try:
                    async with aiofiles.open(image, "rb") as f:
                        image = await f.read()
                except FileNotFoundError:
                    logger.error(f"File {image} not found")
                    raise FileNotFoundError("File not found")
                except Exception as e:
                    logger.error(f"Unknown error: {e}")
                    raise e
            # load for posting hole with image
            load = {
                "text": text,
                "type": "image",
                "data": image,
            }
        else:
            load = {
                "text": text,
                "type": "text",
            }
        async with aiohttp.request(
            "POST",
            self.store_url,
            params=self.base_param,
            headers=self.header,
            data=load,
        ) as response:
            if not self.__is_valid_client_response(response):
                return None
            response_dict = await response.json()
            if not response_dict["success"]:
                logger.exception("Post failed: %s", response_dict["messsage"])
            return response_dict["success"]

    def post_comment(
        self,
        pid: Union[int, str],
        text: str,
        reply_to: Optional[Union[int, str]] = None,
    ) -> Optional[bool]:
        """
        发布评论

        Parameters
        ----------
        - pid: 树洞 ID
        - text: 评论内容
        - reply_to: 回复的用户昵称或标号（非层号），`None` 为回复洞主（默认）

        Returns
        -------
        1. 回复是否成功，请求错误则返回 `None`
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
            "pid": str(pid),
            "text": text,
        }
        response = requests.post(
            self.comment_url, params=self.base_param, headers=self.header, data=load
        )
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not response_dict["success"]:
            logger.exception("Comment failed: %s", response_dict["messsage"])
        return response_dict["success"]

    async def post_comment_async(
        self,
        pid: Union[int, str],
        text: str,
        reply_to: Optional[Union[int, str]] = None,
    ) -> Optional[bool]:
        """
        异步发布评论

        Parameters
        ----------
        - pid: 树洞 ID
        - text: 评论内容
        - reply_to: 回复的用户昵称或标号（非层号），`None` 为回复洞主（默认）

        Returns
        -------
        1. 回复是否成功，请求错误则返回 `None`
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
            "pid": str(pid),
            "text": text,
        }
        async with aiohttp.request(
            "POST",
            self.comment_url,
            params=self.base_param,
            headers=self.header,
            data=load,
        ) as response:
            if not self.__is_valid_client_response(response):
                return None
            response_dict = await response.json()
            if not response_dict["success"]:
                logger.exception("Comment failed: %s", response_dict["messsage"])
            return response_dict["success"]

    def post_toggle_followed(
        self, pid: Union[int, str], two_factor: bool = False
    ) -> Union[Tuple[bool, int], Tuple[None, None]]:
        """
        切换关注状态

        Parameters
        ----------
        - pid: 树洞 ID
        - two_factor: 是否启用双重验证（默认为 `False`）

        Returns
        -------
        1. 是否成功切换关注状态，请求错误则返回 `None`
        2. 当前关注状态，`1` 为关注，`0` 为未关注，请求错误则返回 `None`
        """
        hole = self.get_hole(pid)
        if hole is None or hole.is_follow is None:
            logger.exception("Failed to get attention status of pid %s", pid)
            return (None, None)
        response = requests.post(
            urljoin(self.attention_url, str(pid)),
            params=self.base_param,
            headers=self.header,
        )
        if not self.__is_valid_response(response):
            return (None, None)
        response_dict = response.json()
        if not response_dict["success"]:
            logger.exception("Toggle attention failed: %s", response_dict["messsage"])
        if not two_factor:
            return (
                response_dict["success"],
                (1 - hole.is_follow) if response_dict["success"] else hole.is_follow,
            )
        hole_verify = self.get_hole(pid)
        if hole_verify is None or hole_verify.is_follow is None:
            logger.exception("Failed to get attention status of pid %s", pid)
            return (
                response_dict["success"],
                (1 - hole.is_follow) if response_dict["success"] else hole.is_follow,
            )
        return response_dict["success"], hole.is_follow

    async def post_toggle_followed_async(
        self, pid: Union[int, str], two_factor: bool = False
    ) -> Union[Tuple[bool, int], Tuple[None, None]]:
        """
        异步切换关注状态

        Parameters
        ----------
        - pid: 树洞 ID
        - two_factor: 是否启用双重验证（默认为 `False`）

        Returns
        -------
        1. 是否成功切换关注状态，请求错误则返回 `None`
        2. 当前关注状态，`1` 为关注，`0` 为未关注，请求错误则返回 `None`
        """
        hole = await self.get_hole_async(pid)
        if hole is None or hole.is_follow is None:
            logger.exception("Failed to get attention status of pid %s", pid)
            return (None, None)
        async with aiohttp.request(
            "POST",
            urljoin(self.attention_url, str(pid)),
            params=self.base_param,
            headers=self.header,
        ) as response:
            if not self.__is_valid_client_response(response):
                return (None, None)
            response_dict = await response.json()
            if not response_dict["success"]:
                logger.exception(
                    "Toggle attention failed: %s", response_dict["messsage"]
                )
            if not two_factor:
                return (
                    response_dict["success"],
                    (1 - hole.is_follow)
                    if response_dict["success"]
                    else hole.is_follow,
                )
            hole_verify = await self.get_hole_async(pid)
            if hole_verify is None or hole_verify.is_follow is None:
                logger.exception("Failed to get attention status of pid %s", pid)
                return (
                    response_dict["success"],
                    (1 - hole.is_follow)
                    if response_dict["success"]
                    else hole.is_follow,
                )
            return response_dict["success"], hole.is_follow

    def post_report(self, pid: Union[int, str], reason: str = "") -> Optional[bool]:
        """
        举报树洞（注意！举报自己的树洞会导致立刻被删并且禁言）

        Parameters
        ----------
        - pid: 树洞 ID
        - reason: 举报理由（默认为空）

        Returns
        -------
        1. 是否举报成功，请求错误则返回 `None`
        """
        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        load = {"reason": reason}
        response = requests.post(
            urljoin(self.report_url, str(pid)),
            params=self.base_param,
            headers=self.header,
            data=load,
        )
        if not self.__is_valid_response(response):
            return None
        response_dict = response.json()
        if not response_dict["success"]:
            logger.exception("Report failed: %s", response_dict["messsage"])
        return response_dict["success"]

    async def post_report_async(
        self, pid: Union[int, str], reason: str = ""
    ) -> Optional[bool]:
        """
        异步举报树洞（注意！举报自己的树洞会导致立刻被删并且禁言）

        Parameters
        ----------
        - pid: 树洞 ID
        - reason: 举报理由（默认为空）

        Returns
        -------
        1. 是否举报成功，请求错误则返回 `None`
        """
        if not self.__is_num(pid):
            raise ValueError("pid must be an integer or string of interger")
        load = {"reason": reason}
        async with aiohttp.request(
            "POST",
            urljoin(self.report_url, str(pid)),
            params=self.base_param,
            headers=self.header,
            data=load,
        ) as response:
            if not self.__is_valid_client_response(response):
                return None
            response_dict = await response.json()
            if not response_dict["success"]:
                logger.exception("Report failed: %s", response_dict["messsage"])
            return response_dict["success"]
