import subprocess
from os import makedirs


def compileLaplace(omp, o3):
    file = "./laplace.cxx"
    flags = ["g++", file, "-o", "laplace"]

    if omp:
        flags.append("-fopenmp")
        file = './laplace-omp.cxx'
    if o3:
        flags.append("-O3")

    result = subprocess.run(flags, stdout=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError("Compilation Error with flags:", flags)


makedirs("./results", exist_ok=True)
PROGRAM = "./laplace"
MAXTHREADS = 8

with open("./results/execution.csv", mode="w") as out:
    out.write("flags;n_threads;nx;result;elapsed\n")
    
    # Wihout OpenMP
    omp = False
    
    #without 03
    o3 = False
    compileLaplace(omp, o3)
    for nx in [512, 1024, 2048]:
      print(f"No flags and nx = {nx}")
      result = subprocess.run(
        [PROGRAM, str(nx)], stdout=subprocess.PIPE).stdout.decode('utf-8')
      out.write(f"None;1;{nx};{result}")

    # Run with -O3
    o3 = True
    compileLaplace(omp, o3)
    for nx in [512, 1024, 2048]:
      print(f"O3 and nx = {nx}")
      result = subprocess.run(
        [PROGRAM, str(nx)], stdout=subprocess.PIPE).stdout.decode('utf-8')
      out.write(f"O3;1;{nx};{result}")

    # Run with OMP
    omp = True
    
    # Run without O3
    o3 = False
    compileLaplace(omp, o3)
    for n_threads in range(1, MAXTHREADS+1):
      for nx in [512, 1024, 2048]:
        print(f"fopenmp, threads = {n_threads} and nx = {nx}")
        result = subprocess.run([PROGRAM, str(nx)], stdout=subprocess.PIPE, env={
                                "OMP_NUM_THREADS": str(n_threads)}).stdout.decode('utf-8')
        out.write(f"fopenmp;{n_threads};{nx};{result}")

    # Run with O3
    o3 = True
    compileLaplace(omp, o3)
    for n_threads in range(1, MAXTHREADS+1):
      for nx in [512, 1024, 2048]:
        print(f"fopenmp + O3, threads = {n_threads} and nx = {nx}")
        result = subprocess.run([PROGRAM, str(nx)], stdout=subprocess.PIPE, env={
                                "OMP_NUM_THREADS": str(n_threads)}).stdout.decode('utf-8')
        out.write(f"fopenmp+O3;{n_threads};{nx};{result}")
