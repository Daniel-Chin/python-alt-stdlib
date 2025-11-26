from matplotlib import pyplot as plt

def f(w):
    return w**2, 2 * w

def cosineSimilarity(a, b):
    # 1D case
    if a * b > 0:
        return 1
    elif a * b < 0:
        return -1
    else:
        return 0

def main():
    w = 50
    last_grad = 0
    lr = 1
    W = []
    for i in range(40):
        W.append(w)
        # print(f'{w=}')
        loss, grad = f(w)
        # print(f'{grad=}')
        lr *= (cosineSimilarity(last_grad, grad) + 1) * .5 + .1
        # print(f'{lr=}')
        last_grad = grad
        w += (- grad / abs(grad)) * lr
    plt.plot(W)
    plt.ylabel('w')
    plt.xlabel('t')
    plt.show()

main()
