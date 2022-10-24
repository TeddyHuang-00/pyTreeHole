from treehole import TreeHoleClient

import json

secrets = json.load(open("secrets.json"))

client = TreeHoleClient(secrets["backup_token"])

# # This test is not recommended,
# # as it will actually post a spam hole
# print("Test post")
# pid = client.post_hole("Test from pyTreeHole")
# print(pid)

# # This block of test is safe to run
# # Cause this is a long-dead hole
# print("Test comment")
# pid = client.post_comment(3075815, "Test comment")
# print(pid)

# # Recommend to run this test on a dead hole
# print("Test report")
# success = client.post_report(0)
# print(success)


# Absolutely safe to run
print("Test subscribe")
success = client.post_set_attention(0)
print(success)

print("Test unsubscribe")
success = client.post_remove_attention(4229210)
print(success)

print("Test toggle")
success, attention = client.post_toggle_attention(4229210)
print(success, attention)
