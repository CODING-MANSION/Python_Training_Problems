def check_vowels(sentence,vowels):
    sentence = [x.upper() for x in sentence]
    vow2 = [i for i in sentence if i in vowels]
    return vow2
def count(sentence):
    temp=[sentence.count(x) for x in set(sentence)]
    return temp




if __name__ == '__main__':
    vowels='aeiouAEIOU'
    sentence=input()
    new_Sent = check_vowels(sentence, vowels)
    print("vowels in sentence-[%s]"%(', '.join(map(str, set(new_Sent)))))


    print(f'Each vowel repeated as-{count(new_Sent)} (request with vowel)')

