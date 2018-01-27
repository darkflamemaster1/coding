'''
2D cellular automata that uses modular reduction as a rule. The rules can be specified
manually in the loop though. 
'''


import argparse
import os
import time
import numpy as np
from array import array
import matplotlib

try:
    matplotlib.use('Qt5Agg')
except ValueError as e:
    print('Error: matplotlib backend\n', e)
    print('Trying:', matplotlib.get_backend())
    matplotlib.use(matplotlib.get_backend())
finally:
    import matplotlib.pyplot as plt

from collections import namedtuple
import matplotlib.animation as animation
import numpy as np

Writer = animation.writers['ffmpeg']
writer = Writer(fps=5, bitrate=-1, codec="libx264")


hex_n = lambda t, r, c: [(t, r + 1, c - 1), (t, r + 1, c),
                              (t, r, c - 1), (t, r, c + 1),
                              (t, r - 1, c), (t, r - 1, c + 1)
                              ]

moore_n = lambda t, r, c: [(t, r + 1, c - 1), (t, r + 1, c), (t, r + 1, c + 1),
                                (t, r, c - 1), (t, r, c + 1),
                                (t, r - 1, c - 1), (t, r - 1, c), (t, r - 1, c + 1)
                                ]

nuemann_n = lambda t, r, c: [(t, r + 1, c),
                                  (t, r, c - 1), (t, r, c + 1),
                                  (t, r - 1, c)
                                  ]

Neigborhood =  { "hex": hex_n,
                 "moore" : moore_n,
                 "nuemann": nuemann_n
                 }


def do_fft(X,n):
    from scipy.fftpack import fft
    print("WTF")
    N = len(X)
    T = 1.0 / n
    x = np.linspace(0.0, N * T, N)
    yf = fft(X)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    plt.figure()
    plt.plot(X)

    plt.figure()
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
    plt.grid()
    plt.show()



def main(args):
    W =args.grid
    T = args.steps
    n = args.rule
    eps = args.eps
    Nx = Neigborhood[args.neighborhood]
    D = array("i", [0]*T)

    M = np.zeros((3, W, W), 'int8')
    # M = np.random.randint(0, 2, (W, W,T),'int8')
    M[0, W // 2, W // 2] = 1

    fig, ax = plt.subplots()
    fig.set_size_inches(4, 4, True)

    t0 = time.time()


    import matplotlib as mpl
    cmap = mpl.cm.jet
    cmap.set_over((1., 0., 0.))
    cmap.set_under((0., 0., 1.))
    bounds = list(x for x in range(0, n + 1))
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


    def steps(t):
        tn = t
        t = t % 3
        dt = 2 if not t else t - 1
        for r in range(1, W-1):
            for c in range(1, W-1):
                M[t, r, c] = (np.sum([M[x] for x in Nx(dt,r,c)])) % n


                # Instead of using a lambda function, its faster to just define them

                # ---- von Nuemann neighhborhood ----
                # M[t, r, c] = (M[dt, r, c + 1] + M[dt, r, c - 1] + M[dt, r + 1, c] + M[dt, r - 1, c] + M[dt,r,c]) % n

                # ---- Moore neighborhood ----
                # M[t, r, c] = (np.sum(M[dt, r - 1:r + 2, c - 1:c + 2]) - M[dt,r,c] ) % n

        D[tn] = np.sum(M[t, :, :])
        return M[t, :, :]

    im = ax.imshow(steps(1), cmap='jet', animated=True,clim=(0,n))
    print("Using %s neighborhood" % args.neighborhood)
    # fig.colorbar(im, ax=ax, norm=norm, ticks=bounds[0:-1],spacing='proportional',boundaries=bounds)

    def update_plot(i):
        im.set_array(steps(i))
        input()
        if i == T-1:
            print(("t=%d: %s seconds " % (i, time.time() - t0)))
        return im


    anim = animation.FuncAnimation(fig, update_plot, np.arange(1, T), repeat=False, blit=False,interval=1)
    plt.axis('off')
    plt.tight_layout()
    # anim.save('Moore.mp4', writer=writer)
    plt.show()
    # do_fft(D,n)
    return

if __name__ == '__main__':
    mod = 16
    grid = 200
    step = 150
    eps = 1
    Arguments = namedtuple('arg', 'rule neighborhood steps grid eps')
    parser = argparse.ArgumentParser(
        description='Two-dimensional cellular automata.')

    parser.add_argument('-r', '--rule', type=int, default=mod,
                        help='modular reduction rule: default = %s' % mod)

    parser.add_argument('-n', '--neighborhood', type=str, default='moore',
                        help='Moore or von Neumann neighborhood, default = moore')

    parser.add_argument('-s', '--steps', type=int, default=step,
                        help='time steps: default = %s' % step)

    parser.add_argument('-g', '--grid', type=int, default=grid,
                        help='grid size: default = %s' % grid)

    parser.add_argument('-e', '--eps', type=int, default=eps,
                        help='epsilon neighborhood radius: default = %s' % eps)
    a = parser.parse_args()
    main(Arguments(**vars(a)))
