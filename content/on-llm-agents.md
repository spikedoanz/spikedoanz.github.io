---
title: i spent 100+ dollars on llm agents writing an implementation of minif2f in verfiers, and all i have to show for it is 800 bucks in gpu credits, a merged pr, and 2000 lines of B- code 
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
i spent 100+ dollars on llm agents writing an implementation of minif2f in verfiers, and all i have to show for it is 800 bucks in gpu credits, a merged pr, and 3000 lines of B- code 
</h1>

---
> alternate title: a walkthrough of what happens when a vibe coding weekend project spins way out of control
> but also: some things that i can reliably get llm agents to do
>
> as well as: a brief review of claude code, codex, and slate 
---

## I. what?

> feel free to skip forward to [section V](#v-enter-llm-agents)

for those unaware, here are the some big blobs of context

1. __minif2f__ is a popular formal theorem proving benchmark from
   [openai](https://github.com/openai/miniF2F). basically a bunch of
competition math problems translated into a couple of languages (in particular,
lean3, isabelle, hollight and metamath)

2. __formal theorem proving languages__ (or [proof
   assistants](https://en.wikipedia.org/wiki/Proof_assistant)) (like the ones
listed above) are languages which take math (which is itself pretty formal) and
completely automate the process of verifying that the math is correct.

    this action is not free. and the cost of this of course, similar to the
    distinction between pseudocode and actual code, is that the language is
    much, much more strict.

3. __verifiers__ is a [oss
   framework](https://github.com/PrimeIntellect-ai/verifiers) for developing
benchmarks developed by willcb and the prime intellect team, in which you could
implement many benchmarks, such as minif2f!

4. __llm agents__ are just llms (sometimes multiple) running in some kind of
   context management harness, which emit computer actions which can be executed,
   whose outputs are then plugged back in for (potentially human) inspection 
   and guidance.

5. __one hundred [us
   dollars](https://en.wikipedia.org/wiki/United_States_dollar)__ is a pretty
large amount of money one could spend on llms, and is an especially large sum
of money if you consider how much money people spend to write a piece of
software that doesn't need special hardware to host.

--------------------------------------------------------------------------------

## II. huh?

if you're still confused as to what the blog title is talking about. here's the
full story: back in august, [prime intellect](https://www.primeintellect.ai/)
launched this thing called the [environments
hub](https://www.primeintellect.ai/#environments), which hosts a bunch of
benchmarks for llms. they also did a cool bounty system, which let random people
jump in and implement benchmarks for cash / gpu credits.

seeing that i suddenly had a lot of [free
time](https://en.wikipedia.org/wiki/Unemployment) on my hands, i took on the
challenge of implementing minif2f (worth the aforementioned 800 bucks in gpu
credits). it's popular! the data is clean! even formal! how hard can this be?
should be a weekend project at most.

well as it turns out, it's a whole lot harder than i thought.

--------------------------------------------------------------------------------

## III. formal language compilers don't have the great ux

so that's not entirely true. lean is a pretty nice piece of software:
multithreaded / batched compilation, cached builds (olean files work okay-ish
as a caching system), whose version manager, elan, is available through all
modern package managers.

i can't spare the same nice words for the other languages.

forget package managers, isabelle is distributed as a raw tarball that you
download and chuck into your path.

and forget cli invokation, hollight can only be invoked by using the ocaml repl.
(did i also mention that the entrypoint for hollight is a shell script called
hol.sh), and that the repl can enter irrecoverable states, basically meaning
that setup steps have to be repeated per compilation.

and i hope you love long startup times! because the metamath proofs require set.mm,
a giant 41MB blob that you have to load in for every proof verification. (since
if you combine two proofs into one file, how do you know which one is the one that
caused the failure.

--------------------------------------------------------------------------------

## IV. so what does it mean to 'implement' minif2f, exactly?

here's the recipe for the soup:

1. you need to present the original __proof statements__ on a platter to the
   llm. these proof statements are __incomplete__, and you ask the llm to
generate the full thing. presenting the proof like this is basically some
__string templating__.

2. you use an llm engine (like vllm, or supplied from an api provider) plus a
   sampling engine, like verifiers, to collect proof statements from the llm.
   both of these are already implemented, so can just be reused.

3. you get the proof statement from the llm, run whatever humiliation ritual
   the compilers need from you to get it verified, and then parse the results
into a reward for the llm. rejected means no reward, compiled means full
reward. __this is the load bearing step__.

4. if you want to do multi turn, you'll need to pass the compiler feedback into
   the llm context, and ask for another proof attempt. this step is mandatory
for a difficult benchmark like minif2f.

once you do all of these, in a reliable way, and hook everything together, then 
viola! you have minif2f!

--------------------------------------------------------------------------------

## V. enter, llm agents

the discourse surrounding llm agents, (frequently described with the partially
self deprecating and partially derogatory term : 'vibe-coding') has been
something of a challenging space to find signal in. off the top of my head, here
are some issues:

1. it isn't entirely clear what, and to what extent, different people use these
   llm agents for: are people writing full ml training loops in them? are they
using it for writing compilers? are they using them only for translating
business logic in a B2B SaaS app?

2. it also isn't clear what skills are demanded of a person when they
   'vibe-code'. is it cool to just understand the problem well enough to be
able to write it yourself, or is it ok to just vomit out "huhguhhhhh i
want a webvseti athat makesm ame a  billllinoin doolars please" into claude
code, and hit enter until you have 10 gazillion ARR?

3. it is __especially__ most unclear what specific problems or programming
   tasks an agent can help you with. prototyping? writing tests? making
things pass tests? async programming? fixing python environment issues?

4. and additionally, assuming that there is a set of things that llm agents
can reliably do, is there a recipe for getting this done?

the rest of this essay will maybe answer some of these questions, from my
experience in the past few months, but particularly through the lens of my
project to port minif2f into verifiers.

--------------------------------------------------------------------------------

## VI. so what are agents terrible at?

to set expectations realistically, here's my discovered list of things that you
basically should never hand to an llm:

1. __looking at your data__: for this project, it was looking at the actual
   minif2f proofs, one thing that i discovered was that the proofs are
potentially way too hard to get a correct proof from. worse yet, there isn't
even a completed solution set, so it's possible that i wouldn't be able to
verify that any of my backends will work. the agents are currently __not
capable__ of this meta cognitive thinking.

2. __writing the out of load bearing components of your code__: for this
   project, it was the delicate handling of proofs into the project / file
templates, and the exact nobs and switches i have to press to actually compile
it. i spent one afternoon writing this backend for lean, and had this backend
thoroughly tested end to end.

3. __maintaining code quality__: none of the agents have particularly good
   taste in code ('good' in this case means easy to maintain, first and
foremost by the agents themselves, but also by me). i write in a very
procedural and functional-forward style in python, which makes things
very easy to debug. but the agents don't know this, and usually write 7
layers of indirection to implement long division.

4. __MAINTAINING CODE QUALITY__: even with tests, i still absolutely have to
   read the damn code. maybe not as well as i should, but a code review on a
completed PR is basically mandatory unless i want things to explode in my face.

a useful rule i hold in mind is that agents will never reduce the amount of work
i have to do on a daily basis, but they __will__ increase the scope of work i
can reasonably manage with the same amount of work. effort is still required.

that is to say: vibe coding shouldn't be easy.

--------------------------------------------------------------------------------

## VII. so why use agents at all?

1. because our traditional editors can't specify global fuzzy edits

all of our editors (vim, vscode, emacs, etc etc) are both extremely local (in
that they can only edit code in one particular region at a time), and also
extremely strict.

__an llm agent is basically a fuzzy editor.__

i can specify:

"please refactor all of these files which already have the exact namespaces for their
functions (lean_compile, metamath_compile, ...) to instead use a base class with
class methods with those names (compile, check ,... ) and make each of the backends
inherit from that. please give me a schema of how you are going to implement this
and ask a bunch of questions if you're at all unclear"

and if the llm gives a spec i'm happy with, i can basically hit enter and go do
50 push ups or whatever.

this would instead be 30 mins to an hour of work in vim, and it would be incredibly
boring and tedious work. not only that, it's also incredibly brittle. agents
basically never make syntax errors, don't accidentally break typing conventions,
don't forget to add doc strings (they might even add too many doc-strings), and
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

curl request (and similar things like pings and remote ssh calls) sit in this
sweet of ergonomics for agents, because they're pretty simple (the grammar),
but are very tedious to type out. llms these days have good enough instruction
adherence that i've never seen them mess up writing a curl request to some
link, using some auth, with some args. doing that manually takes a minute.
doing it with the llm while some of these things are already in context,
takes about 10 seconds.

same with scp'ing files

same with running a small number of tests that i don't want to manually
specify, but have a describable category ("run all of the tests for the backend
we just fixed in a tmux session").

using agents instead of writing automated scripts for this kind of thing is
nice, because it:

a. doesn't cost much, at all

b. is pretty reliable, or at least only ever wrong in an obvious way.

c. cuts down on script bloat.

for this project, i had to manage two machines (since lean3 did not work on my
main mac dev machine), so i was constantly running tests on my devbox.

problem is, i hate working on my dev box, so i frequently would just ask the llm
to pull the project on the other machine, and do this inconvenient test for me.

couple of ssh -c commands later, and we're done.

i also had a plethora of different models to test out, but was way too lazy to
look up how to make a request to them (stored in a dedicated endpoints.py file
in my repo) (string matching is hard for my fallible human brain). agents are
basically perfect for this kind of stuff.

--------------------------------------------------------------------------------

## VIII. so why did the agents work for me and not for others?

### 1. because i know what i am doing

i knew ahead of time what the project was going to look like. it was going to
look like 4 different backends for compilers, with a basic system for verifying
installations, a templating entrypoint for setting up the compile step and the
compile step itself. 

i wrote the first lean implementation by hand, and knew what i wanted the abstraction
of that backend to look like.

this means that i can just hit play, and reject or accept. there is no
cognitive load of wondering if this design pattern will work or not, i already
__know__ it works and this comes from experience of actually having to write
this kind of code myself before.

this also means that i have to reject about 50% of the things the llm gives me,
but that's why we have git worktrees and parallel agents. guess how many
agents i run at the same time on average![^1]


### 2. because i am extremely disagreeable

llms are slimy bastards. they appeal to 'best practices' and 'industry
standards' when all they do is write 50 line functions to do index an array
safely, with a 30 line docstring and an additional test.

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

so the answer is obvious: __include__ the good code in the context, slap in a repo
i'm proud of, or reference a codebase i like (usually tinygrad) and i'll
generally have a great time.

--------------------------------------------------------------------------------

## IX. but are agents worth the money?

so in total, for this project, i've spent:

- 100 dollars  [claude code](https://www.claude.com/product/claude-code) (claude max)
- about 20 dollars on [codex](https://openai.com/codex) (gpt tokens)
- 20 bucks on [slate](https://randomlabs.ai/)

so, why multiple and not just one?

### 1. claude code, the useful idiot

claude code is easily the most successful and popular agent product (despite the fact that
it is overpriced, probably not in small part due to its high demand). so why is that?

the bounds of claude code, even at the tool level, are very clear. permission
levels for commands, file reads/writes, very careful separation between human
and llm generated content (with the adorable claude commits).

when i give a prompt to claude code, and it's reasonably detailed, and the repo is easy
to navigate, i can trust that that task will get done.

all of that is to say: claude code is __reliable__.

as a piece of software, it's the most well thought through. the UX is quite nice (owing
probably not little to the fact that it shipped early, and has shipped updates
frequently since)

but that is not to say that it is perfect: claude's kind of an idiot at times.
it requires excessive hand holding for anything more difficult than a minor
fix. bad code style, such as the pervasive over-commenting and over-abstracting,
mostly comes from claude code.

if i want to do exploratory work (say, with a specific direction to
parallelize the compilation steps in minif2f), claude code __will not__ be
able to do this for me. it'll give the veneer of having made the attempt, and
then nothing works. (there's still a dangling async mixup left in the isabelle
backend that i need to get around to fixing)

claude code is also the most likely to attempt to cheat, out of the three
products, which is why i read the PRs from claude code very carefully to make
sure that no such cheating has been done[^4]. give me the serialized outputs
and inputs, or give me death.

and as previously mentioned, claude code is also very expensive. i run out
of usage on my max subscription within a day or two of focused programming.


### 2. codex, the idiot savant

i don't really like codex that much. and i think this owes mostly to:

codex being very opinionated about how it likes to solves problems. while ALSO
not giving many natural windows to insert instructions.

whereas cc will pause basically after every step to ask for my opinion on a
diff, or before running any command, codex will just go at it for 10-30 minutes
at a time.

which, feels great! ... if codex actually got it right the first time (and it
does, to a reasonable degree). but on the off-chance that it didn't, well
that's about a half a dollar and 30 minutes wasted.

i think a workflow like codex is ultimately what you want long term, with more
detailed specs on the user-end and increasingly less user interaction after
that. but until we have those models (and i have reason to believe we won't get
them for a hot minute (future blog)), codex feels like a tool that
overcommitted to a local minima.

that said, codex does give the best code out of the three agents i've used. when
it works, it really does work[^2].

### 3. slate, the idiot who went to get accommodations 

as an agent product, i think slate is the __best designed__ one i've used.

it's the best at handling extremely long turns (i very rarely need to reset
context when using slate; codex lasts a single shot, and claude code is about 5
shots on average).

it's the best at actually using the computer given (no need for a SLATE.md to
tell it how to type check or lint), and intuitively understands the workflow
required to implement a new feature (most of the heavy refactors and debugging
sessions that i did were with slate). as a pair programmer product, it's about
as useful to me as talking back and fourth with opus 4[^3].

it's unclear to me how much of this is over-fit to the kind of engineering that
i do in python (i'll soon be using these agents for writing medium scale
projects in slightly esoteric languages like lean/gleam). so expect another
blog by that point.

that said, being an early piece of software, it's not the most stable at the moment.
jittery UI, lack of visibility into llm state, QOL stuff like fuzzy file finding,
or editing / managing prompts are some things that i'd love to have in the tool.

but i have high hopes for the challenger. the developers i've spoken to from this
team are some of the most clear minded on llm-forward design i've seen in the
industry.

--------------------------------------------------------------------------------

## X. closing thoughts

so what have i learnt?

- formal language tooling is horrendous: these compilers are slow (especially
when scaled up), difficult to work with, and have such clunky syntax that llms
(and myself) struggle to write anything coherent in them. i have especially
high hopes for lean4, particularly in conjunction with llms, given the momentum
that it's getting in the industry.

- hard things are still hard: load bearing code remains to require
disproportionally more effort than other work. llms may reduce the friction of
learning how to write this code properly, but i still ultimately have to be the
one to do it.

- bullshit can be much easier: so much of unix tooling from the 80s is overly
verbose, under-documented, and generally not nice to work with (ah yes, i love
learning 50 different tools to convert between basic data formats). llm agents
basically turn all of those tools into one, with nobs i can verbally dial.

- we're incredibly early: even with current day llms. i can see these tools
shaping up to be orders of magnitude more reliable, fast and powerful. we're
past the point of {X}-of-thought, and now in the stage where people genuinely
see the shape of how llms fit into actual software workflows, and designing
tools to best make it fit.

--------------------------------------------------------------------------------

[^1]: if it's not obvious, the answer is two

[^2]: it's about within 90% of what i would've written myself. the model is very smart.

[^3]: that is to say, __very__.

[^4]: such cheating might include but is in no way limited to: hard coding
    tests, abusing defaults to break upstream code, writing a bunch of
meaningless nonsense to pretend that it's written tests, "# this is only a
partial implementation (though this one has gotten much better with recent
models)", overuse of try excepts instead of simplifying control flow.
