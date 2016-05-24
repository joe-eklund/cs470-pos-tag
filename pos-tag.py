import random
import sys

class BiGram:

    wordMap = {}
    debug = True

    def __init__(self, source):
        previous = None
        with open(source, 'r') as f:
            for line in f:
                for word in line.split():
                    current = word.rpartition('_')[0]
                    if previous is not None:
                        if previous in self.wordMap.keys() is not None:
                            if current in self.wordMap[previous].keys() is not None:
                                self.wordMap[previous][current] += 1
                            else:
                                self.wordMap[previous][current] = 1
                        else:
                            self.wordMap[previous] = {current : 1}
                    previous = current

    '''
    This iterates through our wordmap. For each key it pulls out the associated map for that key. 
    We then iterate through our inner map and normalize our counts by dividing the current counts by the length of the inner map.
    '''
    def normalize_word_map(self):
        #Outer map.
        for key, values in self.wordMap.iteritems():
            #Inner Map
            for word_succeed, count in values.iteritems():
                #Normalize counts & cast to floats
                count = float(count) / float(sum(values.itervalues()))
                values[word_succeed] = count   

    def generate_given(self, keyword, length):
        sys.stdout.write(keyword + " ")
        if keyword in self.wordMap:
            while(length > 0):
                ran = random.random()
                #Still need to use random variable to select next word. Currently just grabs the next word in map.
                next_word = self.WeightedPick(self.wordMap[keyword])
                keyword = next_word
                sys.stdout.write(keyword + " ")
                length -= 1
                if length % 10 == 0:
                    sys.stdout.write("\n")

    def WeightedPick(self, d):
        r = random.uniform(0, sum(d.itervalues()))
        s = 0.0
        for k, w in d.iteritems():
            s += w
            if r < s: return k
        return k

if __name__ == '__main__':
    # Initialize GUI
    source = "training_dataset_small.txt"
    biGram = BiGram(source)
    #biGram.normalize_word_map()
    biGram.generate_given("In", 50)