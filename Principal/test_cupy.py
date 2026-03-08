import cupy as cp
import time
import numpy as np

# Kernel CUDA em C++ puro compilado em Runtime via NVRTC!
odd_even_kernel = cp.RawKernel(r'''
extern "C" __global__
void odd_even_step(int* arr, int n, int phase) {
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    if (phase == 0) {
        if (idx % 2 == 0 && idx < n - 1) {
            if (arr[idx] > arr[idx + 1]) {
                int temp = arr[idx];
                arr[idx] = arr[idx + 1];
                arr[idx + 1] = temp;
            }
        }
    } else {
        if (idx % 2 != 0 && idx < n - 1) {
            if (arr[idx] > arr[idx + 1]) {
                int temp = arr[idx];
                arr[idx] = arr[idx + 1];
                arr[idx + 1] = temp;
            }
        }
    }
}
''', 'odd_even_step')

def bubble_sort_gpu(arr_cpu):
    n = len(arr_cpu)
    d_arr = cp.asarray(arr_cpu)
    threads_per_block = 256
    blocks_per_grid = (n + threads_per_block - 1) // threads_per_block
    
    for i in range(n):
        odd_even_kernel((blocks_per_grid,), (threads_per_block,), (d_arr, n, i % 2))
        
    cp.cuda.Stream.null.synchronize()
    return cp.asnumpy(d_arr)

print("Testando NVRTC Runtime C++ CUDA via CuPy...")
arr = np.random.randint(0, 50000, 10000).astype(np.int32)
start = time.time()
res = bubble_sort_gpu(arr)
print("Odd-Even NVRTC GPU (10k):", time.time() - start)
print("Verificando se ordenou corretamente:", np.array_equal(res, np.sort(arr)))

start = time.time()
d_arr = cp.asarray(arr)
res2 = cp.sort(d_arr)
cp.cuda.Stream.null.synchronize()
print("CuPy Native Sort GPU (10k):", time.time() - start)
