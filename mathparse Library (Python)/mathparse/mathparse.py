import mathnotations

notations = mathnotations.word_notations()

def parse (expression):
    number_word = notations['numbers']
    for word in number_word.keys():
        if word in expression:
            expression = expression.replace(word, str(number_word[word]))

    print (expression)

parse ('one hundred and twenty five')