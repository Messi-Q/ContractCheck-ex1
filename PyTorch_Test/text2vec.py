import os
import numpy as np
import re
import time

INFO = __file__


def printMessage(message_type, trace, message):
    print ('%s %s [%s] %s' % (time.strftime('%d/%m/%Y %H:%M:%S'), message_type, trace, message))


def printStatus(trace, message):
    printMessage('INFO', trace, message)


def clean_str(string):
    string = re.sub(r"[^A-Za-z0-9]", " ", string)
    return string.strip().lower().split()


class Text2Vec:
    def __init__(self, datafile, ndims=0, L1_normalize=0, L2_normalize=0):
        printStatus(INFO + '.' + self.__class__.__name__, 'initializing ...')
        self.datafile = datafile
        self.ndims = ndims
        self.L1_normalize = L1_normalize
        self.L2_normalize = L2_normalize

        assert type(L1_normalize) == int
        assert type(L2_normalize) == int
        assert (L1_normalize + L2_normalize) <= 1

    def embedding(self, query):
        vec = self.mapping(query)
        if vec is not None:
            vec = np.array(vec)
        return vec

    def do_L1_norm(self, vec):
        L1_norm = np.linalg.norm(vec, 1)
        return 1.0 * np.array(vec) / L1_norm

    def do_L2_norm(self, vec):
        L2_norm = np.linalg.norm(vec, 2)
        return 1.0 * np.array(vec) / L2_norm


# Bag-of-words
class BoW2Vec(Text2Vec):

    # datafile: the path of bag-of-words vocabulary file
    def __init__(self, datafile, ndims=0, L1_normalize=0, L2_normalize=0):
        Text2Vec.__init__(self, datafile, ndims, L1_normalize, L2_normalize)
        word_vob = map(str.strip, open(datafile).readlines())
        self.word2index = dict(zip(word_vob, range(len(word_vob))))
        if ndims != 0:
            assert len(word_vob) == self.ndims, "feat dimension is not match %d != %d" % (len(word_vob), self.ndims)
        else:
            self.ndims = len(word_vob)
        printStatus(INFO + '.' + self.__class__.__name__, "%d words" % self.ndims)

    def preprocess(self, query):
        return clean_str(query)

    def mapping(self, query):
        words = self.preprocess(query)

        vec = [0.0] * self.ndims
        for word in words:
            if word in self.word2index:
                vec[self.word2index[word]] += 1
            # else:
            #     print word

        if sum(vec) > 0:
            if self.L1_normalize:
                vec = self.do_L1_norm(vec)
            if self.L2_normalize:
                vec = self.do_L2_norm(vec)
            return vec

        ###############################
        # sometimes need to modify
        # else:
        #     return None
        ###############################
        else:
            return vec
