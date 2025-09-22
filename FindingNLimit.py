
'''
В данном файле производилось вычисление максимальной длины числа при которой
время вычисление операции умножения становилось больше 1 секунды.
'''

from LongInt import *
import time
import random

def main():

    M = 10
    N = 10000 # Изначально 10000, чтобы не было переполения

    timeToCalc, val1Dig, val2Dig = 0, [1], [1]

    val2 = LongInt(M, N, 0, 5)

    while (timeToCalc < 1):

        print(N, timeToCalc)
        N = N + 1
        val1 = LongInt(M, N, 0, *val1Dig)

        start = time.time()
        val1 // val2
        timeToCalc = time.time() - start

        val1Dig.append(random.randint(0, M - 1))

    else:
        print(f"При разрядности {N - 10000} вычисление заняло {timeToCalc}")
        timeToCalc,val1Dig,val2Dig = 0, [1], [1]

    return 0

main()
