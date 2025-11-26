'''
扁鹊二技能到底是瞬间治疗强还是被动强？
'''
# INSTA = (100, 20)
# SUSTA = (8, 2)
INSTA = 20
SUSTA = 2
CD = 5

from matplotlib import pyplot as plt

def main():
    insta = 0
    susta = 0
    layer = 0
    iHistory = []
    sHistory = []
    for sec in range(40):
        if sec % CD == 0:
            insta += INSTA
            layer = min(5, layer + 1)
        susta += layer * SUSTA
        iHistory.append(insta)
        sHistory.append(susta)
    plt.plot(iHistory, color='b', label = 'instant')
    plt.plot(sHistory, color='r', label = 'sustain')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Accumulated Heal (% AP)')
    plt.title('BianQue De ErJiNeng DaoDi Shi BeiDong Qiang HaiShi ShunJian ZhiLiao Qiang?')
    plt.legend()
    plt.show()

main()
