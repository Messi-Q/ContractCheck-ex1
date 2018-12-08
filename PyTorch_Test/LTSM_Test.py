import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.autograd import Variable

training_data = [("The dog ate the apple".split(),
                  ["DET", "NN", "V", "DET", "NN"]),
                 ("Everybody read that book".split(), ["NN", "V", "DET",
                                                       "NN"])]
# 每个单词就用一个数字表示，每种词性也用一个数字表示
word_to_idx = {}
tag_to_idx = {}
for context, tag in training_data:
    for word in context:
        if word not in word_to_idx:
            # 对词进行编码
            word_to_idx[word] = len(word_to_idx)
    for label in tag:
        if label not in tag_to_idx:
            # 对词性编码
            tag_to_idx[label] = len(tag_to_idx)


alphabet = 'abcdefghijklmnopqrstuvwxyz'
character_to_idx = {}
for i in range(len(alphabet)):
    # 对字母编码
    character_to_idx[alphabet[i]] = i


# 字符LSTM
class CharLSTM(nn.Module):
    def __init__(self, n_char, char_dim, char_hidden):
        super(CharLSTM, self).__init__()
        self.char_embedding = nn.Embedding(n_char, char_dim)
        self.char_lstm = nn.LSTM(char_dim, char_hidden, batch_first=True)

    def forward(self, x):
        x = self.char_embedding(x)
        _, h = self.char_lstm(x)
        # 取隐层
        return h[0]


class LSTMTagger(nn.Module):
    def __init__(self, n_word, n_char, char_dim, n_dim, char_hidden, n_hidden,
                 n_tag):
        super(LSTMTagger, self).__init__()
        self.word_embedding = nn.Embedding(n_word, n_dim)
        self.char_lstm = CharLSTM(n_char, char_dim, char_hidden)
        self.lstm = nn.LSTM(n_dim + char_hidden, n_hidden, batch_first=True)
        self.linear1 = nn.Linear(n_hidden, n_tag)

    def forward(self, x, word):
        char = torch.FloatTensor()
        for each in word:
            char_list = []
            for letter in each:
                # 对词进行字母编码
                char_list.append(character_to_idx[letter.lower()])
            char_list = torch.LongTensor(char_list)
            char_list = char_list.unsqueeze(0)
            if torch.cuda.is_available():
                tempchar = self.char_lstm(Variable(char_list).cuda())
            else:
                tempchar = self.char_lstm(Variable(char_list))
            tempchar = tempchar.squeeze(0)
            char = torch.cat((char, tempchar.cpu().data), 0)
        if torch.cuda.is_available():
            char = char.cuda()
        char = Variable(char)
        x = self.word_embedding(x)
        x = torch.cat((x, char), 1)  # char编码与word编码cat
        x = x.unsqueeze(0)
        # 取输出层 句长*n_hidden
        x, _ = self.lstm(x)
        x = x.squeeze(0)
        x = self.linear1(x)
        y = F.log_softmax(x)
        return y


model = LSTMTagger(
    len(word_to_idx), len(character_to_idx), 10, 100, 50, 128, len(tag_to_idx))
if torch.cuda.is_available():
    model = model.cuda()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=1e-2)


def make_sequence(x, dic):
    idx = [dic[i] for i in x]
    idx = Variable(torch.LongTensor(idx))
    return idx


for epoch in range(300):
    print('*' * 10)
    print('epoch {}'.format(epoch + 1))
    running_loss = 0
    for data in training_data:
        word, tag = data
        word_list = make_sequence(word, word_to_idx)
        tag = make_sequence(tag, tag_to_idx)
        if torch.cuda.is_available():
            word_list = word_list.cuda()
            tag = tag.cuda()
        # forward
        out = model(word_list, word)
        loss = criterion(out, tag)
        running_loss += loss.data[0]
        # backward 三步常规操作
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print('Loss: {}'.format(running_loss / len(data)))


print()
input = make_sequence("Everybody ate the apple".split(), word_to_idx)
if torch.cuda.is_available():
    input = input.cuda()
model.eval()  # 对dropout和batch normalization的操作在训练和测试的时候是不一样
out = model(input, "Everybody ate the apple".split())
print(out)
