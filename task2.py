from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import time


def factorize_single(number):
    # Функція для знаходження дільників одного числа.
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


def factorize(numbers):
    # Функція, що приймає список чисел та повертає список їх дільників.
    return [factorize_single(number) for number in numbers]


def factorize_parallel(numbers):
    # Паралельна версія функції factorize.
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        result = list(executor.map(factorize_single, numbers))
    return result


if __name__ == "__main__":
    start_time = time.time()
    a, b, c, d = factorize([128, 255, 99999, 10651060])
    end_time = time.time()
    print(f"Час виконання синхронної версії: {end_time - start_time} секунд")

    start_time2 = time.time()
    a, b, c, d = factorize_parallel([128, 255, 99999, 10651060])
    end_time2 = time.time()
    print(f"Час виконання паралельної версії: {end_time2 - start_time2} секунд")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [
        1,
        2,
        4,
        5,
        7,
        10,
        14,
        20,
        28,
        35,
        70,
        140,
        76079,
        152158,
        304316,
        380395,
        532553,
        760790,
        1065106,
        1521580,
        2130212,
        2662765,
        5325530,
        10651060,
    ]
