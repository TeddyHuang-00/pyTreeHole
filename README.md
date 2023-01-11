**重要通知！！**：由于原树洞更改了鉴权方式和请求地址，导致本包 v2.0.0 之前的版本均不可用，请及时将您的项目更新至 v2.0.0 及以上版本。

新版本树洞认证方法见[下文](#身份验证)

---

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

### 身份验证

您有两种方式来验证身份：

1. 使用用户名和密码登陆（不推荐）
   > 可以在实例化 `TreeHoleClient` 时传入 `uid`（学号）和 `password`（密码）参数即可，使用 IAAA 账号登陆
2. 使用 token 登陆（推荐，相对安全）
   > 树洞 token 的获取方式请参考 @Guyutongxue 的[操作说明](https://github.com/Guyutongxue/pkuhelper-web-score/blob/master/docs/treehole-jwt.md)（即此说明中的“北大树洞 JWT”），您也可以在浏览器的 cookies 中的 pku_token 字段处找到它。

### 代码示例

```python
from treehole import TreeHoleClient

# 使用 token 认证
client = TreeHoleClient(token=<Your Token>)
# 使用 IAAA 账号认证
client = TreeHoleClient(uid=<UID>, password=<Password>)
# 获取单个树洞
hole = client.get_hole(<Hole ID>)
# 获取树洞评论
comments = client.get_comment(<Hole ID>)
# 获取首页树洞列表
holes = client.get_holes(<Page Num>)
# 获取关注树洞列表
holes = client.get_followed(<Page Num>)
# 切换关注状态
success, status = client.post_toggle_followed(<Hole ID>)
# 发布树洞
success = client.post_hole(<Text>, <Image File>)
# 发布评论
success = client.post_comment(<Hole ID>, <Text>, <Reply To>)
# 举报树洞 (!!!!!! 请勿轻易尝试)
success = client.post_report(<Hole ID>, <Reason>)
```

用例请参考 [非异步](./tests/sample.py) 和 [异步](./tests/sample_async.py)

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

- [x] 支持新版树洞
- [x] 支持 IAAA 账号登陆
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
- [x] 支持自定义加载长度
- [ ] 更多功能待补充 ...
