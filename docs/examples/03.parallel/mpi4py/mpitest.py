#!/usr/bin/env python3

from mpi4py import MPI
import math

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def slow_function(arg):
    return math.sin(arg) * rank

if rank == 0:
    root_args = list(range(size))
else:
    root_args = None

# Взять исходные данные root_args у 0-го, раскидать по всем процессам
local_args = comm.scatter(root_args, root=0)

# У всех вызвать функцию от данных
local_response = slow_function(local_args)

# Собрать у всех и отдать в root_response 0-му
root_response = comm.gather(local_response, root=0)

if rank == 0:
    print(rank, root_response)
