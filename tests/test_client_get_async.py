import json
import os

import pytest
from treehole import Comment, Hole, TreeHoleClient

os.chdir(os.path.dirname(os.path.abspath(__file__)))

secrets = json.load(open("secrets.json"))

client = TreeHoleClient(secrets["token"])


@pytest.mark.asyncio
async def test_get_hole_async():
    hole = await client.get_hole_async(4609665)
    assert hole is not None
    assert hole.pid == 4609665
    assert isinstance(hole.timestamp, int)
    assert hole.type in ("text", "image")
    assert isinstance(hole.image_size, tuple)
    assert isinstance(hole.reply, int)
    assert isinstance(hole.likenum, int)
    assert isinstance(hole.label, int)
    assert isinstance(hole.extra, int)


@pytest.mark.asyncio
async def test_get_image_async():
    hole = await client.get_hole_async(4229210)
    assert isinstance(hole, Hole)
    image, img_type = await client.get_hole_image_async(hole)
    assert isinstance(image, bytes)
    assert img_type == "image/jpeg"


@pytest.mark.asyncio
async def test_get_comment_async():
    comments = await client.get_comment_async(3153214)
    assert isinstance(comments, list)
    assert isinstance(comments[0], Comment)
    assert comments[0].pid == 3153214
    assert isinstance(comments[0].cid, int)
    assert isinstance(comments[0].timestamp, int)
    assert isinstance(comments[0].name, str)
    assert isinstance(comments[0].text, str)
    assert comments[0].tag is None or isinstance(comments[0].tag, str)
    assert comments[0].anonymous in (0, 1)
    assert comments[0].islz in (0, 1)


@pytest.mark.asyncio
async def test_get_holes_async():
    holes = await client.get_holes_async()
    assert isinstance(holes, list)
    assert isinstance(holes[0], Hole)
    assert isinstance(holes[0].pid, int)
    assert isinstance(holes[0].timestamp, int)
    assert isinstance(holes[0].image_size, tuple)
    assert isinstance(holes[0].reply, int)
    assert isinstance(holes[0].likenum, int)
    assert isinstance(holes[0].extra, int)
    assert holes[0].tag is None or isinstance(holes[0].tag, str)
    assert holes[0].type in ("text", "image")


@pytest.mark.asyncio
async def test_get_followed_async():
    holes = await client.get_followed_async()
    assert isinstance(holes, list)
    assert isinstance(holes[0], Hole)
    assert isinstance(holes[0].pid, int)
    assert isinstance(holes[0].timestamp, int)
    assert isinstance(holes[0].image_size, tuple)
    assert isinstance(holes[0].reply, int)
    assert isinstance(holes[0].likenum, int)
    assert isinstance(holes[0].extra, int)
    assert holes[0].tag is None or isinstance(holes[0].tag, str)


@pytest.mark.asyncio
async def test_get_search_async():
    holes = await client.get_search_async(["key1", "key2"])
    assert isinstance(holes, list)
    assert isinstance(holes[0], Hole)
    assert isinstance(holes[0].pid, int)
    assert isinstance(holes[0].timestamp, int)
    assert isinstance(holes[0].image_size, tuple)
    assert isinstance(holes[0].reply, int)
    assert isinstance(holes[0].likenum, int)
    assert isinstance(holes[0].extra, int)
    assert holes[0].tag is None or isinstance(holes[0].tag, str)
    assert holes[0].type in ("text", "image")
