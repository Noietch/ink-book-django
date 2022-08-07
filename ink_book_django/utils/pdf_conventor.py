import pdfkit


def convert(content, path):
    return pdfkit.from_string(content, path)