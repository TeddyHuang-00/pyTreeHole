from treehole import Hole, Comment, UserName


fake_hole = {
    "pid": 463721894531,
    "hidden": 0,
    "text": "fake message",
    "type": "text",
    "timestamp": 546123785,
    "reply": 0,
    "likenum": 1,
    "extra": 0,
    "url": "",
    "tag": None,
    "label": 0,
    "label_info": None,
    "anonymous": 1,
    "is_top": 0,
    "status": 0,
    "is_comment": 1,
    "is_follow": 0,
    "is_protect": 0,
    "image_size": [897, 1653],
}

fake_comment = {
    "cid": 367219,
    "pid": 5467123805,
    "text": "[Alice] Hello world",
    "timestamp": 64712381543,
    "anonymous": 1,
    "tag": None,
    "hidden": 0,
    "islz": 0,
    "name": "Alice",
}


def test_hole_from_data():
    """Only for testing type convertion"""
    hole = Hole.from_data(fake_hole)
    assert hole is not None and isinstance(hole, Hole)
    assert isinstance(hole.pid, int)
    assert isinstance(hole.timestamp, int)
    assert isinstance(hole.reply, int)
    assert isinstance(hole.likenum, int)
    assert isinstance(hole.extra, int)


def test_comment_from_data():
    """Only testing type convertion"""
    comment = Comment.from_data(fake_comment)
    assert comment is not None and isinstance(comment, Comment)
    assert isinstance(comment.cid, int)
    assert isinstance(comment.pid, int)
    assert isinstance(comment.timestamp, int)
    assert isinstance(comment.anonymous, int)
    assert isinstance(comment.islz, int)


def test_user_name():
    assert "Angry Alice" in UserName
    assert "alice" in UserName
    assert "a_lice" not in UserName
    assert "you win 1234" in UserName
    assert "you win a234" not in UserName

    assert UserName["you win 702"] == 702
    assert UserName[1234] == "You Win 1234"
    assert UserName["angry alice"] == 26
    assert UserName[48] == "Angry Winnie"
    assert UserName[701] == "Zombie Zach"
    assert UserName["zach"] == 25
