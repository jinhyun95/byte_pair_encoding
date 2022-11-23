import json
import nltk
from nltk.corpus import nps_chat

nltk.download('nps_chat')

VOCAB_SIZE = 1000

vocabulary = dict()
plain_texts = []
fids = nps_chat.fileids()
for fid in fids:
    posts = nps_chat.posts(fid)
    for post in posts:
        plain_texts.append(list(' '.join(post).lower()))

# vocabulary initialization
for text in plain_texts:
    for letter in text:
        if letter not in vocabulary:
            vocabulary[letter] = len(vocabulary)

encoded_texts = []
for text in plain_texts:
    encoded_texts.append([vocabulary[x] for x in text])

# bigram initialization
bigram_counts = dict()
for i in range(len(encoded_texts)):
    for j in range(len(encoded_texts[i]) - 1):
        bigram = (encoded_texts[i][j], encoded_texts[i][j + 1])
        if bigram in bigram_counts.keys():
            bigram_counts[bigram] = bigram_counts[bigram] + 1
        else:
            bigram_counts[bigram] = 1

# make dictionary
while len(vocabulary) < VOCAB_SIZE:
    merged = max(list(bigram_counts.keys()), key=lambda x: bigram_counts[x])
    vocabulary[merged] = len(vocabulary)
    for i in range(len(encoded_texts)):
        j = 0
        while j < len(encoded_texts[i]) - 1:
            if (encoded_texts[i][j], encoded_texts[i][j + 1]) == merged:
                if j > 0:
                    bigram_counts[(encoded_texts[i][j - 1], encoded_texts[i][j])] = bigram_counts[(encoded_texts[i][j - 1], encoded_texts[i][j])] - 1
                    if (encoded_texts[i][j - 1], vocabulary[merged]) in bigram_counts.keys():
                        bigram_counts[(encoded_texts[i][j - 1], vocabulary[merged])] = bigram_counts[(encoded_texts[i][j - 1], vocabulary[merged])] + 1
                    else:
                        bigram_counts[(encoded_texts[i][j - 1], vocabulary[merged])] = 1
                if j < len(encoded_texts[i]) - 2:
                    bigram_counts[(encoded_texts[i][j + 1], encoded_texts[i][j + 2])] = bigram_counts[(encoded_texts[i][j + 1], encoded_texts[i][j + 2])] - 1
                    if (vocabulary[merged], encoded_texts[i][j + 2]) in bigram_counts.keys():
                        bigram_counts[(vocabulary[merged], encoded_texts[i][j + 2])] = bigram_counts[(vocabulary[merged], encoded_texts[i][j + 2])] + 1
                    else:
                        bigram_counts[(vocabulary[merged], encoded_texts[i][j + 2])] = 1
                encoded_texts[i][j] = vocabulary[merged]
                del encoded_texts[i][j + 1]
            j += 1
    del bigram_counts[merged]

with open('vocabulary.json', 'w') as f:
    json.dump({str(x): vocabulary[x] for x in vocabulary.keys()}, f)