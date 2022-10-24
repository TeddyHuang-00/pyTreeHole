import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

src_file_name = "tmp.json"
out_file_name = "test_result.json"
if not os.path.exists(src_file_name):
    raise Exception("tmp.json not found")
data = json.load(open(src_file_name, "r"))["summary"]

out_dict = {
    "schemaVersion": 1,
    "label": "Pytest",
    "message": f"{data['passed'] / (data['total'] - data['skipped']):.0%} passed",
}

json.dump(out_dict, open(out_file_name, "w"))
