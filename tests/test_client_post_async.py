import json
import os

import pytest
from treehole import TreeHoleClient

os.chdir(os.path.dirname(os.path.abspath(__file__)))

secrets = json.load(open("secrets.json"))

client = TreeHoleClient(secrets["token"])


# This unit test is safe to run
# Cause this is a long-dead hole
@pytest.mark.asyncio
async def test_post_comment_async():
    assert await client.post_comment_async(3075815, "Test comment", reply_to="alice")


# Absolutely safe to run
@pytest.mark.asyncio
async def test_post_attention_async():
    pid = 3153214
    success, attention = await client.post_toggle_attention_async(pid)
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


# Do not run this unit test !!!!
# unless you know excatly what you are doing
@pytest.mark.skip(reason="This unit test will spam the server")
@pytest.mark.asyncio
async def test_post_hole_async():
    assert await client.post_hole_async("test")


# Do not run this unit test !!!!
# unless you know excatly what you are doing
@pytest.mark.skip(reason="This unit test will cause people to be banned")
@pytest.mark.asyncio
async def test_post_report_async():
    assert await client.post_report_async(0)
