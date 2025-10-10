---
title: i spent 200+ dollars on llm agents writing an implementation of minif2f in verfiers, and all i have to show for it is 800 bucks in gpu credits, a merged pr, and 2000 lines of B- code 
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
i spent 200+ dollars on llm agents writing an implementation of minif2f in verfiers, and all i have to show for it is 800 bucks in gpu credits, a merged pr, and 3000 lines of B- code 
</h1>

---
> alternate title: a walkthrough of what happens when a vibe coding weekend project spins way out of control
> but also: a list of things that i can reliably get llm agents to do
>
> as well as: a review of claude code, codex, and slate 
---

## I. what?

for those unaware, here are the some big blobs of context

1. __minif2f__ is a popular formal theorem proving benchmark from openai. basically
a bunch of competition math problems translated into a couple of languages (in
particular, lean3, isabelle, hollight and metamath)

2. __formal theorem proving languages__ (like the ones listed above) are languages
which take math (which is itself pretty formal) and completely automate
the process of verifying that the math is correct.

    this action is not free. and the cost of this of course, similar to the
    distinction between pseudocode and actual code, is that the language is
    much, much more strict.

3. __verifiers__ is a oss framework for developing benchmarks developed by willcb
and the prime intellect team, in which you could implement many benchmarks,
such as minif2f!

4. __llm agents__ are just llms (sometimes multiple) running in some kind of
   context management harness, which emit computer actions which can be executed,
   whose outputs are then plugged back in for (potentially human) introspeciton
   and guidance.

5. __two hundred us dollars__ is a pretty large amount of money one could spend
   on llms, and is an especially large sum of money if you consider how much
money people spend to write a piece of software that doesn't need special
hardware to host.

--------------------------------------------------------------------------------

## II. huh?

so if you're still confused as to what the blog title is talking about. here's
the full story. back in august, prime intellect launched this thing called the
environments hub, which hosts a bunch of benchmarks for llms. they also
did a cool bounty system, in which random people can jump in and implement
benchmarks for cash / gpu credits.

seeing that i suddenly had a lot of free time on my hands, i took on the
challenge of implementing minif2f. it's popular! the data is clean! even formal!
how hard can this be? should be a weekend project at most.

well as it turns out, a lot damn harder than i thought.


--------------------------------------------------------------------------------

## III. formal language compilers don't have the great ux

so that's not entirely true. lean is a pretty nice piece of software.
multithreaded / batched compilation, cached builds (olean files work okayish
as a caching system), whose version manager, elan, is available through basically
all package managers.

i can't spare the same nice words for the other languages.

forget package managers, isabelle is distributed as a raw tarball that you
download and chuck into your path.

and forget cli invokation, hollight can only be invoked by using the ocaml repl.
(did i also mention that the entrypoint for hollight is a shell script called
hol.sh)

