
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
> in which i make the case for [work-depth](https://www.cs.cmu.edu/~scandal/cacm/node1.html#SECTION00010000000000000000) analysis instead of
> time complexity.
---



## case 1: element wise multiplication

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
        |  ASYMP |  O(1) |                 | O(n) |                |
        *--------*-------*-----------------*------*----------------*
```



## case 2: vector summation (aka contraction)
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


---

# extra hot takes

## case 7: sorting is logarithmic

