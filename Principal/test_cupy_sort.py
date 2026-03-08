import cupy as cp
import time
import numpy as np

arr = np.random.randint(0, 50000, 100000).astype(np.int32)
d_arr = cp.asarray(arr)

# Teste 1: Warmup
d_sort = cp.sort(d_arr)
cp.cuda.Stream.null.synchronize()

# Teste 2: Velocidade Real
start = time.time()
d_sort = cp.sort(d_arr)
cp.cuda.Stream.null.synchronize()
gpu_time = time.time() - start

print(f"CUDA CuPy Radix Sort (100k): {gpu_time:.6f} segundos")
print(f"Is GPU faster? Resolveu em {gpu_time*1000:.2f} ms")
