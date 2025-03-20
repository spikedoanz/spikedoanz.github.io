
---
title: attention is logarithmic, actually
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
attention is logarithmic, actually
</h1>


---
> time complexity is a very bad model when working with parallelism.
>
> in which i make the case for [work-depth](https://www.cs.cmu.edu/~scandal/cacm/node1.html)
> analysis instead of time complexity.
---

time complexity is the default model brought up when discussing whether
an algorithm is "fast" or "slow".

back in the 80s, when every computer had only one core and no one besides
a couple of [weirdos](https://en.wikipedia.org/wiki/Thinking_Machines_Corporation)
knew what a [simd](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data)
was, this was largely correct.

for instance, an algorithm which had 10 times more multiplies would take 10 times longer,
regardless of the structure of those 10 multiples, because every operation
was implicitly blocking if you only have one computational unit.

but the year is now 2025. it is very hard to find computers with a single core.
even smartphones have 4-8 cores [source needed]. as a result, 
time complexity largely fails as a measure of how fast or slow
certain algorithms are.

using time complexity, there is no way to distinguish between an 
algorithm that requires O(n^3) operations that is 
[emberassingly parallel](https://en.wikipedia.org/wiki/Embarrassingly_parallel)
, versus one that is irreducibly sequential

worse yet, time complexity is sometimes still used to describe
inherently parallel algorithms, such as every 
[linear algebra operation ever](https://en.wikipedia.org/wiki/Computational_complexity_of_matrix_multiplication).

i think this is ridiculous. we need a better way to think about the "complexity"
of different algorithms. the 
[work-depth model](https://www.cs.cmu.edu/~scandal/cacm/node1.html) 
of analysis provides a good
level of abstraction for thinking about the theoretical lower bound complexity of
algorithms not as the number of operations with respect to input size.

instead of thinking about the raw numbers of operations an algorithm performs, or **work**,
, it's better to think about the **depth** of the computation graph with respect
to input size, or in other words, the minumum number of non-parallelizable
sequential operations. as these are irreducibly blocking, no matter how many cores you
have in your computer.

my expertise is mostly in performance engineering of ml systems, so the focus of
this article will mostly relate to algorithms that apply to tensors.

this model is not perfect, and i will detail why in a [later section], but to
start off, the best question to ask is:

> what is the time complexity of element wise multiplication?

from which we will eventually work up to my thesis, which is that **vanilla**
attention as it is implemented in transformers, should be considered logarithmic
in computational complexity.


-------------------------------------------------------------------------------

## case 1: element wise multiplication


given a vector a and a vector b with the same number of elements.

element wise multiplication takes every element in a and multiplies it
with the matching index in b and stores it in a new vector c (or in place)

the pseudo code will look like:

```
n   = <big integer>
a,b = arange(n), arange(n)
c   = zeros(n)
for i in range(n):
  c[i] = a[i] * b[i]
```

time complexity wise, this is obviously linear. and performed on a single thread,
this is true!

however if you take a closer look, you'll realize that in the computation graph
of this problem, none of the steps in range(n) depend on one another. they're
entirely independent.

so ... why not do them in parallel?

which is exactly what every linear algebra/tensor library does under the hood.

and you quickly find out that, the problem isn't linear at all! it actually
looks like constant time until a mysterious cutoff point (that we will detail
later).

[insert benchmark]

more concretely, we can analyze the work and depth of element wise
multiplication:

```
    *--------*-------*-----------------*------*----------------*
    |  op    | depth |     input       | work | parallelizable |
    *--------*-------*-----------------*------*----------------*
    |        |       |                 |      |                |
    |  LOAD  |   1   | [a₁ a₂ ... aᵢ]  |  n   |        n       |
    |  LOAD  |   1   | [b₁ b₂ ... bᵢ]  |  n   |        n       |
    |  MUL   |   1   |  *  *      *    |  n   |        n       |
    |  STORE |   1   | [c₁ c₂ ... cᵢ]  |  n   |        n       |
    |        |       |                 |      |                |
    *--------*-------*-----------------*------*----------------*
    |  TOTAL |   4   |                 |  4n  |        4n      |
    *--------*-------*-----------------*------*----------------*
    |  ASYMP |  o(1) |                 | o(n) |                |
    *--------*-------*-----------------*------*----------------*
```

every operation required in the algorithm: load, mul, store, all have
constant depth, and given enough parallel compute (up to the magical cutoff
point mentioned above), all of them can effectively be done in constant time.


-------------------------------------------------------------------------------

## case 2: vector summation (aka contraction)


summation is a bit more complicated than elementwise operations. here, we clearly
see that there is a dependency between two steps (since accumulation requires calling
into c's state). and this cannot be done emberassingly in parallel.

```
n = <big integer>
a = arange(n)
c = 0
for i in range(n):
  c += a[i]
```

fortunately though, if you look a bit closer, you'll realize that this is only
a dependency between every *two* steps, or pairs.

it is in fact still possible to parallelize this operation, by instead of doing
every elementwise operation in parallel in one step, doing every **pairwise**
operation in one step.

for a list of length n, the progression is as follows:

1. sum up every adjacent even and odd pair of numbers in the list (there are
n/2 of such pairs), and store them into either the even or odd index of the pair.

2. sum up every adjacent **summed pair**, and do the same index trick (there are
n/4 of such pairs of pairs)

3. pairs of pairs of ... pairs

4. after log_2(n) steps, you'll have a single number that is the sum every element
in the list.

```
    *------------*---------*-----------------------------------*------------*
    |  op        |  depth  |                  input            |    work    |
    *------------*---------*-----------------------------------*------------*
    | LOAD       |    1    | [a₁     a₂     a₃     a₄  ⋯  aᵢ]  |     n/2    |
    |            |         |  \     /       \     /       /    |            |
    | PAIRWISE + |    1    |  [a₁+a₂         a₃+a₄   ⋯  ]      |     n/4    |
    |            |         |     \           /        /        |            |
    | PAIRWISE + |    1    |     [(a₁+a₂)+(a₃+a₄) ⋯ ]          |     n/8    |
    |            |         |           \   /                   |            |
    |  ⋯         |    ⋯    |             ⋯                     |      ⋯     |
    |            |         |             |                     |            |
    | PAIRWISE + |    1    |            [∑a]                   |      1     |
    | STORE      |    1    |            [∑a]                   |      1     |
    *------------*---------*-----------------------------------*------------*
    |  TOTAL     | log n+1 |                                   |     n+1    |
    *------------*---------*-----------------------------------*------------*
    |  ASYMP     | O(log n)|                                   |     O(n)   |
    *------------*---------*-----------------------------------*------------*
```




## case 3: tensor product

```

    *--------*-------*--------------------------------*--------*
    |  op    | depth |     input                      |  work  |
    *--------*-------*--------------------------------*--------*
    |        |       |                                |        |
    |  LOAD  |   1   | [a₁₁ a₁₂ ⋯ a₁ⱼ ⋯ aᵢⱼ]          |  n²    |
    |  LOAD  |   1   | [b₁₁ b₁₂ ⋯ b₁ₖ ⋯ bⱼₖ]          |  n²    |
    |  MUL   |   1   |  *   *     *     *             |  n³    |
    |  STORE |   1   | [c₁₁₁ c₁₁₂ ⋯ c₁ⱼₖ ⋯ cᵢⱼₖ]      |  n³    |
    |        |       |                                |        |
    *--------*-------*--------------------------------*--------*
    |  TOTAL |   4   |                                | 2n²+2n³|
    *--------*-------*--------------------------------*--------*
    |  ASYMP |  O(1) |                                | O(n³)  |
    *--------*-------*--------------------------------*--------*

```


## case 4: matrix multiplication

```
    *--------------*-----------*--------------------------*--------*
    |  op          | depth     |     input                | work   |
    *--------------*-----------*--------------------------*--------*
    |              |           |                          |        |
    |  LOAD        |   1       | [a₁₁ a₁₂ ⋯ a₁ⱼ ⋯ aᵢⱼ]    |  n²    |
    |  LOAD        |   1       | [b₁₁ b₁₂ ⋯ b₁ₖ ⋯ bⱼₖ]    |  n²    |
    | TENSOR       |   1       |       "ij,jk->ijk"       |  n³    |
    |              |           |                          |        |
    | CONTRACTION  | log n     |        "ijk->ik"         |  n³    |
    | STORE        |   1       | [d₁₁ d₁₂ ⋯ d₁ₖ ⋯ dᵢₖ]    |  n²    |
    |              |           |                          |        |
    *--------------*-----------*--------------------------*--------*
    |  TOTAL       | logn +4   |                          | 2n²+2n³|
    *--------------*-----------*--------------------------*--------*
    |  ASYMP       | O(log n)  |                          | O(n³)  |
    *--------------*-----------*--------------------------*--------*
```



## case 5: softmax

```
    *--------------*-----------*--------------------------------*--------*
    |  op          | depth     |     input                      | work   |
    *--------------*-----------*--------------------------------*--------*
    |  LOAD        |   1       | x ∈ ℝⁿ                         |   n    |
    |  MAX         |  log n    | m = max(x)                     |   n    |
    |  SUB         |   1       | x' = x - m                     |   n    |
    |  EXP         |   1       | e = exp(x')                    |   n    |
    |  SUM         |  log n    | s = sum(e)                     |   n    |
    |  DIV         |   1       | y = e / s                      |   n    |
    |  STORE       |   1       | y ∈ ℝⁿ                         |   n    |
    *--------------*-----------*--------------------------------*--------*
    |  TOTAL       | 2log n+5  |                                |  7n    |
    *--------------*-----------*--------------------------------*--------*
    |  ASYMP       | O(log n)  |                                | O(n)   |
    *--------------*-----------*--------------------------------*--------*
```

## case 6: attention

```
    *--------------*-----------*--------------------------------*-----------*
    |  op          | depth     |     input                      |   work    |
    *--------------*-----------*--------------------------------*-----------*
    |  LOAD        |   1       | X ∈ ℝᵇˣⁿˣᵈ                     |  bnd      |
    |  LOAD        |   1       | Wq,Wk,Wv ∈ ℝᵈˣᵈ                |  3d²      |
    |  MATMUL      | 3log d    | Q = X·Wq ; K = X·Wk ; V = X·Wv |  3bnd²    |
    |  MATMUL      | log d     | S = Q·Kᵀ                       |  bn²d     |
    |  DIV         |   1       | S' = S / √d                    |  bn²      |
    |  SOFTMAX     | log n     | A = softmax(S')                |  bn²      |
    |  MATMUL      | log n     | O = A·V                        |  bn²d     |
    |  STORE       |   1       | O ∈ ℝᵇˣⁿˣᵈ                     |  bnd      |
    *--------------*-----------*--------------------------------*-----------*
    |  TOTAL       | 4log d +  |                                |           |
    |              | 2log n + 5|                                |  ≈ bn²d   |
    *--------------*-----------*--------------------------------*-----------*
    |  ASYMP       | O(logd)   |                                | O(bn²d)   |
    |              | if d >>n  |                                |           |
    *--------------*-----------*--------------------------------*-----------*
```

## notes on assumptions


## speculations on future compute

- most algos are still memory bound
- BUT, nn weights are completely static during inference
    - and MOSTLY static during training (gradient step is a very small % of the
    training cycle)
- therefore, it seems likely that future chips (if things that look like transformers
are still king, will most likely look like FPGAs (where the weights are flashed onto
the circuit as static memory) and inputs just blow through. gradient calculuations
can happen async.


-------------------------------------------------------------------------------

```
@misc{doan2025attnislogarithmic,
  title = {Attention is logarithmic, actually},
  url = {https://supaiku.com/attention-is-logarithmic},
  year = {2025}
}
```
