"""
A simple interface to PKU Hole

[View in GitHub](https://github.com/TeddyHuang-00/pyTreeHole)

## 亮点

- 简单易用
- 文档齐全
- token 登陆
- Python 3.6+
- 支持异步请求
- 自动处理图像 url
- 所有树洞数据模型均已封装为数据类
- 涵盖(几乎？)所有暴露给用户的业务逻辑

## 快速上手

```py
from treehole import TreeHoleClient

client = TreeHoleClient("your token")
hole, timestamp = client.get_hole("hole ID")
print(hole)
```

## 使用

```python
from treehole import TreeHoleClient

client = TreeHoleClient(<Your Token>)
# 获取单个树洞
hole, timestamp = client.get_hole(<Hole ID>)
# 获取树洞评论
comments, attention = client.get_comment(<Hole ID>)
# 获取首页树洞列表
holes, timestamp = client.get_holes(<Page Num>)
# 获取关注树洞列表
holes, timestamp = client.get_attention(<Page Num>)
# 切换关注状态
success, attention = client.post_toggle_attention(<Hole ID>)
# 发布树洞
pid = client.post_hole(<Text>, <Image File>)
# 发布评论
pid = client.post_comment(<Hole ID>, <Text>, <Reply To>)
# 举报树洞 (!!!!!! 请勿轻易尝试)
success = client.post_report(<Hole ID>)
```

## Roadmap

- [x] 树洞数据模型
- [x] 客户端封装
- [x] 获取单个树洞
- [x] 获取首页树洞
- [x] 获取关注树洞
- [x] 获取树洞回复
- [x] 关注/取关树洞
- [x] 回复树洞
- [x] 发布树洞
- [x] 举报树洞
- [x] 支持异步处理
- [ ] 更多功能待补充 ...
"""

try:
    from importlib.metadata import PackageNotFoundError, version  # novm
except ImportError:  # Fallback for Python < 3.8
    from importlib_metadata import PackageNotFoundError, version  # novm

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "TreeHole"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .client import *
from .models import *
