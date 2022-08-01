

def image_save(pic, path):
    with open(path, 'wb') as f:
        for content in pic.chunks():
            f.write(content)


def image_read(path):
    with open(path, 'rb') as f:
        image_data = f.read()
    return image_data


if __name__ == '__main__':
    pass
