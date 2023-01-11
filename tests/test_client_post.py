import json
import os

import pytest
from treehole import TreeHoleClient

os.chdir(os.path.dirname(os.path.abspath(__file__)))

secrets = json.load(open("secrets.json"))

client = TreeHoleClient(secrets["token"])


# This unit test is safe to run
# Cause this is a long-dead hole
def test_post_comment():
    assert client.post_comment(33171, "Test comment", reply_to="alice")


# Absolutely safe to run
def test_post_attention():
    pid = 3153214
    success, attention = client.post_toggle_followed(pid)
    assert success
    assert attention is not None
    # Run it again to set it back to the original state
    assert client.post_toggle_followed(pid)[0]


# Do not run this unit test !!!!
# unless you know excatly what you are doing
@pytest.mark.skip(reason="This unit test will spam the server")
def test_post_hole():
    assert client.post_hole("test")


# Do not run this unit test !!!!
# unless you know excatly what you are doing
@pytest.mark.skip(reason="This unit test will cause people to be banned")
def test_post_report():
    assert client.post_report(0)
