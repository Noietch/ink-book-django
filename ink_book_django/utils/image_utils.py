import base64

def image_save(pic, path):
    with open(path, 'wb') as f:
        for content in pic.chunks():
            f.write(content)


def image_read(path):
    with open(path, 'rb') as f:
        image_data = f.read()
    return image_data

def base64_image(data, path):
    with open(path, 'wb') as f:
        content = data.split("base64,")
        image = base64.b64decode(content[1])
        f.write(image)

if __name__ == '__main__':
    pass
