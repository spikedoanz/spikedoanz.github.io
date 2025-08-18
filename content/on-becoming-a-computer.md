
---
title: on becoming a computer  
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
teplatem
</h1>

> I've been using P̶y̶T̶o̶r̶c̶h̶ tmux a few months now and I've never felt better. I
> have more energy. My skin is clearer. My eye sight has improved. 
>
> A̶n̶d̶r̶e̶j̶ ̶K̶a̶r̶p̶a̶t̶h̶y̶ me

a lot of the improvements that i've made to my workflow as a programmer has
been to look at my asking 'how would i programmatically do this'. for instance,
i spend a lot of my time laying out my tasks for the day, and decomposing the
tasks (which itself helps me understand the tasks, and subtasks involved much
more clearly). 

for most of my earlier years i did this implicitly: i would mentally note all
the tasks i'd have to do, then do an intuitive estimation of the time and
effort it would take, and then rank order them into actual todos.

this was nightmarish! i would get distracted all the time; have a bunch of
unfinished tasks all over the place; i'd have no idea what i was doing next up
until the 30 seconds i was actually doing it. i don't think i would even have
enough clarity when i was that age (probably early teens?) to properly
verbalize how i was doing this planning process.

so obviously, if the problem is resource tracking, then the solution is to
track it to some kind of reliable ledger, a.k.a 'a todo list'. i think it's
actually very telling that many beginner programmers start out writing software
for todo lists. if you had to think about what piece of software would be most
useful for someone without a dedicated expertise would be, it would be planning
and note taking software -- todo lists, journals, task trackers, ... 

the first piece of task tracking tool i can remember using was notion. i knew
basically jack all about software at the time, and notion looked pretty good.
the funny part is that i never used any of the fancy features like tables, and
programmatic whatever thingamabobs that notion offered. i only ever used the
checklist, and @time macro (which just gets replaced with the current time).

then about the same time i switched to linux i quit notion. i don't exactly
recall why, but i suspect it was because i started getting enamoured by the
search tools available in the terminal. i remember trying to export notion to a
local file one time and ending up with a pile of gibberish. it was a pretty
jarring, disgusting feeling, so i started using obsidian instead.

at first, i loved using the markdown hyperlink feature. i would link every noun
to an article, and see the pretty graph show up in the graph view; jumping
around hyperlinks was also pretty fun. but i never used the graph for anything
interesting, so i eventually stopped using that too.

earlier last year (2024), i realized that i was only using obsidian because it
was a note taking app that had vim bindings. i was already a primary neovim
user. and i had qualms with obsidian, like how file syncing across devices was
a pain. i've never had that issue with my code in vim + git. so naturally, i
switched over to vim + cli.

this was a pretty huge unlock! searching now felt fully natural and native with
ripgrep and fzf. switching between files also felt natural. it was here that i
started coming up with my own dsl for tagging tasks, inspired by john carmack's
[plan files](https://garbagecollected.org/2017/10/24/the-carmack-plan/).

this, plus llms, made me a much more principled and efficient person across the
spectrum. it was also nice seeing the commits pop up on github. it felt like i
was playing an rpg and hitting a checkpoint every time i commit+push.

the next big unlock was tmux. i'd been an on and off user for a while, but
never understood the point until: a. i rebinded the leader key to Ctrl-a (no
really, who the hell thought Ctrl-b was a good idea), and b. i learnt how to
use tmux sessions (specifically, easily creating, renaming, and switching
between sessions).

the tmux + vim + plan file combo is pretty much an integral part of my workflow
now. (probably will write a blog about this in the future). and the point where
i realized i was going to stick to this long term was thinking about myself
more and more as a computer: i, the programmer person, am essentially a single
threaded os. whatever task i'm doing, is essentially the process that i'm
running, with a varying amount of mental resources allocated to that task. if
i'm dedicating any amount of mental effort at all to book-keeping what i'm
currently doing, then that's fewer mental resources i can allocate to the task
at hand. it's like having htop on your screen at all times. that's silly!

i'm still working on more ways to programmatically plan out my life. now that i
have a process scheduler, maybe i need finer grained resource management (time
tracker?, key logger? calorie counter? (probably overkill)). very recently,
i've started using a [time tracker](https://activitywatch.net/) to catalog how
much time i spend on various windows, and am excited to see how this might fit
into the rest of my workflow.
