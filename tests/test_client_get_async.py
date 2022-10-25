import json
import os

import pytest
from treehole import AttentionHole, Comment, Hole, ListHole, TreeHoleClient

os.chdir(os.path.dirname(os.path.abspath(__file__)))

secrets = json.load(open("secrets.json"))

client = TreeHoleClient(secrets["token"])


@pytest.mark.asyncio
async def test_get_hole_async():
    hole, timestamp = await client.get_hole_async(3153214)
    assert hole is not None and timestamp is not None
    assert hole.pid == 3153214
    assert hole.timestamp is not None and isinstance(hole.timestamp, int)
    assert hole.type in ("text", "image")
    assert hole.url is not None and isinstance(hole.url, str)
    assert hole.reply is not None and isinstance(hole.reply, int)
    assert hole.likenum is not None and isinstance(hole.likenum, int)
    assert hole.tag is not None and isinstance(hole.tag, str)
    assert hole.extra is not None and isinstance(hole.extra, int)


@pytest.mark.asyncio
async def test_get_image_async():
    hole, _ = await client.get_hole_async(4229210)
    assert hole is not None and isinstance(hole, Hole)
    image, img_type = client.get_hole_image(hole)
    assert image is not None and isinstance(image, bytes)
    assert img_type == "image/jpeg"


@pytest.mark.asyncio
async def test_get_comment_async():
    comments, attention = await client.get_comment_async(3153214)
    assert attention is not None and isinstance(attention, int)
    assert comments is not None and isinstance(comments, list)
    assert isinstance(comments[0], Comment)
    assert comments[0].pid == 3153214
    assert comments[0].cid is not None and isinstance(comments[0].cid, int)
    assert comments[0].timestamp is not None and isinstance(comments[0].timestamp, int)
    assert comments[0].name is not None and isinstance(comments[0].name, str)
    assert comments[0].text is not None and isinstance(comments[0].text, str)
    assert comments[0].tag is None or isinstance(comments[0].tag, str)
    assert comments[0].anonymous in (0, 1)
    assert comments[0].islz in (0, 1)


@pytest.mark.asyncio
async def test_get_holes_async():
    holes, _ = await client.get_holes_async()
    assert holes is not None and isinstance(holes, list)
    assert isinstance(holes[0], ListHole)
    assert holes[0].pid is not None and isinstance(holes[0].pid, int)
    assert holes[0].timestamp is not None and isinstance(holes[0].timestamp, int)
    assert holes[0].url is not None and isinstance(holes[0].url, str)
    assert holes[0].reply is not None and isinstance(holes[0].reply, int)
    assert holes[0].likenum is not None and isinstance(holes[0].likenum, int)
    assert holes[0].extra is not None and isinstance(holes[0].extra, int)
    assert holes[0].tag is None or isinstance(holes[0].tag, str)
    assert holes[0].type in ("text", "image")
    assert holes[0].hidden in (0, 1)
    assert holes[0].hot == holes[0].timestamp


@pytest.mark.asyncio
async def test_get_attention_async():
    holes, _ = await client.get_attention_async()
    assert holes is not None and isinstance(holes, list)
    assert isinstance(holes[0], AttentionHole)
    assert holes[0].pid is not None and isinstance(holes[0].pid, int)
    assert holes[0].timestamp is not None and isinstance(holes[0].timestamp, int)
    assert holes[0].url is not None and isinstance(holes[0].url, str)
    assert holes[0].reply is not None and isinstance(holes[0].reply, int)
    assert holes[0].likenum is not None and isinstance(holes[0].likenum, int)
    assert holes[0].extra is not None and isinstance(holes[0].extra, int)
    assert holes[0].tag is None or isinstance(holes[0].tag, str)
    assert holes[0].attention_tag is None or isinstance(holes[0].attention_tag, str)


@pytest.mark.asyncio
async def test_get_search_async():
    holes = await client.get_search_async(["key1", "key2"])
    assert holes is not None and isinstance(holes, list)
    assert isinstance(holes[0], Hole)
    assert holes[0].pid is not None and isinstance(holes[0].pid, int)
    assert holes[0].timestamp is not None and isinstance(holes[0].timestamp, int)
    assert holes[0].url is not None and isinstance(holes[0].url, str)
    assert holes[0].reply is not None and isinstance(holes[0].reply, int)
    assert holes[0].likenum is not None and isinstance(holes[0].likenum, int)
    assert holes[0].extra is not None and isinstance(holes[0].extra, int)
    assert holes[0].tag is None or isinstance(holes[0].tag, str)
    assert holes[0].type in ("text", "image")