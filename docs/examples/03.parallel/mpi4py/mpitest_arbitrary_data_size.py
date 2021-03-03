#!/usr/bin/env python3

from mpi4py import MPI
import math
import itertools

comm = MPI.COMM_WORLD
cluster_size = comm.Get_size()
process_rank = comm.Get_rank()


def slow_function(arg_list):
    return [-a * process_rank for a in arg_list]

if process_rank == 0:
    # Пусть у нас есть сколько-то данных, которые нам надо обработать независимо от того, сколько процессов считает
    data_size = 100
    source_data = [1] * data_size

    # Но их надо раскидать по cluster_size процессам, примерно равномерно
    root_args = [ source_data[round(rank * data_size / cluster_size) : round((rank + 1) * data_size / cluster_size) ] for rank in range(cluster_size) ]
else:
    root_args = None

# Взять исходные данные root_args у 0-го, раскидать по всем процессам
local_args = comm.scatter(root_args, root=0)

# У всех вызвать функцию от данных
local_response = slow_function(local_args)

# Собрать у всех и отдать в root_response 0-му
root_response = comm.gather(local_response, root=0)

if process_rank == 0:
    result = list(itertools.chain.from_iterable(root_response))
    print(result)
