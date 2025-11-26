def kthSkipPositive(arr, k):
    # 自然数问题 比 正整数问题 更好写，因此化归一下
    return kthSkipNatural([0] + arr, k)

def kthSkipNatural(arr, k):
    i = recur(arr, k, 0, len(arr))
    n_skipped = arr[i] - i
    more_to_skip = k - n_skipped
    return arr[i] + more_to_skip

def recur(arr, k, start, end):
    # Binary search, return index
    if start == end:
        return start
    mid = int((start + end) / 2)
    mid_value = arr[mid]
    n_skipped = mid_value - mid
    if n_skipped < k:
        if start == mid:
            return mid
        else:
            return recur(arr, k, mid, end)
    else:
        return recur(arr, k, start, mid)

def test():
    print(kthSkipPositive([2,3,4,7,11], 5))
    print(kthSkipPositive([1,2,3,4], 2))
    print(kthSkipPositive([5,6,7], 2))

test()
