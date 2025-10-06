---
title: may lean eat the world
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
may lean eat the world
</h1>

---
> the generic goal of my next few months is to set the stage for lean vibe
> coding.
---

## I. what?

[lean](https://lean-lang.org/) is theorem proving language primarily used
for doing math. you may have heard it from such recent events as:

- [morph labs formalizing a classical theorem relating to the abc conjecture](
    https://github.com/morph-labs/lean-abc-true-almost-always)
- [terry tao's project formalizing PNT](
    https://mathstodon.xyz/@tao/111847680248482955)
- [math inc successfully formalizing strong PNT](
    https://github.com/math-inc/strongpnt)
- [an ongoing formalization of fermat's last theorem](
    https://lean-lang.org/use-cases/flt/)

__but__, it is also a [generic programming language](
https://lean-lang.org/functional_programming_in_lean/). think of it like haskell,
but even more strict.

anyone who's tried to write the language has very quickly realized it's extermely
hard to write.

however, while this is true, it is also true that you get certain guarantees
that wouldn't otherwise be available to you in a normal language, like python, rust
or even haskell. 

an example: __merge sort__: in lean, you can technically just write merge sort
the exact same way you would in haskell:

```haskell
mergeSort :: Ord a => [a] -> [a]
mergeSort [] = []
mergeSort [x] = [x]
mergeSort xs = merge (mergeSort left) (mergeSort right)
  where
    (left, right) = splitAt (length xs `div` 2) xs

merge :: Ord a => [a] -> [a] -> [a]
merge [] ys = ys
merge xs [] = xs
merge (x:xs) (y:ys)
  | x <= y    = x : merge xs (y:ys)
  | otherwise = y : merge (x:xs) ys
```

and in lean:

```python
def merge [Ord α] : List α → List α → List α
  | [], ys => ys
  | xs, [] => xs
  | x::xs, y::ys =>
    if x <= y then
      x :: merge xs (y::ys)
    else
      y :: merge (x::xs) ys

def split {α : Type} : List α → List α × List α
  | [] => ([], [])
  | [x] => ([x], [])
  | x::y::rest =>
    let (left, right) := split rest
    (x::left, y::right)

def mergeSort [Ord α] : List α → List α
  | [] => []
  | [x] => [x]
  | xs =>
    let (left, right) := split xs
    merge (mergeSort left) (mergeSort right)
```

it looks basically identical! so what's the catch?

well, for one, you can express the notion of a 'sorted list' directly into the type signature
```python
def Sorted [LE α] : List α → Prop
  | [] => True
  | [_] => True
  | x::y::rest => x ≤ y ∧ Sorted (y::rest)

def SortedList (α : Type) [LE α] := { xs : List α // Sorted xs }
```

and turn the function signature into:
```python
def mergeSort [Ord α] : List α → SortedList α
```

this guarantees that whatever you write, and compiles, is guaranteed to __actually__ correctly
map from an arbitrary list to a sorted one.

but now you're screwed! lean does not let you compile unless if you can prove that this
program actually does the job! here's an attempt from opus 4

```python
-- First, define what it means to be sorted
def Sorted [LE α] : List α → Prop
  | [] => True
  | [_] => True
  | x::y::rest => x ≤ y ∧ Sorted (y::rest)

-- Define SortedList as a subtype
def SortedList (α : Type) [LE α] := { xs : List α // Sorted xs }

-- Now merge sort must return both the list AND a proof it's sorted
def mergeSort [LE α] [DecidableRel (· ≤ · : α → α → Prop)] 
    (xs : List α) : SortedList α :=
  match xs with
  | [] => ⟨[], trivial⟩  -- Empty list is trivially sorted
  | [x] => ⟨[x], trivial⟩  -- Singleton is trivially sorted
  | xs =>
    let (left, right) := split xs
    let ⟨sortedLeft, proofLeft⟩ := mergeSort left
    let ⟨sortedRight, proofRight⟩ := mergeSort right
    let merged := merge sortedLeft sortedRight
    ⟨merged, by
      sorry  -- Need to prove that merge preserves sortedness!
    ⟩

-- The merge function would also need to prove it maintains sortedness
def merge [LE α] [DecidableRel (· ≤ · : α → α → Prop)]
    (xs : List α) (ys : List α) 
    (hx : Sorted xs) (hy : Sorted ys) : 
    { zs : List α // Sorted zs } :=
  match xs, ys with
  | [], ys => ⟨ys, hy⟩
  | xs, [] => ⟨xs, hx⟩
  | x::xs', y::ys' =>
    if h : x ≤ y then
      -- Need to prove that x :: (merge xs' (y::ys')) is sorted
      let ⟨rest, restProof⟩ := merge xs' (y::ys') (by sorry) hy
      ⟨x::rest, by
        sorry  -- Proof that x::rest is sorted given x ≤ y and rest is sorted
      ⟩
    else
      let ⟨rest, restProof⟩ := merge (x::xs') ys' hx (by sorry)
      ⟨y::rest, by
        sorry  -- Similar proof for y::rest
      ⟩
```

note the 'sorry' at the bottom. this means that the proof is not complete.

and this is only half the problem, there is also the more generic concern
that you need to prove that your algorithm is guaranteed to terminate given a
finite list.

so it's safe to assume basically no llm can do this task competently currently.
(without significant scaffolding and / or handholding) why do i care so much
about it as a research goal then?

================================================================================

## II. why?

### 1. lean as a frontier benchmark for reasoning llms

given that no publicly accessible (as of writing) can competently build even
something simple like a web application (or god forbid, even merge sort) in
lean4, this creates an interesting position for the language:

1. there are essentially limitless software engineering problems we could port
onto the language, and be relatively certain that data leakage is not too big
of a concern due to how little data exists for lean4.

2. the ported software tasks will be __harder__ than the existing benchmarks.
this lets us get a batch of unsaturated benchmarks for free!

3. absolving the need for a solution set for the benchmark. we can know if
something compiles, that it is the right solution for the problem, even if
we don't have the solution at the back of the book.

4. durable compounding software artifacts: say we have an "http benchmark".
well, the completion of this benchmark means that we now have http in lean!
which unlocks whatever benchmarks require an implementation of the http spec.
i'm sure you see the implications if we applied this to the other foundation
software standards: posix, concurrency runtimes, ...

if this were a vc pitch, i'd say something like: ARC-AGI, but for programming!

--------------------------------------------------------------------------------

### 2. lean as a fix __by construction__ to the hackable benchmark problem

a lot of the available oss programming benchmarks suffer from the issue of
hackability, in which the llm can manipulate portions of the codebase in
such a way that tricks the benchmark harness into letting a test pass.

the most obvious example of this happening in practice is plainly obvious
to anyone who's used claude sonnet 3.7, who frequently slaps a confident

```
def a_load_bearing_function():
  # this is a placeholder function, the real implementation will be much
  # cooler i promise
  pass
```

onto half of every codeblock it generates.

you can try one way or another to patch this at the level of the host
language in which your benchmark lives. but very few languages besides the
formal theorem proving family (lean, coq, agda, ...) allow you the specificity
and certainty that __if__ your agent successfully generated a code block
which passed the compiler __then__ it definitely did the job correctly.

as the number of environments blows up (as it currently is on prime's
environment hub), the certainty of knowing that your benchmarks are
actually reliable will become increasingly load bearing.

what if we solved this problem at the root, and build the lean compilation
loop as a part of the benchmark? this would partially[^1] solve the certainty
problem. the benchmarks would become unhackable given their spec.

---

## III. how?

### 1. data mining

while there isn't an insane amount of lean on the market, there is still at least
enough to write a compiler, so that covers ground code snippets regarding:
- a bunch of data structures: strings, trees, lists
- a bunch of algorithms: parsers, and generic traversal algos on data structures
- github issues, plus their resolutions: the lean4 codebase has 7500+ closed PRs

all of this can be mined and turned into sft data, or transformed into
benchmarks via reverse prompting.

--------------------------------------------------------------------------------

## 2. synthetic data with super rejection sampling

given an existing compiling lean program, attempt to create an equivalent
program with some notable change (or no change at all), and sample a bunch of
llm outputs. if it compiles, we're good![^2]

--------------------------------------------------------------------------------

## 3. synthetic environment generation

this is the most ambitious approach, and hinges on a hunch:

spec generation is easier than spec completion is easier than spec alignment

given this, we leave the hardest task, alignment to environment designers.
alignment can be __mined__ via reuse of existing codebases, which can be
transformed into specs automatically, and against which we can create a
benchmark.

there's a couple of research avenues we can target in this sub goal:
- a spec generation model (semisupervised rl)
- a spec preference model (alignment)

this part is where i am most unclear in where to take the research initiative.
suggestions would be greatly welcome!

--------------------------------------------------------------------------------

## III. mvp

as a starter target, i think it is most prudent to get the ball rolling on lean
as a platform for creating durable standing benchmarks. the most obvious way to
do this is to start by creating a suite of simple programming challenges that
can be benched and trained on using small llms. think rustlings for lean, for
llms.

--------------------------------------------------------------------------------

## IV. related works

[lean dojo](https://github.com/lean-dojo)

[lean copilot](https://arxiv.org/abs/2404.12534)

[https://moonshotai.github.io/Kimi-K2/](https://moonshotai.github.io/Kimi-K2/)#agentic-capabilities


[^1]: it is possible that even though your program passes the spec, that it's
still not what you want. sure, the semantics for 'sorted' are pretty simple
for merge sort. but what about something more complicated like convergence
properties of a numerical optimization algorithm?

[^2]: up to the spec, the programs themselves can and likely will be different
in terms of things not declared in the spec, but this is what we want)

