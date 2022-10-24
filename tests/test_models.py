from treehole import Hole, ListHole, AttentionHole, Comment, UserName

data = {
    "pid": "4216687",
    "text": "请问怎么在门户里查自己的尸检结果呀",
    "type": "text",
    "timestamp": "1666248960",
    "reply": "74",
    "likenum": "108",
    "extra": "0",
    "url": "",
    "tag": None,
}

print("Hole", Hole.from_data(data))

data = {
    "pid": "4225323",
    "hidden": "0",
    "text": "计概辅导的学长一般是几年级的呀",
    "type": "text",
    "timestamp": "1666429825",
    "reply": "1",
    "likenum": "1",
    "extra": "0",
    "url": "",
    "hot": "1666429825",
    "tag": None,
}

print("ListHole", ListHole.from_data(data))

data = {
    "pid": "4114903",
    "text": "网盘崩了？上传极慢，加载极慢",
    "type": "text",
    "timestamp": "1664124157",
    "reply": "5",
    "extra": "0",
    "url": "",
    "likenum": "1",
    "tag": None,
    "attention_tag": None,
}

print("AttentionHole", AttentionHole.from_data(data))

data = {
    "cid": "18898276",
    "pid": "4224963",
    "text": "[Alice] 统计大家今天呼吸了吗，呼吸的扣a，没呼吸的扣b",
    "timestamp": "1666424757",
    "anonymous": "1",
    "tag": None,
    "islz": 0,
    "name": "Alice",
}

print("Comment", Comment.from_data(data))

assert ("Angry Alice" in UserName) == True
assert ("alice" in UserName) == True
assert ("a_lice" in UserName) == False
assert ("you win 1234" in UserName) == True
assert ("you win a234" in UserName) == False

assert UserName["you win 1234"] == 1234
assert UserName[1234] == "You Win 1234"
assert UserName["angry alice"] == 26
assert UserName[48] == "Angry Winnie"
assert UserName[17] == "Richard"
assert UserName["zach"] == 25
