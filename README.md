===============================================================================
PROJECT: Brun's Constant Computation Engine
===============================================================================

OVERVIEW:
Calculates Brun's constant for twin primes (B_2 ≈ 1.902160583104...) by evaluating 
the sum of reciprocals of twin prime pairs (p, p+2).

ALGORITHM & MATHEMATICS:
- Formula:
    B_2 = sum_{(p, p+2) in Primes} (1/p + 1/(p+2))
- Fast Miller-Rabin / Baillie-PSW primality testing using gmpy2 for fast reciprocal summation.
