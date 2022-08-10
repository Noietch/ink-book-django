import json

email_config = {
    "email_sender": "19802570583@163.com",
    "authority_code": "EIIHGBDRVXXCFWMZ"
}

img_path = "/home/ubuntu/static_resources/files"
img_url = "https://www.noietch.cn/resource/files"

template_path = "/home/ubuntu/static_resources/templates/"
document_template = "documents/"
prototype_template = "prototypes/"
document_template_choices = ['无模板', '安装维护手册', '可行性分析文档', '软件测试报告', '软件实施方案', 
                            '软件测试计划', '需求规格说明书']
prototype_template_choices = ['无模板', '华为机壳', 'ipad机壳', 'ipone机壳', '电脑', '苹果电脑', '京东电脑版首页', 
                            '京东手机版', '视频网站首页', '视频网站详情', '视频网站个人信息', '游戏', '知网首页']

default_file_system = {'name': '文档中心', 'id': 1, 'isProject': False, 'isLeaf': False, 'dragDisabled': True, 'addTreeNodeDisabled': False, 'addLeafNodeDisabled': False, 'editNodeDisabled': True, 'delNodeDisabled': True, 'children': [{'name': '项目文档区', 'id': 2, 'isLeaf': False, 'isProject': False, 'dragDisabled': True, 'addTreeNodeDisabled': True, 'addLeafNodeDisabled': True, 'editNodeDisabled': True, 'delNodeDisabled': True, 'children': []}, {'name': 'Readme.md', 'id': 3, 'dragDisabled': True, 'editNodeDisabled': False, 'delNodeDisabled': False, 'isLeaf': True}]}


if __name__ == '__main__':
    import json
    with open("tree.txt",encoding="utf-8") as f:
        tree = json.loads(f.read())
        stack = [tree]
        while len(stack) > 0:
            cur_node = stack.pop()
            if cur_node["isLeaf"] == True:
                print(cur_node)
            else:
                print(cur_node["id"])
                print(type(cur_node["id"]))
                for node in cur_node["children"]:
                    stack.append(node)