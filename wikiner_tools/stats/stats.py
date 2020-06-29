import argparse
import pdb
import string

from torch.utils.data import DataLoader, Dataset


class WikiNerCoNLL(Dataset):

    def __init__(self, path):
        """Class for statistics on WikiNER

        Args:
            path (str): format '/path/to/wikiner/wikiner[<lang id>].conll' (e.g. ../wikiner_conll/it/wikinerIT.conll)
        """
        self.words = []
        self.targets = []
        self.sentences = []

        self.readfile(path, 'train')
        self.readfile(path, 'val')
        self.readfile(path, 'test')
        assert len(self.words) == len(self.targets)

    def readfile(self, path, datatype='train'):
        fp = open('{}.{}'.format(path, datatype))
        self.sentences.append([])
        for line in fp:
            if line == '' or line == '\n':
                if line == '\n':
                    self.sentences.append([])
                continue

            self.words.append(line.split()[0])
            self.targets.append(line.split()[1])
            self.sentences[-1].append(self.words[-1])

    def __getitem__(self, index):
        t = self.targets[index]
        if len(t) > 3 and t != 'MISC':
            t = t[2:]
        return self.words[index], t

    def __len__(self):
        return len(self.words)



if __name__ == '__main__':
    """Example
        python stats.py --data ../wikiner_conll/it/wikinerIT.conll
    """
    parser = argparse.ArgumentParser()


    parser.add_argument(
        '--data',
        default=None,
        type=str,
        required=True,
        help='Path to wikiner in conll format folder'
    )

    args = parser.parse_args()

    dataset = WikiNerCoNLL(args.data)
    loader = DataLoader(dataset)
    
    # stats data structures
    unique_words = set()
    num_entities_per_type = {'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0, 'O': 0}
    for (word, target) in loader:
        w = word[0]
        t = target[0]

        num_entities_per_type[t] += 1
        if w not in string.punctuation:
            unique_words.add(word)

    accum = 0
    for s in dataset.sentences:
        accum += len(s)
    average_sentence_len = accum/len(dataset.sentences)

    print('Unique words: {}'.format(len(unique_words)))
    print('Number of entities per type: {}'.format(num_entities_per_type))
    print('Number of sentences: {}'.format(len(dataset.sentences)))
    print('Average sentence length: {}'.format(round(average_sentence_len, 2)))
