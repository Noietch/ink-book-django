import json

email_config = {
    "email_sender": "19802570583@163.com",
    "authority_code": "EIIHGBDRVXXCFWMZ"
}

img_path = "/home/ubuntu/static_resources/files"
img_url = "https://www.noietch.cn/resource/files"

template_path = "/home/ubuntu/static_resources/templates"
document_template = "/documents"
prototype_template = "/prototypes"
document_template_choices = ['无模板', '安装维护手册', '可行性分析文档', '软件测试报告', '软件实施方案', '软件测试计划', '需求规格说明书']


default_file_system = {'name': '文档中心', 'id': 1, 'isProject': False, 'isLeaf': False, 'dragDisabled': True, 'addTreeNodeDisabled': False, 'addLeafNodeDisabled': False, 'editNodeDisabled': True, 'delNodeDisabled': True, 'children': [{'name': '项目文档区', 'id': 2, 'isLeaf': False, 'isProject': False, 'dragDisabled': True, 'addTreeNodeDisabled': True, 'addLeafNodeDisabled': True, 'editNodeDisabled': True, 'delNodeDisabled': True, 'children': []}, {'name': 'Readme.md', 'id': 3, 'dragDisabled': True, 'editNodeDisabled': False, 'delNodeDisabled': False, 'isLeaf': True}]}


if __name__ == '__main__':
    dir_list = default_file_system["children"]
    for dir in dir_list:
        if dir["name"] == "项目文档区":
            print(dir["children"])

