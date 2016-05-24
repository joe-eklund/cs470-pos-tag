class BiGram:

    wordMap = {}

    def __init__(self, source):
        previous = None
        with open(source, 'r') as f:
            for line in f:
                for word in line.split():
                    current = word.rpartition('_')[0]
                    #print current
                    if previous is not None:
                        if previous in self.wordMap.keys() is not None:
                            if current in self.wordMap[previous].keys() is not None:
                                self.wordMap[previous][current] += 1
                            else:
                                self.wordMap[previous][current] = 1
                        else:
                            self.wordMap[previous] = {current : 1}
                    previous = current

if __name__ == '__main__':
    # Initialize GUI
    source = "training_dataset.txt"
    biGram = BiGram(source)