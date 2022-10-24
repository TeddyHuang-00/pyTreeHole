from treehole import Hole, ListHole, AttentionHole, Comment, UserName


fake_hole = {
    "pid": "463721894531",
    "hidden": "0",
    "text": "fake message",
    "type": "text",
    "timestamp": "546123785",
    "reply": "0",
    "likenum": "1",
    "extra": "0",
    "url": "",
    "hidden": "0",
    "hot": "546123785",
    "tag": None,
    "attention_tag": None,
}

fake_comment = {
    "cid": "367219",
    "pid": "5467123805",
    "text": "[Alice] Hello world",
    "timestamp": "64712381543",
    "anonymous": "1",
    "tag": None,
    "islz": "0",
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


def test_list_hole_from_data():
    """Only for testing type convertion"""
    hole = ListHole.from_data(fake_hole)
    assert hole is not None and isinstance(hole, ListHole)
    assert isinstance(hole.pid, int)
    assert isinstance(hole.timestamp, int)
    assert isinstance(hole.reply, int)
    assert isinstance(hole.likenum, int)
    assert isinstance(hole.extra, int)
    assert isinstance(hole.hot, int)
    assert isinstance(hole.hidden, int)


def test_attention_hole_from_data():
    """Only testing type convertion"""
    hole = AttentionHole.from_data(fake_hole)
    assert hole is not None and isinstance(hole, AttentionHole)
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
