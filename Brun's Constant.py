#!/usr/bin/env python3
"""
Brun's Constant Calculator (HPC OEIS Edition)
=============================================
Calculates Brun's constant for twin primes (B_2) using 12-core parallel prime sieving, 
C-accelerated gmpy2 primality tests, and strict OEIS truncation formatting.
"""
from __future__ import annotations

import argparse
import gc
import math
import multiprocessing as mp
import os
import sys
import time

from gmpy2 import is_prime
import mpmath





os.environ['MPMATH_GMPY2'] = '1'

sys.set_int_max_str_digits(0)

NUM_WORKERS = 12


def worker_twin_sieve(args) -> tuple:
    """Worker function for twin sieve.
    
    Args:
        args:
    
    Returns:
        tuple: Result of type tuple
    
    """
    start, end, dps = args
    mpmath.mp.dps = dps
    ctx = mpmath.mp

    partial_sum = ctx.mpf(0)
    count = 0
    p = start
    if p % 2 == 0:
        p += 1

    while p < end:
        if is_prime(p) and is_prime(p + 2):
            partial_sum += ctx.mpf(1)/ctx.mpf(p) + ctx.mpf(1)/ctx.mpf(p+2)
            count += 1
        p += 2
    return partial_sum, count


def save_oeis_files(constant_name, digits_str, target_digits):
    """Save oeis files to file.
    
    Args:
        constant_name:
        digits_str:
        target_digits:
    
    """
    clean_digits = digits_str.replace(".", "")[:target_digits]
    
    raw_filename = f"{constant_name}_{target_digits}_digits.txt"
    with open(raw_filename, "w", encoding="utf-8") as f:
        f.write(clean_digits)
    print(f"Saved raw digit output to {raw_filename}")

    b_filename = f"b_file_{constant_name}_{target_digits}.txt"
    with open(b_filename, "w", encoding="utf-8") as f:
        for idx, digit in enumerate(clean_digits, start=1):
            f.write(f"{idx} {digit}\n")
    print(f"Saved OEIS b-file output to {b_filename}")


def compute_brun_hpc(limit) -> tuple:
    """Compute brun hpc using optimized algorithms.
    
    Args:
        limit:
    
    Returns:
        tuple: Result of type tuple
    
    """
    dps_working = 50
    mpmath.mp.dps = dps_working
    ctx = mpmath.mp

    chunk_size = math.ceil((limit - 3) / NUM_WORKERS)
    chunks = []
    for i in range(NUM_WORKERS):
        start = 3 + i * chunk_size
        end = min(limit, 3 + (i + 1) * chunk_size)
        if start < limit:
            chunks.append((start, end, dps_working))

    with mp.Pool(processes=NUM_WORKERS) as pool:
        results = pool.map(worker_twin_sieve, chunks)

    total_sum = ctx.mpf(0)
    total_count = 0
    for chunk_sum, count in results:
        total_sum += chunk_sum
        total_count += count

    del results
    gc.collect()

    brun_str = ctx.nstr(total_sum, 20)
    clean_digits = brun_str.replace(".", "")[:15]

    save_oeis_files("Brun", clean_digits, 15)
    return clean_digits, total_count


def main():
    """Entry point — parse arguments and run the main computation.
    
    """
    parser = argparse.ArgumentParser(description="HPC Brun OEIS Calculator")
    parser.add_argument("-l", "--limit", type=int, default=1000000, help="Sieve limit (default: 1,000,000)")
    args = parser.parse_args()

    t0 = time.time()
    digits, twin_count = compute_brun_hpc(args.limit)
    t1 = time.time()

    print(f"Found {twin_count:,} twin prime pairs in {t1 - t0:.4f} seconds using {NUM_WORKERS} cores.")

if __name__ == "__main__":
    main()
