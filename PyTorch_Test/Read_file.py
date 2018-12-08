import os


def read_file():
    filepath = "contract"
    files = os.listdir(filepath)
    result = []
    for file in files:
        if not os.path.isdir(file):
            f = open(filepath + "/" + file)
            iter_file = iter(f)
            str = ""
            for line in iter_file:  # 遍历文件，一行行遍历，读取文本
                str = str + line
            result.append(str)  # 每个文件的文本存到list中
    return result


if __name__ == '__main__':
    read_file()
