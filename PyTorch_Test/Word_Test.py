import re
import os
from collections import Counter

filename = "contract/123.sol"
dirname = os.getcwd()
fname = os.path.join(dirname, filename)
print(fname)

input_line = "The line 6 {} is(arriving) the spot"

with open(fname) as f:
    s = f.read()
# print(s)
s3 = re.sub("(?<!:)\\/\\/.*|\\/\\*(\\s|.)*?\\*\\/", "", s)  # 去掉注释
a = re.compile('(?<=").*?(?=")')
s4 = a.sub('', s3)
b = re.compile(r'[a-fA-F\d]{32}')
s5 = b.sub('', s4)
# print(s4)
s1 = s4.replace('\n', '').split(' ')
print(s1)
s2 = " ".join(s1)
print(s2)

pattern = r'''\/\*.*?\*\/'''
result_list = re.findall('[a-zA-Z_]+', s2)
print(result_list)
counter = Counter(result_list)
print(counter)


# 格式化要输出的每行数据，首尾各占8位，中间占18位
def formatResult(a, b, c):
    return alignment(str(a)) + alignment(str(b), 30) + alignment(str(c)) + '\n'


# 用于英汉混合对齐，汉字英文对齐，汉英对齐，中英对齐
def alignment(str1, space=8, align='left'):
    length = len(str1.encode('gbk'))
    space = space - length if space >= length else 0
    if align in ['left', 'l', 'L', 'Left', 'LEFT']:
        return str1 + ' ' * space
    elif align in ['right', 'r', 'R', 'Right', 'RIGHT']:
        return ' ' * space + str1
    elif align in ['center', 'c', 'C', 'Center', 'CENTER', 'centre']:
        return ' ' * (space // 2) + str1 + ' ' * (space - space // 2)
    return 'Unknown align format'


title = formatResult('No', 'Word', 'Frequency')
results = []
word_to_idx = []
allWord_to_idx = []
# 输出的数据：每一行：序号(8位) 词(30位) 频率(8位) '\n' 序号=List.index(element)+1
for i, (w, c) in enumerate(counter.most_common(), 1):
    results.append(formatResult(i, w, c))
    word_to_idx.append(w + '\n')

# 将结果写入文件中
writefile = "results/123.txt"
wpath = os.path.join(dirname, writefile)
with open(wpath, 'w') as f:
    f.write(''.join([title] + results))


writeWord = "results/123_word.txt"
word_path = os.path.join(dirname, writeWord)
with open(word_path, 'w') as f:
    f.write(''.join(word_to_idx))


writeAllword = "results/all_word.txt"
all_word_path = os.path.join(dirname, writeAllword)
with open(all_word_path, 'w') as f:
    f.write(''.join())
