import time
import datetime
import timeit

def with_datetime():
    return datetime.datetime.now().isoformat()

def with_strftime_precision():
    t = time.time()
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t)) + ".%03d" % (t % 1 * 1000)

t1 = timeit.timeit(with_datetime, number=10000)
t2 = timeit.timeit(with_strftime_precision, number=10000)

print(f"datetime: {t1:.4f}s")
print(f"strftime+precision: {t2:.4f}s")
print(f"Improvement: {(t1-t2)/t1*100:.2f}%")
