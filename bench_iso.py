import time
import datetime
import timeit

def with_datetime():
    return datetime.datetime.now().isoformat()

def with_strftime():
    return time.strftime("%Y-%m-%dT%H:%M:%S")

t1 = timeit.timeit(with_datetime, number=10000)
t2 = timeit.timeit(with_strftime, number=10000)

print(f"datetime: {t1:.4f}s")
print(f"strftime: {t2:.4f}s")
print(f"Improvement: {(t1-t2)/t1*100:.2f}%")
