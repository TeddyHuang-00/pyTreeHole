import json

from treehole import Client

secrets = json.load(open("secrets.json"))

client = Client(secrets["token"])

# Test on a hole with both text and image
print("Get Hole")
body, timestamp = client.get_hole(4226377)
print("Body:", body)
print("Timestamp:", timestamp)

print("Get Comments")
comments, attention = client.get_comment(4224963)
print("Comments:", comments[:2] if comments else comments)
print("Attention:", attention)

print("Get Holes")
holes, timestamp = client.get_holes()
print("Holes:", holes[:2] if holes else holes)
print("Timestamp:", timestamp)

print("Get Attention")
holes, timestamp = client.get_attention()
print("Holes:", holes[:2] if holes else holes)
print("Timestamp:", timestamp)
