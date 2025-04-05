
---
title: what constructivism buys you
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
what constructivism buys you
</h1>

---
> constructivism is a field of formal logic where you must explicitly prove everything.
> it is a stricly weaker (and arguably more difficult) form of logic.
>
> so why would anyone ever use it?
---

## 1. wait there's multiple logics?

yes! there are many families of logic, and they mostly boil down to how you interpret
a "statement". (for those interested, it has to with how one interprets the words 
[denotation](https://en.wikipedia.org/wiki/Denotational_semantics), 
[sense](https://gawron.sdsu.edu/semantics/course_core/lectures/sense_compositionality.htm)
and [semantics](https://en.wikipedia.org/wiki/Semantics))

there are even more families than just classical (aka 
[tarskian](https://en.wikipedia.org/wiki/Semantic_theory_of_truth) logic) 
and constructivst (aka [heytingian](https://en.wikipedia.org/wiki/Heyting_algebra) logic).

but these are the two most popular ones, one forming the foundations of classical mathematics,
and the other forming the foundation of formal computational theory.

essentially, the difference is:

- classical logic views "statements" as boxes, which contain either True or False.
- constructivist logic views "statements" as things that are proven.

importantly, "proven" here means that a proof **must be provided**, it cannot be presumed.

---

## 2. so what is a "proof"?

a proof starts with a list of presumed statements, (called axioms).
then, you use logical operators (AND, OR, IMPLIES) to compose these axioms until you've arrived
at the statement you wish to prove.

i won't go into too deep details here, since this is a bottomless rabbit hole. so instead i'll link
to various resources:

- proofs and types.
- lean lang docs.

what is important though, is that if you're a programmer, you already know what a proof is.
a proof is a **program**. this is proven by the 
[curry-howard correspondence](https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence).

so you've written countless proofs before, but the words look slightly different.

instead of "statements" you have "types", and instead of "proofs", you have "programs".

but these are equivalent! proving a statement, and writing a program for it are the same thing.

example: writing a program that sorts a list is the same as proving that an arbitrary list can be sorted.

---

## 3. so what does this buy me?

the two important things that constructivist logic buys you are:
- consistency: every valid statement expressed is correct (no paradoxes).
- decidability: every valid question **will be answered**. this is also the same as **computability**.

what can you do with these things?


### 3.1 formal verification

some things come for free with consistency and decidable programs:

1. they cannot crash during runtime. (hardware could of course fail, but that's essentially never
the fault of the software)
2. you cannot have the halting problem: all processes will terminate, 

and it lets us write formal specification for software which doesn't require human reviewers.

the automotive industry uses one of these for C code (using the compcert compiler), but this
unfortunately doesn't scale past 10,000 lines of code.

### 3.2 proof assistants

we also have proof assistants like lean, coq, agda, ...
which enforce the rules of constructivist logic at a more global level.

this allows us to reliably write code that is **correct by definition**. if a program or
math proof compiles, it is guaranteed to have the properties that are listed.

there is of course the risk that the properties are wrong. but having a proof assistant
means that the entire process of writing the software given a spec is bulletproof.

### 3.3 sat/smt solvers


### 3.4 program synthesis

### 3.5 ability to reliably use AI

using a formally verified language also allows us to make use of AI in a reliable manner.

instead of typing in a verbal request, getting the AI output and running mental / automated tests on it
(both of which rarely have full coverage), we could instead:

1. write a spec of the program that we desire.
2. write proofs about that program, which formally capture that spec.
3. while(True): llm slings stuff at the wall until something sticks.

obviously it could be greatly improved. with intelligence comes ability to intelligently navigate
through the space of programs. we could have the AI write more proofs which extend the original spec
(all the while being **unable** to write something which contradicts our spec).

it could splice the program into multiple components, which then allows parallelization of the task to
either multiple AIs, or for human AI cooperation (though i doubt this lasts for more than a year or two)

---

## 4. so what's the catch?

the catch is that you have to toss out a significant chunk of classical mathematics.

uncountable infinity is not a constructable thing, therefore it doesn't exist in constructivist logic.
(or at least, cannot be **proven** to exist or not exist)

so...uh prepare to relearn (or reformulate, if the domain is niche enough)
topology? analysis? measure theory? probability theory? information theory?
calculus? basically most of mathematics.

you might get to keep linear algebra and category theory though, and all finite/discrete of math, like
combinatorics, graph theory, ...

you can still construct the reals, albeit they look a lot weirder.

you also sacrifice three very cool first order logical tactics:
- proof by contradiction: (not a -> false) -> (a -> true)
- proof by double negation: not not a -> a
- law of the excluded middle: (a or not a) -> true

also, "false" has slightly different semantics, and is also now called "bottom".
instead of just meaning "false" as in the opposite of true, or "proven",
it also can potentially mean:
- unproven
- unprovable (distinct from the top one, but this is an unprovable connection)
- doesn't halt (means the same as unprovable)
- causes a side effect (like your program crashing)
