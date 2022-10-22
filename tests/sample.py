from treehole import Client

token = input("Input token: ")
if len(token) != 32:
    try:
        import json

        token = json.load(open("secrets.json"))["token"]
    except (FileNotFoundError, KeyError):
        print("You must provide a token to continue!")
        print("Either copy & paste or write it to secrets.json")
        exit(1)


def img_filter(hole):
    return len(hole.url) > 0


client = Client(token)
idx = 1
holes, _ = client.get_holes(idx)
while not holes:
    print("No holes found, trying next page...")
    idx += 1
    holes, _ = client.get_holes(idx)
holes_with_image = list(filter(img_filter, holes))
print(f"Found {len(holes_with_image)} holes with image out of {len(holes)} holes")
img_urls = [hole.url for hole in holes_with_image]
print("Image URLs:")
for url in img_urls:
    print("\t", url)