and i hope you love long startup times! because the metamath proofs require set.mm,
a 41MB giant blob, that you have to load in for every proof verification. (since
if you combine two proofs into one file, how do you know which one is the one that
caused the failure.

--------------------------------------------------------------------------------

## IV. so what does it mean to 'implement' minif2f, exactly

here's the recipe for the soup:

1. you need to present the original __incomplete proof statements__ on a
   platter to the llm. these proof statements are incomplete, and you ask the
   llm to generate the full thing. this is basically some __string templating__.

2. you use a llm engine (like vllm, or supplied from an api provider) plus a
   sampling engine, like verifiers, to collect proof statements from the llm.
   both of these are already implemented, so can just be reused.

3. you take the proof statement into the llm, run whatever humiliation ritual
   the compilers need from you to get it verified, and then parse the results
into a reward for the llm. __this is the load bearing step__.

4. if you want to do multi turn, you'll need to pass the compiler feedback into
   the llm context, and ask for another proof attempt. this step is mandatory
for a difficult benchmark like minif2f.


do all of these, in a reliable way, and hook everything together, and viola!
you have minif2f!

--------------------------------------------------------------------------------

## V. enter, llm agents

the discourse surrounding llm agents, (frequently described with the partially
self deprecating and partially derogatory term 'vibe-coding') has been
something of a challenging space to find signal in. of the top of my head, here
are some issues:

1. it isn't entirely clear what, and to what extent, different people use these
   llm agents for: are people writing full ml training loops in them? are they
using it for writing compilers? are they using them only for translating
business logic in a B2B SaaS app?

2. it also isn't clear what skills are demanded of a person when they
   'vibe-code'. is it enough to just understand the problem well enough that
   you'd be able to write it yourself, or is it enough that you can vomit out
   "huhguhhhhh i want a webvseti athat makesm ame a  billllinoin doolars please"
   into claude code, and hit enter until you have 10 gazillion ARR?

3. it is __especially__ most unclear what speicifc problems or programming
   tasks an llm agent can help you with. prototyping? writing tests? making
things pass tests? async programming? fixing python environment issues?

4. and additionally, assuming that there is a set of things that llm agents
can reliably do, is there a recipe for getting this done?

this answer will maybe answer some of these questions, from my experience
in the past few months, but particularly through the lens of my project to port
minif2f to verifiers.

--------------------------------------------------------------------------------

## VI. what can't i reliably use agents for?

so set expectations correctly, here's my discovered list of things that you should
definitely do yourself and basically never hand to an llm:

1. __looking at your data__: for this project, it was looking at the actual
   minif2f proofs, one thing that i discovered immediately was that the proofs
are potentially way too hard to get a correct proof from. worse yet, there
isn't even a completed solution set, so it's possible that i wouldn't be able
to verify that any of my backends will work. the agents are currently __not
capable__ of this meta cognitive thinking.

2. __writing the out of distribution load bearing components of your code__:
   for this project, it was the delicate handling of proofs into the project /
file template. i spent one afternoon writing this backend for lean, and had
this backend thoroughly tested end to end.

3. __maintaining code quality__: none of the agents have particularly good
   taste in code ('good' in this case means easy to maintain, first and
foremost by the llm agents themselves, but also by me). i write in a very
procedural and functional forward style in python, which makes things
very easy to debug. but the agents don't know this, and usually write 7
layers of indirection to implement a simple function.

4. __maintaining code quality__: even with tests, i still absolutely have to
   read the damn code. maybe not as well as i should, but a code review on a
completed PR is basically mandatory unless i want things to explode in my face.

a useful rule i hold in mind is that llms will never reduce the amount of work
i have to do on a daily basis, but they __will__ increase the scope of work i
can reasonbly manage with the same amount of time. effort is still abssolutely
required.

that is to say: vibe coding shouldn't be easy.

--------------------------------------------------------------------------------

## VII. so why use llm agents at all?

1. because our editors can't specify global fuzzy edits

all of our editing tools (vim, vscode, emacs, etc etc) are both extremely local
(in that they can only edit code in one particuilar region at a time), and also
extremely strict.

__an llm agent is basically a fuzzy editor.__

i can specify

"please refactor all of these files which already have the exact namespaces for their
functions (lean_compile, metamath_compile, ...) to instead use a base class with
class methods with those names (compile, check ,... ) and make each of the backends
inherit from that. please give me a schema of how you are going to implement this
and ask a bunch of questions if you're at all unclear"

and if the llm gives a spec i'm happy with, i can basically hit enter and go do
50 pushups or whatever.

this would instead be 30 mins to an hour of work in vim, and it would be incredibly
boring and tedious work. not only that, but it's also incredibly brittle. agents
basically never make syntax errors, don't accidentally break typing conventions,
don't forget to add doc strings (they might even add too many docstrings), and
don't mind typing out multiple variable names in a function signature to avoid
having to invent another abstraction.

this means i can maintain simple design patterns for longer into the project,
for way less effort and cost.

and notice, this kind of fuzzy edit __shouldn't__ and __doesn't__ change the
semantics of the code. that's still on me.

see [before](https://github.com/spikedoanz/prime-environments/commit/3d3ab0b1f054feccd7685ba21cc8f977bebce713)

and [after](https://github.com/spikedoanz/prime-environments/blob/main/environments/minif2f/backends/base.py)

neither are my proudest work, but the latter is more reliably testable
(inheritance patterns at least enforce a strict namespacing scheme and type
signature). and more importantly, i got 80% of the way there for maybe 1% of
the effort.

2. because alot of 'writing software' is braindead boring stuff too insignificant to automate

have you ever written a curl request by hand?

would you ever want to do that?

well you're in luck! because llms will gladly write curl request after curl
request until the sun burns out, and do it way more reliably than you will.

curl request (and similar things like pings) sit in this great spot of
ergonomics for llms, because they're pretty simple (the grammar), but are
very tedious to type out. llms these days have good enough instruction adherence
that i've never seen them mess up writing a curl request to some link,
using some auth, with some args. doing that manually takes a minute. doing
it with the llm, with some of these things usually already in context,
takes like 10 seconds.

same with scp'ing files

same with running a small number of tests that i don't want to manually specify,
but have a general category i can describe (run all of the tests for the backend
we just fixed).

using agents instead of writing automated scripts for this kind of thing is
nice, because it:

a. doesn't cost much, at all

b. is pretty reliable, or at least only ever wrong in the obvious way.

c. cuts down on project bloat.

for this project, i had to manage two machines (since lean3 did not work on my
main mac dev machine), so i was constantly running tests on my devbox.

problem is, i hate working on my dev box, so i would constantly just ask the llm
to pull the project on the other machine, and do this inconvenient test for me.

couple of ssh -c commands later, and we're done.

i also had a plethora of different models to test out, but was way too lazy to
look up how to make a request to them (stored in a dedicated endpoints.py file
in my repo) (string matching is hard for my fallible human brain). llms are
basically perfect for this kind of stuff.


--------------------------------------------------------------------------------

## VIII. so why did the agents work for me and not for others?

1. because i knew exactly what i wanted

i knew ahead of time what the project was going to look like. it was going to
look like 4 different backends for compilers, with a basic system for verifying
installations, a templating entrypoint for setting up the compile step and the
compile step itself. 

i wrote the first lean implementation by hand, and knew what i wanted the abstraction
of that backend to look like.

this means that i can just hit play, and reject or accept. there is no
cognitive load of wondering if this design pattern will work or not, i __know__
it works already and this comes from experience of actually having to write
this code myself before.

this also means that i have to reject about 50% of the things the llm gives me,
but that's why we have git worktrees and parallel agents, and guess how many
agents i run at the same time on average![^1]


2. because i am extremely disagreeable about code style

llms are slimy bastards. they appeal to 'best practices' and 'industry standards'
when all they do is write 50 line functions to do float division, with a fully documented
docstring and an additional test.

i have to yell at them (usually through the global CLAUDE.md in ~/.claude/CLAUDE.md)
about my preferences ahead of time, or else i'll be spending most of my tokens
telling them to please use an inline function instead of adding another layer
of indirection.

this is where a lot of the effort comes from, and where delicate care really goes the long
way. so repeat after me:

"llms are in __context__ learning machines"

"llms are in __context__ learning machines"

"llms are in __context__ learning machines"

they do not have the magical universal prior of 'the good code distribution', and even
if they did, that's not my preferred style of code.

so the answer is obviously: include the good code in the distribution. slap in a repo
i'm proud of, or reference a codebase i like (usually tinygrad) and i get to have a great
time.

--------------------------------------------------------------------------------

[^1]: if it's not obvious, the answer is two


