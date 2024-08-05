---
title: circular double buffers
---

### [[index|supaiku dot com]]

# a weird data structure for scaling synthetic data generation

---
> oops i accidentally made our training pipeline 170x faster
>
> the best way to deal with race conditions is to not have them
>
> also "python is slow", lol, lmao even
---

for most of ml, when people talk about synthetic data, they mostly think about how good it is. for neuroimaging though, we have some extra concerns, each of which gives you more problems as you try to solve them.
- where the hell are you storing it? -- neuroimaging data is 3d, and a single (256,256,256) cube is 64MB. scale this up for a couple hundred thousand, and you have terabytes on your hands.

> okay i'll just store it in a cache then

- how the hell are you going to move it? -- this is a lot of data, from a lot of computers potentially. how do you fill up and clear out a cache reliably with gigantic data without running into race conditions and other stuff.

> okay... i'll just use something off the shelf, like redis or mongodb

- okay redis has blocking io, first of all, and second of all, mongodb has a collection size limit

---

## the rotating circular array

- torch has its dataset class, which really likes arrays with contiguous indeces
- using a source of data that has **throughput** has some implications
    - if either training or generation outpaces the other, there's a **bottleneck**
    - if training is faster, then you're wasting flops on the training node
    - if generation is faster, then you're wasting samples from the generation node


okay what if we did something like:
```
v-------------------------------------------v := Array of size N
|                                           |
[sample 1, sample 2, sample 3, ..., sample N, sample 1, sample 2, ...]
                                              ^^^^^^^^^
    using modular indexing, a[index%len(a)] to make an "infinite" array

        ex: with 100 samples in the cache, i can do a[10000] and 
            get the 10000 % 100 == 0th sample (this works for all N) 
```

this certainly solves the training throughput question. so if we have N samples in our cache, we can just train on it on a loop, basically equivalent to running multiple epochs

but how do we get data into it? how about:
```
[sample 1, ... sampleN, sample1, ...]  <- READ cache, always full
                                                        
[sample 1, sample 2 ...             ]  <- WRITE cache, not full
|                                   |
^-----------------------------------^ := capped array size N
```

okay but how do we get the sample from write to read though? 

well, well, well, have you heard of [double buffering](https://en.wikipedia.org/wiki/Multiple_buffering#:~:text=The%20term%20double%20buffering%20is,provided%20via%20Physical%20Address%20Extension)?
```
if WRITE cache is full:
    *READ cache = &WRITE cache 
    free(WRITE cache)
    WRITE cache = new cache
```

- you can just swap the pointers to the caches
- this is an O(1) operation
