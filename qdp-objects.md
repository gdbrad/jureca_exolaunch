grep -rni "qdp-jit statistics" *

## eigs 
single cfg 
 ------------------------
        -- qdp-jit statistics --
        ------------------------

Memory cache
  lattice objects copied to host memory:   8
  lattice objects copied to device memory: 4

Code generator
  functions jit-compiled:                  33
  total time for IR builder:               0.006428 s
  total time for libm IR linking:          0.048916 s
  total time for IR passes:                0.009298 s
  total time for code generation:          0.177197 s
  total time for dynamic loading:          1.103211 s

# meson-32
 ------------------------
        -- qdp-jit statistics --
        ------------------------

Memory cache
  lattice objects copied to host memory:   8
  lattice objects copied to device memory: 4

Code generator
  functions jit-compiled:                  33
  total time for IR builder:               0.006261 s
  total time for libm IR linking:          0.030258 s
  total time for IR passes:                0.009237 s
  total time for code generation:          0.178141 s
  total time for dynamic loading:          3.977068 s

# meson-64

# meson-96

# meson-128
------------------------
        -- qdp-jit statistics --
        ------------------------

Memory cache
  lattice objects copied to host memory:   8
  lattice objects copied to device memory: 4

Code generator
  functions jit-compiled:                  33
  total time for IR builder:               0.00676 s
  total time for libm IR linking:          0.034213 s
  total time for IR passes:                0.00958 s
  total time for code generation:          0.177151 s
  total time for dynamic loading:          3.518046 s


## perams 

# peram-32
------------------------
        -- qdp-jit statistics --
        ------------------------

Memory cache
  lattice objects copied to host memory:   8
  lattice objects copied to device memory: 4

Code generator
  functions jit-compiled:                  54
  total time for IR builder:               0.020499 s
  total time for libm IR linking:          0.057759 s
  total time for IR passes:                0.025723 s
  total time for code generation:          0.519581 s
  total time for dynamic loading:          35.49958 s


# peram-64

# peram-96

# peram-128
