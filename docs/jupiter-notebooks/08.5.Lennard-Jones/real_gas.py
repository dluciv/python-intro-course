import numba
import matplotlib.pyplot as plt
import numpy
from numpy import array as mkvec
from numpy.linalg import norm

from numba import njit, prange
# prange = range
# def njit(*a, **k):
#     def d(f):
#         return f
#     return d

# ### Определим константы
PARTICLE_EPSILON: float = 1.0e0
PARTICLE_SIGMA  : float = 5.0e0
PARTICLE_MASS   : float = 1.0

MODEL_PRESS_C   : float = 1.0e2
MODEL_PRESS_FALL: float = 0.9

PARTICLE_SAME   : float = 0.01
PARTICLE_FAR    : float = 0.1

PARTICLE_NUMBER : int   = 300

PARTICLE_I_VEL  : float = 5e-3 / PARTICLE_NUMBER

MODEL_DELTA_T   : float = 1e-6
MODEL_TIME_TO   : float = 2e-3

MODEL_STEPS_PER_FRAME : int = 5

@njit(
    # numba.float64(numba.float64),
    fastmath=True, inline='always')
def r_force_lennard_jones(r: float)->float:
    if PARTICLE_SAME <= r <= PARTICLE_FAR:
        return 24.0 * PARTICLE_EPSILON * (PARTICLE_SIGMA**6 / r**7 - 2 * PARTICLE_SIGMA**12 / r**13)
    else:
        return 0.0

@njit(
    # numba.float64(numba.float64),
    fastmath=True, inline='always')
def r_force(r: float)->float:
    if PARTICLE_SAME <= r <= PARTICLE_FAR:
        return PARTICLE_EPSILON * PARTICLE_SIGMA / r**3.5
    else:
        return 0.0


zerovec = mkvec([0.0, 0.0], dtype=float)
zeros = numpy.zeros((PARTICLE_NUMBER, 2), dtype=float)

@njit(
    # numba.float64[:](numba.float64[:], numba.float64[:]),
    fastmath=True, inline='always'
)
def force_induced(to_p, by_p):
    r = norm(to_p - by_p)
    f = r_force(r)
    if f != 0.0:
        return f * (to_p - by_p) / r
    else:
        return zerovec

def init_particles():
    global curr_coordinates, prev_coordinates
    curr_coordinates =  numpy.random.uniform(low=0.0, high=1.0, size=(PARTICLE_NUMBER, 2))
    curr_coordinates *= mkvec([1, 1/3])  # сдвинем все в нижнюю треть стакана
    prev_coordinates =  curr_coordinates +\
        numpy.random.uniform(low=-PARTICLE_I_VEL, high=PARTICLE_I_VEL, size=(PARTICLE_NUMBER, 2))

init_particles()
    
@njit(
    numba.float64[:](numba.int32),
    fastmath=True
)
def particle_velocity(idx: int):
    return (curr_coordinates[idx] - prev_coordinates[idx]) / MODEL_DELTA_T

@njit(
    numba.float64(numba.float64[:,:],numba.float64[:,:]),
    fastmath=True, nogil=True
)
def model_step(cc, pc):
    nc = (2.0 * cc - pc)
    pressure = 0.0

    for i in prange(PARTICLE_NUMBER):
        force_i = zerovec.copy()
        # другие частицы
        for j in range(PARTICLE_NUMBER):
            if j != i:
                force_i += force_induced(cc[i], cc[j])
        nc[i] += force_i / PARTICLE_MASS * MODEL_DELTA_T ** 2 # $a \delta_t^2$

        # от стенок лучше просто отражаться
        for k in range(2):
            if not (0.0 <= nc[i,k] <= 1.0):  # когда вылетели по k-й координате из кастрюли
                if k == 1 and nc[i,k] < 0.0: # отскок от дна
                    pressure += MODEL_PRESS_C * PARTICLE_MASS * (cc[i,k] - nc[i,k])
                nc[i,k], cc[i,k] = cc[i,k], nc[i,k]  # делаем, будто не вылетели, а влетели

    # и так numba не умеет
    # prev_coordinates = curr_coordinates
    # curr_coordinates = next_coordinates
    # и так тоже =)
    # numpy.copyto(prev_coordinates, curr_coordinates)
    # numpy.copyto(curr_coordinates, next_coordinates)
    pc[:] = cc[:]
    cc[:] = nc[:]
    return pressure

import matplotlib.animation as animation
# %matplotlib interactive

fig, ax = plt.subplots()

plt.xlim([0, 1])
plt.ylim([0, 1])


init_particles()
particles, = plt.plot(curr_coordinates[1:,0], curr_coordinates[1:,1], 'b.')
particle0, = plt.plot(curr_coordinates[0, 0], curr_coordinates[0, 1], 'r.')
label = ax.text(0, 0, "Frame: 0")
pressure = 0.0

def animate(frame_no):
    global pressure
    if 0 == frame_no:
        init_particles()
    for _ in range(MODEL_STEPS_PER_FRAME):
        pressure += model_step(curr_coordinates, prev_coordinates)
        pressure *= MODEL_PRESS_FALL
    label.set_text(f"Frame: {frame_no}, P: {pressure}")
    particles.set_data(curr_coordinates[1:,0], curr_coordinates[1:,1])
    particle0.set_data(curr_coordinates[0, 0], curr_coordinates[0, 1])

ma = animation.FuncAnimation(
    fig, animate,
    frames=round(MODEL_TIME_TO / MODEL_DELTA_T),
    interval=50, blit=False, repeat=False
)

plt.show()
ma.save("rg.mp4")
