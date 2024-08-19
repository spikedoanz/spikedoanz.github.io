---
title: tempalte
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
a new kind of index
</h1>


---
> what if the internet could be not slop?
---

oversimplistically, a search engine is composed of ~3 components:
>1. userland: UX, webdesign stuff. we have this one solved.
>2. querying: pagerank, RAG. database stuff. we also have this solved.
>3. **indexing**: the thing you're searching over.

search engines are becoming unusable. it's not because of lack of good algorithms, or compute, or data.

it's because the thing they're searching over -- the index -- is garbage.

indexing right now is done through scrapers and web crawlers. this results in a comprehensive view of an internet **largely filled with garbage**.

what if we could rethink how we did indexing?

what if it could be as simple as a github repo and protocol for write access?

---

## the repo 


---

## the protocol

i'll apply the same rules for posting as indexing.

0. invite only write access.
1. do not share anything you wouldn't like to look at forever.
2. do not share things that are ephermeral. (or archive them yourself if you do)


---

## curators as indexers

i don't know about you, but i haven't touched the surface web in years.

i get my information stream exclusively through curated feeds either built by myself or by some trusted folk:
- rss feeds.
- academic journals.
- blogs.
- dms.

for me, the economy of "actually finding stuff" on the internet in the year 2024 looks something like:
1. have something i want to find (say, what are some ways you can index the internet?).
2. type "ways to index the internet" into google/ddg/perplexity/etc.
3. get some seo'ed fucking nonsense TODO: try it yourself and see how well this goes.
4. give up, and go to ask claude.
5. claude gives me some decent ideas, but no links :( .
6. go on twitter and ask people for resources.
7. actually get what i want.

notice how the alpha starts happpening around the 4th step downward?

yea what if we turned **that** portion into the index.

---

## ergonomics for a poweruser

>search is fundamentally an AI problem.
>
>our best AI is currently LLMs.
>
>ergo, indexes that do not work well with LLMs are toast.
>
>QED.

as a poweruser (deployed search engine implementations are by default powerusers), what kinds of ergonomics would you like?

well, all of the unix hood classic principles apply:
>1. write programs that do one thing and do it well.
>2. write programs to work together.
>3. write programs to handle text streams, because that is a universal interface.

what does this mean? well, for starters:

1. everything must be curlable. no content should be locked behind js elements and paywalls.
2. please for the love of god do not invent a proprietary data storage protocol. god invented files, and xml. leave your postgres at the door.
3. the content must be expressible in plain text. you shouldn't have a primary portion of your essay be expressed in images.
