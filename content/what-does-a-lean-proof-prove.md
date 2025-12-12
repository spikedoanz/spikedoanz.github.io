---
title: what does a lean proof prove?
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
what does a lean proof prove?
</h1>

--------------------------------------------------------------------------------
> alternate title: the epistemics of trust in lean as a working programmer.
>
> tldr:
>   1. lean's theory is __consistent__. (relative to ZFC)
>   2. the (main) implementation seems __faithful__ to the theory (indirectly).
>   3. the implementation is __mostly bug free__.
>   4. the bugs that __were encountered__ (so far), were __not fatal__, and __are fixed__.
>   5. there is a small, but growing family of __independent implementations__ that
>   bolster the trust model in lean and proofs written in it.
>   6. maybe don't trust claims about software written in lean.
--------------------------------------------------------------------------------

## jargon

> things will get technical, but it's okay, here's a reference.

- a __type__: is the fundamental building block of all objects in Lean.
  > think `Nat`, `Bool`, `List`, and so on.

- a __term__: is an inhabitant of a type. think the number `4`, which is an inhabitant of `Nat`.

- a __proposition__: is a special type living in Lean's `Prop` universe[^1], whose inhabitants are _proofs_ rather than data.
  > for example, `2 + 2 = 4` is a proposition. a proof of it is a term of that
  > type. `True` and `False` are themselves propositions -- `True` has a trivial
  > proof, while `False` has no inhabitants at all.

- a __goal__: is a proposition you're trying to prove, together with the hypotheses you have available.
  > for the statement "if I have a proof of A and B, then I have a proof of B," this is encoded as:
  > ```
  > A B : Prop
  > h : A ∧ B
  > ⊢ B
  > ```
  > in english, each line says:
  > - A and B are propositions
  > - our hypothesis h is a proof of A ∧ B
  > - we need to construct a proof of B

- a __proof__: is a term inhabiting a proposition (in exactly the same way that `4` inhabits `Nat`).
  > for the above example regarding A and B
  > ```lean
  > theorem and_right' (A B : Prop) (h : A ∧ B) : B :=
  >   h.right -- .right deconstructs 'h' into its right element, in this case B, which is what we want to show/prove.
  > ```

