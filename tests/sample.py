from treehole import TreeHoleClient, Hole

token = input("Input token: ")
if not len(token):
    try:
        import json

        token = json.load(open("secrets.json"))["token"]
    except (FileNotFoundError, KeyError):
        print("You must provide a token to continue!")
        print("Either copy & paste or write it to secrets.json")
        exit(1)


def img_filter(hole: Hole):
    return hole.type == "image"


client = TreeHoleClient(token)
idx = 1
holes = client.get_holes(idx)
while not holes:
    print("No holes found, trying next page...")
    idx += 1
    holes = client.get_holes(idx)
holes_with_image = list(filter(img_filter, holes))
print(f"Found {len(holes_with_image)} holes with image out of {len(holes)} holes")
for hole in holes_with_image:
    print(hole.pid)
