from collections import Counter, defaultdict

class BPETokenizer:
    def __init__(self, num_merges=100):
        self.num_merges = num_merges
        self.vocab = None
        self.merges = []
    
    def get_vocab(self, corpus):
        """
        make the vocab from input corpus where we just split words and add a end of word marker
        """
        vocab = Counter()
        for word in corpus.split():
            tokens = list(word) + ['</w>']
            vocab[tuple(tokens)] += 1
        return vocab
    
    def get_stats(self, vocab):
        """
        count the frequency of adjacent tokens
        """
        pairs = defaultdict(int)
        for word, freq in vocab.items():
            symbols = word
            for i in range(len(symbols)-1):
                pair = (symbols[i], symbols[i+1])
                pairs[pair] += freq
        return pairs
    
    def merge_vocab(self, pair, vocab):
        """
        merge most frequent pair in vocab
        """
        new_vocab = {}
        bigram = ' '.join(pair)
        replacement = ''.join(pair)
        
        for word, freq in vocab.items():
            word_str = ' '.join(word)
            new_word_str = word_str.replace(bigram, replacement)
            new_word = tuple(new_word_str.split(' '))
            new_vocab[new_word] = freq
        return new_vocab
    
    def fit(self, corpus):
        """
        store merges
        """
        vocab = self.get_vocab(corpus)
        for i in range(self.num_merges):
            pairs = self.get_stats(vocab)
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            vocab = self.merge_vocab(best, vocab)
            self.merges.append(best)
        self.vocab = vocab
    
    def tokenize(self, text):
        """
        tokenize the new text using merges
        """
        words = text.split()
        output = []
        for word in words:
            tokens = list(word) + ['</w>']
            tokens = self.apply_merges(tokens)
            output.extend(tokens)
        return output
    
    def apply_merges(self, tokens):
        tokens = tokens[:]
        while True:
            pairs = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
            merge_candidates = [pair for pair in pairs if pair in self.merges]
            if not merge_candidates:
                break
            
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens)-1 and (tokens[i], tokens[i+1]) in merge_candidates:
                    pair = (tokens[i], tokens[i+1])
                    new_tokens.append(tokens[i] + tokens[i+1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
        return tokens


tokenizer = BPETokenizer(num_merges=50)
tokenizer.fit("low lower lowest lower lowest newest widest widest newer high highest higher height")

print(tokenizer.merges)
print("lowest --> ", tokenizer.tokenize("lowest"))
print("newest --> ", tokenizer.tokenize("newest"))