- a __tactic__: is a procedure that transforms goals. Given a goal, a tactic either completes the proof or produces simpler subgoals.
  > for example, the rewrite tactic takes a proven proposition, and attempts to pattern match it to the current goal state
  > say we have the a proposition saying that we have two natural numbers called `n` and `m`, and we want to show that `n + m = m + n`
  > this would be encoded in lean as:
  > ```
  > example (n m : Nat) : n + m = m + n := by
  > ```
  > say we also have proven that addition over the natural numbers is commutative
  > (which is called `Nat.add_comm`), which looks like
  > [this](https://github.com/leanprover/lean4/blob/9d4ad1273f6cea397c3066c2c83062a4410d16bf/src/Init/Data/Nat/Basic.lean#L158-L163)
  > then we can apply the rewrite tactic to our proposition:
  > ```lean
  > example (n m : Nat) : n + m = m + n := by
  >   rw [Nat.add_comm]
  > ```
  > which transforms the goal state from
  > ```
  > n m : Nat
  > ⊢ n + m = m + n
  > ```
  > to
  > ```
  > n m : Nat
  > ⊢ m + n = m + n  -- trivially true!
  > ```

- __soundness__: a formal system is sound if every provable statement is true
  in the intended interpretation.
  > that is, the syntax (what you can derive) matches the semantics (what is
  > actually true). in lean's case, this would mean that if you have a term
  > `t : P`, then P actually holds in the mathematical model.

- __consistency__: a formal system is consistent if it cannot prove `False`
  > equivalently, it cannot prove both a statement and its negation (in systems
  > with explosion, these definitions coincide). 
  >
  > for completeness, i'll point out
  > that consistency is strictly weaker than soundness a consistent system might
  > prove false things, as long as it doesn't prove `False` itself. see [this
  > discussion](https://cs.stackexchange.com/questions/88274/why-does-soundness-imply-consistency)

- a __type theory__: is a collection of statements regarding types (and related
  theoretical machinery), how to use them, (optionally) the properties of that
  system in aggregate.
  > in lean's case, this is a modified version of [Martin-Löf Type
  > Theory](https://en.wikipedia.org/wiki/Intuitionistic_type_theory) (MLTT)

- the lean __kernel__ (also called the type checker): is a piece of software
  which implements that type theory, whose job is to validate that given a type
  and a term which is supposed to inhabit that type, that the term actually produces something of that type. 
  > in lean's case, this is intentionally made to be very small. despite this, as
  > of writing, there are few independent implementations of it in various
  > languages / by various people, and this has implications on the epistemics of
  > trusting the lean kernel which will be discussed in a later section

> note regarding interaction of tactics with the kernel: tactics do not show up
> in the artifacts that the kernel is supposed to validate at all. because
> tactics are intentionally designed to only produce proof terms, they
> themselves can be 'elaborated away'[^2]. as a result, people are
> allowed to use funky tactics like
> [hammer](https://github.com/JOSHCLUNE/LeanHammer) while still trusting that
> it doesn't overcomplicate the job for the kernel.

--------------------------------------------------------------------------------
 
## why do we care about soundness?

soundness means that every provable statement is true in the intended
interpretation—the symbols mean what you think they mean.

why does this matter?

- if a system is unsound, you might prove statements that don't hold in the
  model you care about. your proofs typecheck, but they're not "true" in any
  meaningful sense. the system is quietly lying to you.
- consistency (not proving `False`) is weaker. a consistent-but-unsound system
  won't explode, but it also won't reliably tell you anything about mathematics.

## why do we care about consistency?

- lean's type theory accepts the [principle of
  explosion](https://en.wikipedia.org/wiki/Principle_of_explosion): from a
  contradiction, anything follows. if you can prove `False`, you can prove
  anything, rendering the system useless.
- consistency guarantees this doesn't happen. it's the bare minimum for a
  logical system to be worth anything.

soundness gives you meaning. consistency gives you non-triviality. we want both.[^3]

--------------------------------------------------------------------------------

## should you trust lean?

> the short answer: yea probably
> 
> the long answer: this has to be done in two parts
> 1. that lean (the theoretical object) describes a sound/consistent formal system
> 2. that lean (the piece of software) accurately implements this theory

### epistemics of lean (the theory)
1. lean's type theory is formally specified (this wasn't always the case. lucky us!)

2. this formally specified theory has been proven consistent __relative__ to ZFC[^4]
   > that is, assuming ZFC is consistent (as all working mathematicians do),
   > lean is consistent. this is formal blackmail: you can't worry about lean's
   > consistency without also worrying about ZFC.
   >
   > note: this is the best one could hope for. lean is susceptible to gödel's
   > second incompleteness theorem: systems capable of describing natural number
   > arithmetic cannot prove their own consistency. so consistency proofs must
   > be relative.

3. lean's __soundness__ (the stronger property) remains unproven.
   > recall: consistency says "you can't prove `False`." soundness says "every
   > provable statement is true in the intended model" -- the symbols mean what
   > you think they mean.
   >
   > carneiro's thesis sketches a soundness proof relative to a ZFC model, but
   > it's incomplete (several sections marked "UNFINISHED"). lean4lean is
   > working toward mechanizing this, but as of writing, only parts of the
   > typechecker have been verified and there are sorries throughout.
   >
   > in practice, this gap is small—if basic types like `Nat` and `=` didn't
   > mean what we think they mean, we'd likely have noticed by now. but the
   > philosophical gap between "probably fine" and "proven" remains.

### epistemics of lean (the software)

1. lean 4 (the one everyone uses) is written in C++ and is __not__ proven
   faithful to lean's type theory.
   > even more concerningly, lean's type theory did not formally exist for most
   > of lean's history. a specification only appeared around 2019 (Mario
   > Carneiro's thesis).

2. as a result, the trust model for lean resembles the compiler landscape:
   if two independent implementations give different outputs, at least one is
   wrong. but lean's situation is more complex, as we need trust at two levels:
  - __implementation__: does the kernel correctly implement the type theory?
   (multiple implementations help here)
  - __theory__: is the type theory itself sound?
   (this requires external proof, and by gödel, can't be done in lean itself)

3. [lean4lean](https://github.com/digama0/lean4lean) exists: a reimplementation
   of lean 4's kernel in lean 4 itself (self-described as a 'carbon copy' of
   the C++ implementation). this allows cross-checking, though with obvious
   circularity—you're trusting lean 4 to verify lean 4.
   > note: the consistency proof from Carneiro's thesis was a pen-and-paper
   > proof about lean 3's type theory, not a mechanized proof in lean4lean.
   > the mechanized proofs are WIP as of writing.

4. in the process of translating the lean kernel from C++ to lean4, several
   bugs [were actually
   found](https://github.com/digama0/lean4lean/blob/master/bugs-found.md).
   fortunately, these were all patchable. but considering that lean4lean
   was intentionally as close to the original implementation as feasible,
   there remains the possibility that there are other bugs lying in wait.
   > furthermore, these bugs only occured in edge cases, and did not
   > retroactively invalidate any existing proofs in mathlib / lean's core
   > modules.

5. very few independent implementations exist otherwise: there is
   [nanoda_lib](https://github.com/ammkrn/nanoda_lib) (from the author of
   ["Type Checking in Lean
   4"](https://ammkrn.github.io/type_checking_in_lean4/). though as of writing
   it doesn't achieve completeness w.r.t. all of mathlib),
   [trepplein](https://github.com/gebner/trepplein) (lean 3 only), and a few
   others in progress. 

   i myself am working on
   [lean4idris](https://github.com/spikedoanz/lean4idris) which covers about
   95% of lean's core modules but is still nowhere near the shape where it
   would have implications for this discussion.

--------------------------------------------------------------------------------

## how much should i trust proofs written in lean then?

for most intents and purposes, for the domain that lean dedicates most of its
work to, that is mathematics, it is approaching the gold standard of trust.
(even moreso than a math proof on paper, understandably, if one accepts that
lean's kernel is trustworthy)

while lean is proven consistent but not proven __sound__, there remains the
possibility that our proofs typecheck perfectly but don't mean what we think
they mean. the system wouldn't explode -- it would just be quietly lying to us.

there is an additional concern, which is the regular trust models associated
with code auditing. i myself haven't fully gone through the proof of lean's
relative consistency w.r.t. ZFC; yet i trust that this result is likely true
for the same reason that working professionals in any technical field have for
trusting most things in their field work -- other smart people said so.

so there is definitely a sociological angle that can be looked at when it
comes to trust in the lean kernel not just at the global level (knowing all
the proofs, reading all the papers, being the amalgamation of all lean experts
in one brain), but also at the individual and organizational level.

--------------------------------------------------------------------------------

## what does lean have to say about software?

> short answer: not as much as you'd hope

lean's marketing increasingly emphasizes software verification, and there are
real success stories (AWS Cedar, some blockchain work). but there are
significant gaps between "lean can verify software" and "lean provides the same
guarantees for software that it provides for mathematics."


### 1. the coinduction problem

lean lacks native support for coinductive types. this means you can't naturally model:

- infinite streams (like server event loops)
- lazy data structures
- reactive systems
- anything that runs forever without terminating

coq and agda have coinduction in their kernels. lean's approach is to encode
coinduction via quotients of polynomial functors (QPF), which works but is
awkward and not well-supported by tooling. there's ongoing work (QpfTypes), but
it's not mature. 

this matters because most real software doesn't terminate: servers, operating
systems, UI event loops. lean can reason about terminating computations, but
the bread and butter of systems programming is out of reach.


### 2. the runtime problem

even if you prove properties about lean code, you face a stack of trust issues:

a. lean's compiler is unverified. your proven lean code gets compiled to C,
which gets compiled by gcc/clang. none of this is verified.

b. the runtime is unverified. lean's runtime (reference counting, memory
management, FFI) is C++ code outside the kernel. bugs here can violate any
invariants your proofs established.

c. FFI breaks everything. lean's FFI lets you call arbitrary C code, which can
do anything—corrupt memory, violate type safety, introduce undefined behavior.
there's no verification story here.

d. relatedly, sometimes this has implications on the theorem proving side of
lean as well, because some tactics, like
[native_decide](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference/#native_decide),
__call into__ the runtime, and thus slightly complicate the trust model of the
derived proof.


### 3. the translation problem

even with a perfect runtime, you'd still need to trust that your lean model
faithfully captures the software you care about. if you model your system in
lean and prove things about the model, those proofs say nothing about your
actual deployed code unless you can verify the translation; which you can't,
currently.


### 4. hardware verification is not lean's focus

coq has decades of hardware verification work (CompCert, etc.). lean's
community is primarily mathematicians. from the zulip archives: "it seems very
much like Lean was written for mathematicians whereas Coq was written for
software verification." 

this is slowly changing, but the libraries, tooling, and expertise aren't there yet.


### 5. what can you trust?

if you prove something in pure lean (no IO, no FFI, no unsafe), you can trust
that:

- the mathematical statement holds (modulo lean's soundness)
- if you extract the lean code and run it through the lean interpreter, it will
  compute correctly

but "lean verified my software" is not the same as "my deployed binary is
correct." the gap between the two is significant and currently unbridged. if
you're interested in verification of software specifically, then may i interest
you in our lord and savior [idris2](https://github.com/idris-lang/Idris2)

--------------------------------------------------------------------------------

## related links

- [type checking in lean4](https://ammkrn.github.io/type_checking_in_lean4/), in
particular the section about
[trust](https://ammkrn.github.io/type_checking_in_lean4/trust/trust.html), which provides
a comprehensive list of assumptions one should reasonably make in order to 'trust' the lean kernel.

JY Girard's excellent ['Proofs and
Types'](https://www.paultaylor.eu/stable/prot.pdf), which underpins most of my
early study of type theory and formal theorem proving.

- [Mario Carniero's paper formally describing lean's type theory](https://github.com/digama0/lean-type-theory)

- [a list of bugs discovered in the process of writing lean4lean, and related
  discussions](https://github.com/digama0/lean4lean/blob/master/bugs-found.md)

- [Mario Carneiro's talk about lean4lean](https://www.youtube.com/watch?v=GOrIMiI2zLA)

--------------------------------------------------------------------------------

[^1]: [universes](https://ncatlab.org/nlab/show/type+universe) themselves are
    also types whose inhabitants are types (roughly). they exist for paradox
    prevention reasons (as well as making polymorphisms and large eliminations
    work coherently)that aren't relevant to the contents of this blog. think of
    it as a formal OSHA requirement.
[^2]: if you don't know what this means, it's the same as functions being
    'compiled away' into jump instructions. the machine (in this case the kernel),
    only sees its ISA (legal type operations)
[^3]: while consistency is derivable from soundness, it's not the __only__ way
    to obtain this. in principle, this suggests the existence of systems that
    are __unsound__ but nonetheless __consistent__. in english this suggests
    systems that are by all means, perfectly usable as logical systems, with
    all things being internally consistent, and yet proves things that are
    completely alien to what you intended. search for such a system / related
    works is left to the astute reader.
[^4]: more accurately, [ZFC + n
    inaccessibles](https://math.stackexchange.com/questions/3633748/zfc-there-exists-an-inaccessible-cardinal-proves-conzfc),
    but the meaning of this distinction doesn't really matter for our purposes.
