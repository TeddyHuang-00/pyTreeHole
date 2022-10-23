# TreeHole

> A simple Python interface to PKU Tree Hole

目前正在持续开发完善中，欢迎使用和提出建议！

## 亮点

- 简单易用
- token 登陆
- 自动处理图像 url
- 所有树洞数据模型均已封装为数据类

## 安装

已发布至 Pypi 源，可直接使用 pip 安装：

```bash
pip3 install TreeHole
```

## 使用

```python
from treehole import Client

client = Client(<Your token>)
# 获取单个树洞
hole, timestamp = client.get_hole(<Hole ID>)
# 获取树洞评论
comments, attention = client.get_comment(<Hole ID>)
# 获取首页树洞列表
holes, timestamp = client.get_holes(<Page num>)
# 获取关注树洞列表
holes, timestamp = client.get_attention(<Page num>)
# 切换关注状态
success, attention = client.post_toggle_attention(<Hole ID>)
# 发布树洞
pid = client.post_hole(<Text>, <Image file>)
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
- [ ] 异步支持
  - 目前看来单个任务速度较快，如有明确需求再考虑添加
- [ ] 更多交互功能
  - 待补充 ...
- [ ] ...
