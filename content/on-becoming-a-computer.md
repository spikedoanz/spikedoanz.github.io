---
title: on becoming a computer
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
on becoming a computer
</h1>

---
> I've been using tmux a few months now and I've never felt better. I have more
> energy. My skin is clearer. My eye sight has improved. 
---

a lot of the improvements that i've made to my workflow as a programmer has
been to look at what i'm doing and asking 'how would i programmatically do this
instead?'. for instance, i spend a lot of my time laying out my tasks for the
day, and decomposing the tasks (which itself helps me understand the tasks, and
subtasks involved much more clearly) until they become 'atomic' tasks that i
can quickly do and tick off. finish a task, go back to scheduling, repeat for 8
hours.

for most of my earlier years i did this implicitly: i would mentally note all
the tasks i'd have to do, then do an intuitive estimation of the time and
effort it would take, plus their relative urgency, and then rank order them
into actual todos.

this was nightmarish! i would get distracted all the time; have a bunch of
unfinished tasks all over the place; i'd have no idea what task i was doing
next right up until the 30 seconds i was actually doing it. i don't think i
even really had enough clarity when i was that age to properly verbalize how i
was (poorly) doing this planning process.

so obviously, if the problem is resource tracking, then the solution is to
track it to some kind of reliable ledger, a.k.a 'a todo list'. i think it's
actually somewhat telling that the telltale beginner programmer piece of
software is a todo list. i mean if you had to think about what piece of
software would be most useful for someone without a dedicated area of expertise
, it would be some kind of generic planning and note taking software -- todo
lists, journals, task trackers, and so on.

the first piece of task tracking software i can remember using was notion. i knew
basically jack all about software at the time, and notion looked pretty good.
the funny part is that i never used any of the fancy features like tables or
programmatic whatever thingamabobs that notion offered. i only ever used the
checklists, and @time macro (which just gets replaced with the current time).

then about one or two years later, i switched to linux, and promptly quit
notion. i don't exactly recall why, but i suspect it was because i got
enamoured by the search tools available in the terminal. i remember trying to
export notion to a local file one time and ending up with a pile of gibberish
that couldn't be parsed with grep, or plugged into a different piece of
software while retaining all the nice formating and such. it was a pretty
jarring, offensive experience, so i switched over to obsidian + markdown
instead.

at first, i loved using the markdown hyperlink feature. i would link every noun
to an article, and see the pretty graph show up in the graph view; jumping
around hyperlinks was also pretty fun. but ultimately, i never used the graph
for anything interesting, so i eventually stopped using that too.

earlier last year (2024), i realized that i was only using obsidian because it
was a note taking app that had vim bindings. i was already using neovim as a
primary editor. and on top of that i had many qualms with obsidian, like how
file syncing across devices was a pain. i've never had that issue with my code
in vim + git. so naturally, i switched over to just using vim.

this was a pretty huge unlock! searching now felt fully natural and native with
[ripgrep](https://github.com/BurntSushi/ripgrep) and
[fzf](https://github.com/junegunn/fzf). switching between files also felt
natural. it was here that i started coming up with my own dsl for tagging
tasks, inspired by john carmack's [plan
files](https://garbagecollected.org/2017/10/24/the-carmack-plan/). basically
just markdown + some conventions for organizing a file into subsections +
bootstrapping off a [markdown lsp](https://github.com/artempyanykh/marksman) to
get some qol nicities.

this, plus llms, made me a much more principled and efficient person across the
spectrum. it was also nice seeing the commits pop up on github. it felt like i
was playing an rpg and hitting a checkpoint every time i commit+push.

---

the next big unlock was tmux. i'd been an on and off user for a while, but
never understood the point of tmux until: a. i rebound the leader key to Ctrl-a
(no really, who the hell thought Ctrl-b was a good idea), and b. i learnt how
to use tmux sessions (specifically, easily creating, renaming, and switching
between sessions). this turned tmux into not just a terminal session manager,
but also a process manager for my own brain. i could now dedicate a session per
task, have a plan file open on each, and be able to reference them globally
with my daily / weekly plan file. this also made it extremely nice to work with
claude code. for the brief period in which i had infinite claude credits, this
workflow made me feel like i was working at peak human efficiency.

the tmux + vim + plan file combo is now an integral part of my workflow.
(probably will write a detailed blog about this in the future). and the point
where i realized i was going to stick to this long term was thinking about
myself more and more as a computer: i, the programmer person, am essentially a
single threaded os. the task i'm currently doing is essentially the 'process'
that i'm 'running', with varying amounts of mental resources allocated to that
task. if i'm dedicating any amount of mental effort at all to this book-keeping
'process', then that's fewer mental resources i can allocate to the task at
hand. it's like having htop on your screen at all times. that's silly!

i'm still working on more ways to programmatically plan out my life. now that i
have a process scheduler, maybe i need finer grained resource management (maybe
time tracker?, key logger?). for the former, i've very recently started using a
[activity watch](https://activitywatch.net/) to catalog how much time i spend
on various windowsa and browser tabs, and am excited to see how this might fit
into the rest of my workflow. (getting full coverage tracking of all my
computer actions also flows naturally into cloning myself in the future. but
that's a problem for spike 1.0)
