'''
What I learned from Statistics for Business and Finance. 
'''
dict_Z = {.05  : 1.645, 
          .025 : 1.96, 
          .01  : 2.326, 
          .005 : 2.576, 
          .0005: 3.291
         }

def Z(half_alpha):
    half_alpha = round(half_alpha * 1000000) / 1000000
    return dict_Z[half_alpha]

def mean(sample):
    return sum(sample)/len(sample)

def var(sample, fix = True, clever = True):
    sample_mean = mean(sample)
    if clever:
        sum = 0
        for i in sample:
            sum += i**2
        sum -= sample_mean ** 2 * len(sample)
    else:
        sum = 0
        for i in sample:
            sum += (i - sample_mean) ** 2
    if fix:
        return sum / (len(sample) - 1)
    else:
        return sum / len(sample)

def std(*args, **kw):
    return var(*args, **kw) ** .5

def inputList():
    new_list = []
    count = 0
    op = ''
    def takeInput():
        nonlocal op, count
        op = input(str(count) + ': ')
        count += 1
        return op != ''
    while takeInput():
        new_list.append(float(op))
    return new_list

def compare(sample_1, sample_2, confidence = .95):
    assert len(sample_1) >= 30 and len(sample_2) >= 30
    delta = mean(sample_1) - mean(sample_2)
    s = (var(sample_1) / len(sample_1) + var(sample_2) / len(sample_2))**.5
    return confidenceInterval(delta, s, .99, Z)

def confidenceInterval(point_est, deviation, confidence = .95, distribution = Z):
    return (point_est - marginError(deviation, confidence, distribution), \
        point_est + marginError(deviation, confidence, distribution))

def marginError(deviation, confidence = .95, distribution = Z, two_tail = True):
    if two_tail:
        half_alpha = (1 - confidence) / 2
    else:
        half_alpha = (1 - confidence)
    return deviation * distribution(half_alpha)

def regression(x, y):
    '''
    beta_0 is intercept, beta_1 is slope. 
    '''
    x_ = mean(x)
    y_ = mean(y)
    ssxx = sum([(i - x_) ** 2 for i in x])
    ssxy = sum([(i - x_) * (j - y_) for i, j in zip(x, y)])
    # ssyy = sum([(j - y_) ** 2 for j in y])
    beta_1 = ssxy / ssxx
    beta_0 = y_ - beta_1 * x_
    return beta_0, beta_1

def coefficient(x, y):
    x_ = mean(x)
    y_ = mean(y)
    ssxx = sum([(i - x_) ** 2 for i in x])
    ssxy = sum([(i - x_) * (j - y_) for i, j in zip(x, y)])
    ssyy = sum([(j - y_) ** 2 for j in y])
    return ssxy / (ssxx * ssyy) ** .5

if __name__ == '__main__':
    from console import console
    global a
    a = inputList()
    console(globals())
