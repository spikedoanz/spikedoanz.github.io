---
title: rocq vscode guide
description: minimal instructions to get rocq working on a computer
---

### [[index|all rocq and no play makes spike a dull boy]]

<h2 style="text-align: center;" href=""
onclick="document.getElementById('darkmode-toggle').click(); return false;">
all rocq and no play makes jack a dull boy
</h2>


--------------------------------------------------------------------------------
```
                        all rocq and no play makes jack a dull boy
                        all rocq and no play makes jack a dull boy
                                  all rocq and no play
                                  makes jack a dull boy
                                  all rocq and no play
                                  makes Jack a dull boy
                        all Roq  and no play makes Jack a dull boy

                        all coq  and no PAY  makes JAck a dull boy

                        all rocq and no play makes Jack a dull boy
                        all rocq and no play makes Jack a dull boy
```
--------------------------------------------------------------------------------

it's been a longtime observation of mine, that the better you get at computer
science, the worse you actually get at software. take for instance, my two
favorite slop languages: python and go, universally derided as some of the
worst designed languages ever, serves as the glue layer for basically all of
modern software. no matter how hard you try, you'll get some python and go in
prod.

when was the last time you ran a piece of software in lean? or idris? or coq?
personally? besides the stuff i write myself? basically never.

maybe some of you run xmonad or something, and so touch haskell.[^1]

before i got into
[plt](https://en.wikipedia.org/wiki/Programming_language_theory) myself,
coq[^2] has always been this kind of boogeyman. the syntax looked completely
alien, the kinds of stuff people did in the language seemed like stuff you
needed a PhD in pure math to understand, and the IDEs, god the IDEs. zoomers
like me (at the time) with blazed out neovim setups would cower in fear at the
sight of the most user friendly interface people used for coq.

for reference, here's what the first party coq IDE looked like:

![a screenshot of the coq
ide](https://rocq-prover.org/doc/V8.19.0/refman/_images/coqide.png)


however, as the years passed, i eventually did face various relatives of the
boogeyman. his nephew: haskell, wasn't really that bad. his gen alpha brainrot
grandson: rust, was actually pretty delightful to spend time with after i got
past all of the insider jokes. my favorite is probably sister in law:
idris[^3].

but, to be completely honest, it wasn't until i met his younger brother, lean,
that i came to realize that, y'know, maybe uncle coq wasn't so intimidating
afterall.

i actually like lean a lot! it's a great language for doing math proofs. it's
also pretty ergonomic for some [intermediate
programming](https://github.com/spikedoanz/LeanLox) (albeit, without very strong
proof tech for generic programming)

however i am a filthy software engineer. and unfortunately, doing algebra and
analysis really isn't part of my job description.

so i set out on a search for a proof language that did have better tooling for
software verification, and before i knew it, i was back at uncle coq's
doorstep.

how hard can it be! i can basically read coq now! i even know some type theory!
even some category theory!

then i was faced with the horrifying lesson that, math is, in fact, easier than
software.

--------------------------------------------------------------------------------

## step 1:


--------------------------------------------------------------------------------

## appendix

[^1]: what they don't want you to know is that haskell is also a slop language.

[^2]: name pending rebranding into 'rocq', so please use that name, unless if
    you're a piece of software written by or for coq, in which case please don't
    change the name because that would be confusing.

[^3]: which is shaping up to be my favorite programming language ever. but for
    the current lack of tooling. all it really needs is a strong industry player
    like jane street for ocaml and it'll wipe the competition of the map.
