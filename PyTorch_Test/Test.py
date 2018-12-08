import re
from collections import Counter
from PyTorch_Test.Read_file import read_file


input_file = read_file()
print(input_file)
input_file = "\n".join(input_file)
x = re.sub("(?<!:)\\/\\/.*|\\/\\*(\\s|.)*?\\*\\/", "", input_file)
a_1 = re.compile('(?<=").*?(?=")')
y = a_1.sub('', x)
b_1 = re.compile(r'[a-fA-F\d]{32}')
z = b_1.sub('', y)
output = z.replace('\n', '').split(' ')
output_1 = " ".join(output)

all_result_list = re.findall('[a-zA-Z_]+', output_1)
counter = Counter(all_result_list)
print(counter)
