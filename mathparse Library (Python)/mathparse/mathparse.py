import mathnotations
import re

notations = mathnotations.word_notations()

def parse (expression):
    number_word = notations['numbers']
    for word in number_word.keys():
        if word in expression:
            expression = expression.replace(word, str(number_word[word]))

    print (expression)



def number_formation():
    numbers = [1,1000,200,20,5]
    if len(numbers) == 4:
        print ((numbers[0] * numbers[1]) + numbers[2] + numbers[3])
    elif len(numbers) == 3:
        print (numbers[0] * numbers[1] + numbers[2])
    elif len(numbers) == 2:
        if 100 in numbers:
            print ( numbers[0] * numbers[1])
        else:
            print (numbers[0] + numbers[1])
    else:
        print (numbers[0])


def find_word_groups(string, words):
    """
    Find matches for words in the format "3 thousand 6 hundred 2".
    The words parameter should be the list of words to check for
    such as "hundred".
    """
    scale_pattern = '|'.join(words)
    # For example:
    # (?:(?:\d+)\s+(?:hundred|thousand)*\s*)+(?:\d+|hundred|thousand)+
    print (scale_pattern)
    regex = re.compile(
        r'(?:(?:\d+)\s+(?:' +
        scale_pattern +
        r')*\s*)+(?:\d+|' +
        scale_pattern + r')+'
    )
    print (regex)
    result = regex.findall(string)
    print (result)
    print (string)
    return result

parse ('one hundred and twenty five')
number_formation()
print (find_word_groups('one hundred and twenty five', list(notations['scales'].keys())))


