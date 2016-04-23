def pregraph(dic, var):
    import numpy as np
    inf = []
    for i in range(0, len(dic['X'])):
        inf.append([dic['X'][i], dic[var][i]])
    inf = np.array(inf)

    return(inf)


def g2f(n, name):

    import numpy as np

    np.savetxt(name, n, delimiter=',')


def x2f(loc):
    r = exdat()
    w2f(r, loc+'.csv')
    p = pregraph(r, 'AP')
    g2f(p, loc+'.csv')
    return(p)


def graph(files, name):
    import itertools
    marker = itertools.cycle(('-.', ':', '-', '--'))
    import pylab
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.ticker as plticker
    matplotlib.rcParams['font.family'] = 'sans-serif'
    list_of_files = [(v, c, marker.next(), ' ') for v, c in files]
    datalist = [(data, label, ls, mk) for data, label, ls, mk in list_of_files]
    fig, ax = plt.subplots()
    for data, label, ls, mk in datalist:
        ax.plot(data[:, 0], data[:, 1], label=label, ls=ls, lw=3, marker=mk)
    font = {'family': 'sans-serif', 'size': 20}
    matplotlib.rc('font', **font)
    plt.legend(loc=2, prop={'size': 20}, ncol=2, frameon=False)
    loc = plticker.MultipleLocator(base=10)
    # this locator puts ticks at regular intervals

    ax.xaxis.set_major_locator(loc)
    pylab.xlabel("distance from nostrils (mm)")
    pylab.ylabel("area/(perimeter length) (mm)")
    plt.axis([0, 70, 0, 2e-3])
    plt.tight_layout()
    pylab.savefig(name)


def mcvol():
    dics = ['04', '05', '6', '7']
    from numpy import genfromtxt
    arr = {}
    al = []

    for dic in dics:
        y = genfromtxt(dic+".csv", delimiter=",")
        xi = y[:, 1]
        v1 = 0
        m1 = 5000
        v2 = 0
        m2 = 5000

        for x in range(len(xi)):
            if y[x, 0] < 20:

                v1 = v1 + ((y[x, 1]+y[x+1, 1])/2)*(y[x+1, 0]-y[x, 0])*1000
                if y[x, 1]*10000 < m1:
                    m1 = y[x, 1]*10000

            elif 20 <= y[x, 0] <= 50:

                v2 = v2 + ((y[x-1, 1]+y[x, 1])/2)*(y[x, 0]-y[x-1, 0])*1000
                if y[x, 1]*10000 < m2:
                    m2 = y[x, 1]*10000
        arr[dic] = [v1, m1, v2, m2]
        al.append(arr[dic])
    arr['list'] = al

    return(arr)


def totable(arra):
    array = [[], [], [], []]
    for cou in range(0, len(arra)):
        for nt in range(0, len(arra[cou])):
            array[cou].append("%.2f" % arra[cou][nt])

    l = ['NC04', 'NC05', 'NC06', 'NC07']
    for r in range(0, 4):
        array[r].insert(0, l[r])
    l1 = [['', 'vol1', 'MCA1', 'vol2', 'MCA2']]

    for ll in array:
        l1.append(ll)

    ln = np.asarray(l1)
    la = ln.transpose()

    np.savetxt("mydata.csv", la, delimiter=' & ', fmt='%s', newline=' \\\\\n')

    return(la)


def a4p():

    import numpy as np
    r = ['04', '05', '6', '7']
    le = []
    for l in r:
        ll = np.genfromtxt(l+'rtot.csv', delimiter=",")

        lll = np.append([ll[:, 0]], [np.multiply(ll[:, 3], 1/(4*ll[:, 1]))], axis=0)  # NOQA
        le.append((lll.transpose(), l))

    return(le)


def ap2():

    import numpy as np
    r = ['04', '05', '6', '7']
    le = []
    for l in r:
        ll = np.genfromtxt(l+'rtot.csv', delimiter=",")

        lll = np.append([ll[:, 0]], [np.multiply(ll[:, 3], 1/(ll[:, 1]**2))], axis=0)  # NOQA
        le.append((lll.transpose(), l))

    return(le)


def comb():

    import numpy as np
    r = ['04', '05', '6', '7']
    le = {}
    for l in r:
        ll = np.genfromtxt(l+'ltot.csv', delimiter=",")[:, 0]
        lll = np.append([ll[:, 0]], [np.multiply(ll[:, 3], 1/(4*ll[:, 1]))], axis=0)  # NOQA
        le[l] = lll.transpose()
        np.savetxt(l+'.csv', le[l], delimiter=",")
    return(le)
