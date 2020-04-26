#!/usr/bin/env python3

import numpy as np
import model

if __name__ == '__main__':
    sur = model.Surface("surface_heights.csv", 2000.0)

    import matplotlib.pyplot as plt
    xs = np.arange(0.0, sur.get_width())
    plt.plot(xs, [sur.get_height(x) for x in xs])
    plt.show()
