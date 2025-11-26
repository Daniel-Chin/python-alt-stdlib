features = None
feature_length = None
train = None
test = None

def spread():
    global train, test
    with open("spam_train.txt","r") as f:
        spam_train = [x.strip() for x in f.readlines()]
    spam_train.pop(4682) # important: from big to small
    spam_train.pop(4184)
    spam_train.pop(1107)
    with open("spam_test.txt","r") as f:
        spam_test = [x.strip() for x in f.readlines()]
    options = {
        'v': 'train = spam_train[1000 : 1000 + N];   test = spam_train[:1000]', 
        't': 'train = spam_train[:N];                test = spam_test', 
    }
    fullname = {'v': 'validation mode', 't': 'testing mode   '}
    print()
    print('We have two raw files: spam_train (%d) and spam_test (%d).' % (len(spam_train), len(spam_test)))
    print('How do you want to extract samples from them?')
    for mode, code in options.items():
        print(' *', fullname[mode], ':', code)
    inp = ''
    while inp not in options.keys():
        inp = input(f'Type {"/".join(options.keys())} >>')
    code = options[inp]
    print()
    print('This will be run: ')
    print(code)
    N = int(input('please specify N = '))
    codes = [line.split(' = ')[1] for line in code.replace('N', str(N)).split(';')]
    train, test = eval(codes[0]), eval(codes[1])
    train = parseEmail(train)
    print('training data', len(train), 'emails')
    test = parseEmail(test)
    print('testing data', len(test), 'emails')

def parseEmail(str_emails):
    emails = []
    for str_email in str_emails:
        emails.append(str_email.split(' '))
    return emails

def findHighWords(X):
    stats = {}
    for email in train:
        word_set = set(email) - {'0', '1'}
        for word in word_set:
            stats[word] = stats.get(word, 0) + 1
            # If exist, +1. If not, =1. 
    high_words = []
    for word, appearance in stats.items():
        if appearance >= X:
            high_words.append(word)
    return high_words

''' ####################################################### '''
def feature_data(email):
    vector = []
    for word in features:
        if word in email:
            vector.append(1)
        else:
            vector.append(0)
    return vector

def vectorizeEmails(emails):
    vector = []
    total = len(emails)
    for i, email in enumerate(emails):
        if email[0] == '1':
            is_spam = 1
        else:
            is_spam = -1
        print('Vectorizing email', i, '/', total, '...', end = '\r', flush = True)
        vector.append(feature_data(email) + [is_spam])
    print('All emails vectorized.', ' ' * 10)
    return vector

def predict(vector_email, w):
    tem = 0
    for j in range(feature_length):
        tem += w[j] * vector_email[j]
    return tem

def perceptron_train(iter_max):
    vector_emails = vectorizeEmails(train)
    w = [0] * feature_length
    k = 0
    iteration = 0
    while iter_max == 0 or iteration < iter_max:
        iteration += 1
        print('iteration', iteration, '...', end = '\r', flush = True)
        mark = 0
        for vector_email in vector_emails:
            score = vector_email[-1] * predict(vector_email, w)
            if score <= 0:
                for j in range(feature_length):
                    w[j] += vector_email[-1] * vector_email[j]
                mark += 1
        print('iteration', iteration, end = ' ')
        if mark == 0:
            print('result: good. mark = 0')
            break
        else:
            print('result: not so good. mark =', mark)
            k += mark
    return w, k, iteration

def perceptron_error(w, tester):
    mark = 0
    vector_emails = vectorizeEmails(tester)
    print('Testing predictions...', end = '\r', flush = True)
    for vector_email in vector_emails:
        if predict(vector_email, w) * vector_email[-1] <= 0:
            mark += 1
    error = mark / len(vector_emails)
    return error

def common_words(w):
    dic = dict(zip(features, w))
    tem_w = w
    tem_w.sort()
    lst_max = [x for x in features if dic[x] >= tem_w[-12]]
    lst_min = [x for x in features if dic[x] <= tem_w[11]]
    print('the list of the words with the most positive weights is', lst_max)
    print('the list of the words with the most negative weights is', lst_min)

def main():
    global features, feature_length
    prompt, default = 'please input the number determine the feature of data = ', '26'
    print(prompt + default, end = '\r')
    X = int(input(prompt).strip() or default)
    spread()
    print('Selecting features...', end = '\r', flush = True)
    features = findHighWords(X)
    feature_length = len(features)
    print('feature_length =', feature_length, ' ' * 10)
    prompt, default = "please enter the control number of the iteration. Enter 0 to release control = ", '30'
    print(prompt + default, end = '\r')
    iter_max = int(input(prompt).strip() or default)
    print('Traning starts.')
    w, k, iter = perceptron_train(iter_max)
    print('the total update number is', k)
    print('the total iteration is', iter)
    training_error = perceptron_error(w, train)
    print('the perceptron error of training data is',training_error)
    validation_error = perceptron_error(w, test)
    print('the perceptron error of validation/test data is', validation_error)
    common_words(w)

main()
