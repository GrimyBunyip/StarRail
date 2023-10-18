length = 512000
width = 6
out_size = 256

l = [[i for _ in range(width)] for i in range(length)]

mins = [min([row[i] for row in l]) for i in range(width)]
maxs = [max([row[i] for row in l]) for i in range(width)]

input_list = [
                [(entry - mins[i]) / (maxs[i] - mins[i]) for i, entry in enumerate(l[0])],
                [(entry - mins[i]) / (maxs[i] - mins[i]) for i, entry in enumerate(l[-1])],
             ]

import time
start_time = time.perf_counter()
target_list = [
                [
                    (entry - mins[col]) / (maxs[col] - mins[col])
                    for col, entry in enumerate(l[int(row * len(l) / out_size)])
                ]
                for row in range(out_size)
              ]
elapsed_time = time.perf_counter() - start_time

print(elapsed_time)

start_time = time.perf_counter()
target_list = [l[int(row * len(l) / out_size)] for row in range(out_size)]
target_list = [ [(entry - mins[col]) / (maxs[col] - mins[col]) for col, entry in enumerate(row)] for row in target_list]
elapsed_time = time.perf_counter() - start_time

print(elapsed_time)