---
title: how i self hosted zulip and escaped the permanent underclass
description: when stomped on by technocrats, don't complain about the taste of the boot
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
how i self hosted zulip and escaped the permanent underclass
</h1>

--------------------------------------------------------------------------------
> when stomped on by technocrats, don't complain about the taste of the boot
--------------------------------------------------------------------------------

## some compelling reasons to get off of discord

before we continue, let's first discuss the colorful set of reasons why discord
is a careless, misaligned and untruthworthy company that you should not rely
on. a tally of some shenanigans they've been up to:

- [getting hacked and leaking ~70,000 users' IDs, selfies and billing
  info](https://www.newsweek.com/discord-age-verification-face-scan-controversy-11494375)

- [rolling out mandatory age verification via face scans and government ID
  uploads — right after said
  hack](https://proton.me/blog/discord-global-age-verification)

- [kneecapping unverified users to an age restricted experience](https://proton.me/blog/discord-global-age-verification)

- [getting sued by new jersey for marketing itself as a "safe space for teens"
  while letting predators run wild on the
  platform](https://www.nj.gov/oag/newsreleases25/2025-0417_Discord_Complaint.pdf)

- [making nitro cancellation so deliberately convoluted it spawned youtube
  tutorials and a class action
  lawsuit](https://socialmediavictims.org/discord-lawsuit/)

- [openly admitting they expect to lose users over this and saying "we'll find
  other ways to bring users
  back"](https://www.newsweek.com/discord-age-verification-face-scan-controversy-11494375)

--------------------------------------------------------------------------------

## escaping the permanent underclass

### 1. self hosting is neither scary nor expensive

to host something like zulip, you fundamentally need two things:

- a potato (basically any computer that has a heartbeat).
- a static ip address to host off of.

my solution to both of these is to just use
[hetzner](https://www.hetzner.com/)[^1]. the 5 dollar a month node with 2 vCPUs
and some integer gigabytes of ram is more than enough to host a zulip instance
for up to 100 people.

basically just sign up, put in some credit card [^2], pick the node you want,
and you'll get some ssh credentials and an ip address. couldn't possibly be more
straightforward even if you tried.


--------------------------------------------------------------------------------

### 2. asking claude[^3] to set up the zulip server for you

step 1: ssh into the server

step 2: point claude at the [zulip self hosting
docs](https://zulip.com/self-hosting/)

step 3: do whatever claude says[^4]

step 3.5: this is optional, but you can also use an email hosting service like 
mailgun to handle signups emails.

step 4: there is no step 4. you now have a self hosted zulip server, congrats!

--------------------------------------------------------------------------------

### 3. get a domain (if you care)

after you're done with step 2, you technically do have a zulip instance up and
running, but it'll be accessed via something like http://100.101.81.30:8080/,
and i don't know about you, but i don't want to click on a chat service that
looks like that.

the solution: go on namecheap, or godaddy, or whatever, and buy a domain for
like 7 bucks (a year). just buy a simple dot com or dot org. checkout, boom,
done.

then, tab back to the claude session, and type in the magic words:

```
hey uh i just bought the domain from namecheap, how do i link it to my zulip
session. thanks i love you
```

and claude will guide your hand through the rest.

--------------------------------------------------------------------------------

## why should you go through the effort of any of this?

i've already listed out my case for why you should stop using discord, but why
should you use zulip in particular? instead of irc, or matrix, or slack, or
going outside and meeting with friends in person?

well a couple of reasons:

1. you own literally all of the data: everything is hosted off of a sqlite db
   that you can cache, read, backup, ... to your hearts content. there's also
   less concern of a custodial service (like discord), snooping into your
   server to train some AI models or whatever.

2. among all of the chat software alternatives, zulip is the closest to getting
   to feature parity with discord, while avoiding the issues that got you into
   the discord problems in the first place (not owning the platform). irc
   doesn't have image embeds, matrix doesn't have a functional phone client,
   slack is just not open source (and also they can see your messages if they
   want), etc etc. i've tried the rest, and found zulip to be the most
   functional choice out of everything.

3. the zulip search bar is blazing fast (probably because your server isn't
   being multi-tenanted with 2000 other servers). 

4. everything being organized into hierarchical threads, makes links and
   citations extremely easy. here's the actual link to one of my math reading
   threads on my server:
   https://chat.syndecate.org/#narrow/channel/6-math/topic/spike-reading-the-blind-spot

5. there are [__vim bindings__](https://zulip.com/help/keyboard-shortcuts)

6. it's remarkably fast. it's faster than basically anything that isn't plain
   irc from my experience. if you're migrating from discord, welcome to the
   world of functional software.

--------------------------------------------------------------------------------

## the costs

we obviously can't have good things for nothing, so what's the catch?

well, here's the tally of costs for my setup process:

- the hetzner node itself: fixed 5.50 dollars a month
- the domain: ~1.3 dollars a month
- time: 2 hours (lazily copying things back and forth with claude)

and there are genuinely some features missing from discord that you'll need to
provide yourself:

- voice / video / streaming: the big missing feature from discord. however, i
  don't really miss this, since discord's voice and video has always been
  completely kneecapped for everyone who wasn't shelling out money for discord
  nitro. i just use google meets instead. the migration was recent, and my
  server is exploring alternatives, i'll give an update when a suitable option
  is found.

- backups: probably the biggest one. you're responsible for the node. if it
  dies or gets corrupted, the server is gone. if you don't like sysadminning
  (or paying claude to do it and all the risks that come with that), then this
  is likely not the option for you.


online communication is an immense part of my social life, and relying on
discord for all of this was a massive liability. 

compared to the rest of the services that i pay for, like spotify, netflix, or
god forbid a latte at a mid coffee shop, buying back complete control and
reliability over my communication channels for just 7 bucks a month is a
complete steal.

alternatively, you can also just use a free tier from zulip themselves[^5], but
then you're back in the original position of being reliant on a service
provider to keep the lights running, which for me, is a tradeoff i never want
to make ever again in software.

--------------------------------------------------------------------------------

## appendix

[^1]: i'm not sponsored by any of the services mentioned btw. i just like using
    them.

[^2]: btw for cloud businesses. __always__ use a virtual card with a spend cap
    so you don't have bills blowing up your account.

[^3]: or any llm of your choosing

[^4]: please be somewhat careful when setting up the auth and handling ssh
    permissions into the server. if you don't know how to handle this, you
    should pay zulip to deal with it instead; they're a good company.

[^5] https://en.wikipedia.org/wiki/You_are_the_product
