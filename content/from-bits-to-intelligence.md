---
title: from bits to intelligence 
---

# from bits to intelligence
---

> how many lines of code do you need to train gpt 2?

---

let's consider the default stack. from loss.backward() down to the hardware

gpt 2 (500)[^1] written in 

torch (2.3 million) running on 

python (1.7 million) running on 

c compiled with gcc (10 million) running on 

linux (28.8 million)[^2] calling 

cuda kernels running on nvidia gpus written in an hdl

this totals up to about 50 million loc, give and take a couple million[^3]

while this gets you performance and reliability, it's not exactly educational. understanding this fully would be impossible

---

i propose an alternate stack, one aimed not at performance, but instead interpretability. consider this a [from the transistor](https://github.com/geohot/fromthetransistor), but for ml[^4]


### 1. hardware

compute: gpu/dsp style chip, (verilog, 1000)[^5]

host: cpu style chip, verilog (verilog, 1500)

memory: mmu (verilog, 1000)

storage: sd card driver (verilog, 150)

### 2. software

c compiler (python, 2000)[^6]

python runtime (c, 50000)[^7]

os (c, 2500)

file system: fat (c, 300)

init, shell, download, cat, editor (c, 500)


#### 3. tensors

tensorlib: numpy-like (python, 500)

autograd: (python, 5000)[^8]

#### 4. machine learning

data processing (500, python)

gpt 2 (500, python)

---


in total, this would be 64950 lines of code. but lets round that up to 100,000

that fits in a single repo. a single person could probably write all of this

if you're interested, start [here](github.com/spikedoanz/from-bits-to-intelligence)

---

[^1]: yes i know gpt 2 was originally written in tensorflow 

[^2]: all lines of code were collected with [loc](https://github.com/cgag/loc) from the repos [pytorch](https://github.com/pytorch/pytorch), [python](https://github.com/python/cpython), [linux](git@github.com:torvalds/linux.git)

[^3]: drivers, apis and the hdl for the gpus are closed source, so they've been omitted. but pulling ~ couple million lines out of a hat might not be [too far off](https://www.quora.com/How-large-is-the-HDL-source-code-of-a-modern-Intel-CPU)

[^4]: and made by someone who suffers from severe skill issues

[^5]: [tiny-gpu](https://github.com/adam-maj/tiny-gpu)

[^6]: you've heard of [co-recursion](https://en.wikipedia.org/wiki/Corecursion#:~:text=Put%20simply%2C%20corecursive%20algorithms%20use,produce%20further%20bits%20of%20data.), but have you heard of co-[self-hosting](https://en.wikipedia.org/wiki/Self-hosting_(compilers))?

[^7]: [micropython](https://github.com/micropython/micropython)

[^8]: [tinygrad](https://github.com/tinygrad/tinygrad)

---

last update 2024-07-16
