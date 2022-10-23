import json

from treehole import Client

secrets = json.load(open("secrets.json"))

client = Client(secrets["token"])

# Test on a hole with both text and image
print("Get Hole")
body, timestamp = client.get_hole(4229210)
assert body is not None and timestamp is not None
print("Body:", body)
image, img_type = client.get_hole_image(body)
assert image is not None and img_type is not None
print("Image:", img_type)
with open(f"tmp.{img_type.split('/')[-1]}", "wb") as f:
    f.write(image)

print("Get Comments")
comments, attention = client.get_comment(4224963)
assert comments is not None and attention is not None
print("Comments:", comments[:2] if comments else comments)

print("Get Holes")
holes, timestamp = client.get_holes()
assert holes is not None and timestamp is not None
print("Holes:", holes[:2] if holes else holes)

print("Get Attention")
holes, timestamp = client.get_attention()
assert holes is not None and timestamp is not None
print("Holes:", holes[:2] if holes else holes)

print("Get Search")
holes = client.get_search(["key1", "key2"])
assert holes is not None
print("Holes:", holes[:2] if holes else holes)
