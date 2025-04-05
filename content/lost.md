
---
title: how to never be lost
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
how to never be lost
</h1>


---
> knowing what you are doing is usually the fundamental bottleneck for both research and engineering.
> so what if you just never got lost?
---

over the course of doing many projects over the years, i've come to realize that the limiting factor
to whether i can get something done or not is directly proportional to how well i understand the task
that i am doing.

resources and manpower are also usually not a limiting factor, because "knowing what i'm doing" works
out very well when it comes to getting compute or help from coworkers and friends and so on.

therefore, i've developed a routine that prevents me from getting lost in a project no matter how
daunting it seems at first. this article details that routine.

---

## 1. there are no shortcuts

while it may be tempting to take on "technical debt", either by using prepackaged solutions, or by asking
your local llm to solve your problem for you, i've found that this strategy essentially never works out.
even when it does, it quickly comes to my attention afterwards that the task was not really worth doing in
the first place.

there is no substitute for this, you **have** to understand exactly what the task you're accomplishing is.
the ai will not **understand for you**

---

## 2. do the stupidest thing that works

a lot of projects i jump on (either for consulting, or because someone vibe coded a little too hard and now
the todolist app is 20k lines of 5 different languages that no one knows how to build) have this pernicious
habit of always jumping straight to the target without first going through intermediate steps.

technical projects basically can't be done like this. you almost always need to build a tech tree.
and the tech tree almost always should start at something incredibly "stupid".

but "stupid" here mostly means simple. but in the simplicity usually lies a lot of hidden complexity.
the famous "hello world" that everyone writes isn't actually supposed to be a full guide on how to program
in a new language. but what it does ensure, is that your tooling is perfect. doing a hello world means that:
- your computer works.
- your text editor works.
- you know how to operate said computer and text editor.
- you can compile the program.
- you can run the program.
- you've verified that you've run the program.

and most crucially of all, the stupid first simple thing has a core ingredient for the rest of your project:
**the iteration looop**

---

## 3. have a tight iteration loop

it goes by many names: dev cycle, feedback loop, etc.
there are infinite ways you could have your loop set up, but essentially the value metric of 
an iteration loop breaks down to a single paramter: latency. or in other words:

**how fast can you verify a change?**

i can't stress how important this is. every project you'll do will involve some hundreds, if not
thousands of changes from your starting point.
you will be compiling, running, deploying, batching, and whatever other verb in between making a change
and seeing that change on the screen over and over and over again.

every single second counts. scratch that, every single **milisecond** counts.

this is not just an experiential "nice to have".

a tigher dev loop gives you fundamentally new **capabilities**.

- an extremely slow dev loop (~ 10 minutes between iterations) means that you'll be spending a lot of idle time,
or be forced to complicate your tooling (you **need** a debugger, or a slurm queue manager, or some funky
looking dashboard to visualize your sparse outputs). you get maybe a couple dozen loops a day.

- a slow dev loop (~ 1 minute) means that you'll have a couple hundred loops a day. this lets you start branch
your experiments, and maybe start something like print debugging.

- a tight dev loop (~ 1 second) means that you can start spam programming. you can try thousands of things a day,
and here, llm tooling becomes really usable. (this is in large part why python has become so successful. it's a
slow language, but it has a very tight dev loop compared to compiled languages)

- an extremely tight dev loop (~ milliseconds) means that you can massivelly parallelize your experiments. grid
searches, codegen cranked to the max.

---

## 4. name a better combo than numbers and specs

you cannot know where you're going if you're blind.

in research and engineering writ large, knowing where you're going mostly comes down to:
- your spec: verifiable description of what you're trying to do.
- your measurements: verifiable numeric descriptions of what you're actually doing.

it is extremely important that both of these are well oiled, and must absolutely **not** be vibe coded.
