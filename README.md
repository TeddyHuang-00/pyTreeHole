# TreeHole

> A simple Python interface to PKU Tree Hole

[![GitHub - License](https://img.shields.io/github/license/TeddyHuang-00/pyTreeHole?color=f1f2f6&logo=github&style=for-the-badge)](https://github.com/TeddyHuang-00/pyTreeHole/blob/main/LICENSE.txt)
[![Git - Last Doc Commit](https://img.shields.io/github/last-commit/TeddyHuang-00/pyTreeHole/gh-pages?color=a4b0be&logo=readthedocs&style=for-the-badge&label=documentation)](https://teddyhuang-00.github.io/pyTreeHole)

[![PyPI - Version](https://img.shields.io/pypi/v/treehole?color=2980b9&label=version&logo=python&style=for-the-badge)](https://pypi.org/project/treehole/)
[![PyPI - Downloads per month](https://img.shields.io/pypi/dm/TreeHole?color=01579b&label=downloads&logo=pypi&style=for-the-badge)](https://pypistats.org/packages/treehole)

![Pytest - Result](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FTeddyHuang-00%2FpyTreeHole%2Fmain%2Ftests%2Ftest_result.json&color=0097e0&logo=pytest&style=for-the-badge)
[![Git - Last Commit](https://img.shields.io/github/last-commit/TeddyHuang-00/pyTreeHole?color=c0392b&logo=git&style=for-the-badge)](https://github.com/TeddyHuang-00/pyTreeHole)

目前正在持续开发完善中，欢迎使用和提出建议！

## 亮点

- 简单易用
- 文档齐全
- token 登陆
- Python 3.6+
- 支持异步请求
- 自动处理图像 url
- 所有树洞数据模型均已封装为数据类
- 涵盖(几乎？)所有暴露给用户的业务逻辑

## 安装

已发布至 Pypi 源，可直接使用 pip 安装：

```bash
pip3 install TreeHole
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

用例请参考 [example](./tests/sample.py)

## 开发

克隆此仓库：

```bash
git clone git@github.com:TeddyHuang-00/pyTreeHole.git
```

编辑模式下：

```bash
pip3 install -e ".[test]"
```

欢迎提 issues 与 PR！

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
