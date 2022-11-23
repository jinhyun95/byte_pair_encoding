
import json

encoded = [316, 117, 189, 690, 13, 288, 195, 333, 38, 70, 262, 9, 827, 127, 37, 569, 116, 164, 32, 99, 207, 401, 164, 32, 99, 109]

with open('vocabulary.json', 'r') as f:
    vocabulary = json.load(f)
keys = list(vocabulary.keys())
for k in keys:
    if len(k) > 1:
        vocabulary[(int(k.split(',')[0][1:]), int(k.split(',')[1][:-1]))] = vocabulary[k]
        del vocabulary[k]
vocabulary = {vocabulary[x]: x for x in vocabulary.keys()}

for i in list(range(len(vocabulary)))[::-1]:
    new_encoded = []
    for token in encoded:
        if token == i:
            if isinstance(vocabulary[token], tuple):
                new_encoded.extend(list(vocabulary[token]))
            else:
                new_encoded.append(vocabulary[token])
        else:
            new_encoded.append(token)
    encoded = new_encoded
print(''.join(new_encoded))
