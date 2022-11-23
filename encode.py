import json

text = 'this is an example text for testing bpe encoding and decoding!!'

with open('vocabulary.json', 'r') as f:
    vocabulary = json.load(f)
keys = list(vocabulary.keys())
for k in keys:
    if len(k) > 1:
        vocabulary[(int(k.split(',')[0][1:]), int(k.split(',')[1][:-1]))] = vocabulary[k]
        del vocabulary[k]

encoded = list(text)
for token in sorted(list(vocabulary.keys()), key=lambda x: vocabulary[x]):
    if isinstance(token, tuple):
        i = 0
        while i < len(encoded) - 1:
            if token == (encoded[i], encoded[i + 1]):
                encoded[i] = vocabulary[token]
                del encoded[i + 1]
            i += 1
    else:
        for i in range(len(encoded)):
            if encoded[i] == token:
                encoded[i] = vocabulary[token]
print(encoded)