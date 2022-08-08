import json

email_config = {
    "email_sender": "19802570583@163.com",
    "authority_code": "EIIHGBDRVXXCFWMZ"
}

img_path = "/home/ubuntu/static_resources/files"
img_url = "https://www.noietch.cn/resource/files"


default_file_system = {'name': '文档中心', 'id': 1, 'isProject': False, 'isLeaf': False, 'dragDisabled': True, 'addTreeNodeDisabled': False, 'addLeafNodeDisabled': False, 'editNodeDisabled': True, 'delNodeDisabled': True, 'children': [{'name': '项目文档区', 'id': 2, 'isLeaf': False, 'isProject': False, 'dragDisabled': True, 'addTreeNodeDisabled': True, 'addLeafNodeDisabled': False, 'editNodeDisabled': True, 'delNodeDisabled': True, 'children': []}, {'name': 'Readme.md', 'id': 3, 'dragDisabled': True, 'editNodeDisabled': True, 'delNodeDisabled': True, 'isLeaf': True}]}


if __name__ == '__main__':
    import json
    import time

    new_file = {
        "name": "Readme.md",
        "id": int(time.time()),
        "dragDisabled": True,
        "editNodeDisabled": True,
        "delNodeDisabled": True,
        "isLeaf": True
    }
    project_name = "项目1"
    with open("tree.txt",encoding="utf-8") as f:
        file_system = json.loads(f.read())
        dir_list = file_system["children"][0]["children"][0]["children"]
        for dir in dir_list:
            if dir["name"] == "项目文档区":
                for project in dir["children"]:
                    if project["name"] == project_name:
                        new_file = {
                            "name": "Readme.md",
                            "id": int(time.time()),
                            "dragDisabled": True,
                            "editNodeDisabled": True,
                            "delNodeDisabled": True,
                            "isLeaf": True
                        }
                    project["children"].append(new_file)
                    print(project["children"])