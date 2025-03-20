
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

time complexity is taught to every cs student in every cs program. 
it is the default model that most people have when it comes to whether
an algorithm is "fast" or "slow".

back in the 80s, when every computer had only one core and no one besides
a couple of [weirdos](https://en.wikipedia.org/wiki/Thinking_Machines_Corporation)
knew what a [simd](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data)
was, this was largely a correct model.

an algorithm which had 10 times more multiplies would take 10 times longer,
regardless of the structure of those 10 multiples, because every operation
was implicitly blocking if you only have one computational unit.

but the year is now 2025. it is very hard to find computers with a single core.
even smartphones have 4-8 cores [source needed].

and as a result, time complexity largely fails as a measure of how fast or slow
certain algorithms are, and sometimes, is entirely misleading.

worse of all, time complexity is sometimes still used as an attribute for
inherently parallel algorithms, like every 
[linear algebra operation ever](https://en.wikipedia.org/wiki/Computational_complexity_of_matrix_multiplication).

i think this is ridiculous. we need a better way to think about the "complexity"
of different algorithms. the 
[work-depth model](https://www.cs.cmu.edu/~scandal/cacm/node1.html) 
of analysis provides a good
level of abstraction for thinking about the theoretical lower bound complexity of
algorithms not as the number of operations with respect to input size.

instead, it's better to think about the depth of the computation graph with respect
to input size, or in other words, the minumum number of non-parallelizable
sequential operations.

these are truly not parallelizable, and **demand** that the previous steps in
the computation graph have been completed before it can proceed.

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

        *--------*-------*------------------------*------*----------------*
        |  op    | depth |     input              | work | parallelizable |
        *--------*-------*------------------------*------*----------------*
        |        |       |                        |      |                |
        |  LOAD  |   1   | [a₁₁ a₁₂ ⋯ a₁ⱼ ⋯ aᵢⱼ]  |  n   |        n       |
        |  LOAD  |   1   | [b₁₁ b₁₂ ⋯ b₁ⱼ ⋯ bᵢⱼ]  |  n   |        n       |
        |  MUL   |   1   |  *  *      *     *     |  n   |        n       |
        |  STORE |   1   | [c₁₁ c₁₂ ⋯ c₁ⱼ ⋯ cᵢⱼ]  |  n   |        n       |
        |        |       |                        |      |                |
        *--------*-------*------------------------*------*----------------*
        |  TOTAL |   4   |                        |  4n  |        4n      |
        *--------*-------*------------------------*------*----------------*
        |  ASYMP |  O(1) |                        | O(n) |                |
        *--------*-------*------------------------*------*----------------*
```


## case 4: matrix multiplication


## case 5: softmax


## case 6: attention


## notes on assumptions

## speculations on future compute


---

# extra hot takes

## case 7: sorting is logarithmic



----

@misc{doan2025attnislogarithmic,
  author = {Doan, Mike},
  title = {Attention is logarithmic, actually},
  url = {https://supaiku.com/attention-is-logarithmic},
  year = {2025}
}
