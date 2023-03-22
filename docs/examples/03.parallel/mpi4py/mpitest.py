#!/usr/bin/env python3

from mpi4py import MPI
import math
import time

comm = MPI.COMM_WORLD
cluster_size = comm.Get_size()
process_rank = comm.Get_rank()

def slow_function(arg):
    s = 0.0
    for i in range(3_000_000):
        s += math.sin(i*arg) * process_rank
    return s

if process_rank == 0:
    root_args = list(range(cluster_size))
else:
    root_args = None

# Взять исходные данные root_args у 0-го, раскидать по всем процессам
local_args = comm.scatter(root_args, root=0)

# У всех вызвать функцию от данных
t0 = time.time()
local_response = slow_function(local_args)
t1 = time.time()

# Собрать у всех и отдать в root_response 0-му
root_response = comm.gather(local_response, root=0)

if process_rank == 0:
    print("Time spent:", t1 - t0)
    print(root_response)
