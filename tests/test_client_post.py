import json
import os

from treehole import TreeHoleClient

os.chdir(os.path.dirname(os.path.abspath(__file__)))

secrets = json.load(open("secrets.json"))

client = TreeHoleClient(secrets["backup_token"])


# This unit test is safe to run
# Cause this is a long-dead hole
def test_post_comment():
    assert client.post_comment(3075815, "Test comment", reply_to="alice")


# Absolutely safe to run
def test_post_attention():
    pid = 3153214
    success, attention = client.post_toggle_attention(pid)
    assert success
    assert attention is not None
    if attention:
        assert client.post_remove_attention(pid)
        assert client.post_set_attention(pid)
    else:
        assert client.post_set_attention(pid)
        assert client.post_remove_attention(pid)
    # Run it again to set it back to the original state
    assert client.post_toggle_attention(pid)[0]


# # Do not run this unit test !!!!
# # unless you know excatly what you are doing
# def test_post_hole():
#     assert client.post_hole("test")


# # Do not run this unit test !!!!
# # unless you know excatly what you are doing
# def test_post_report():
#     assert client.post_report(0)
