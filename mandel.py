import sys
import time

def norm(c):
    return c.real * c.real + c.imag * c.imag

def mandelbrot(width, height, bitmap):
    max_iterations = 50
    limit = 4
    for y in range(height):
        for x in range(width):
            Z = complex(0, 0)
            C = complex(2 * x / width - 1.5, 2 * y / height - 1.0)

            i = 0
            while i < max_iterations and norm(Z) <= limit:
                Z = Z * Z + C
                i += 1

            bitmap[y * width + x] = 1 if norm(Z) <= limit else 0

width_height = int(sys.argv[1])

bitmap = [0] * (width_height * width_height)
start = time.perf_counter_ns()
mandelbrot(width_height, width_height, bitmap)
elapsed_ns = time.perf_counter_ns() - start
print("Elapsed ms:", elapsed_ns / (1000 * 1000))

with open("mandelbrot.pbm", 'wb') as f:
    f.write(bytes(f"P4\n{width_height} {width_height}\n", 'utf-8'))
    byte = 0
    for i, bit in enumerate(bitmap):
        byte = byte << 1 | bit
        if i % 8 == 7:
            f.write(bytes([byte]))
            byte = 0
