---
title: llm is the new unix hood classic
---

### [[index|supaiku dot com]]

<h1 onclick="document.getElementById('darkmode-toggle').click(); return false;">
llm is the new unix hood classic
</h1>

---
> i am become grep, the curler of worlds
---

[llm](https://pypi.org/project/llm/) is a ~new cli tool made by [simonw](https://en.wikipedia.org/wiki/Simon_Willison) that lets you use llms from a ton of providers (including local) in the terminal. 

you can pipe stuff into it, for example, to get the tldr of this article:

> curl https://supaiku.com/llm-unix | llm -s "tldr this essay please"

**this makes it absurdly powerful.**

i think your computer should come with it. like sed, curl, grep, cron, or vim.

here's some fun stuff i've found i can do with it.

---

## summarization d(a)emon

have you ever **READ**?

would you like to never **READ** anything ever again?

introducing

> llm -s "summarize this into bullet points, provide urls where appropriate"

[orange site](https://news.ycombinator.com/) bad, yes yes, but what if you wanted to get some news from it?

simply pipe it in

> § curl https://news.ycombinator.com/ | clean-html | llm -s "summarize this into bullet points, provide urls where appropriate"
>
> ===========================================================================
>
> Here are the top news stories from Hacker News in bullet points, with URLs where appropriate:
>
> **Prevention of HIV**: A new article on Science.org explores the latest research and advancements in preventing HIV. [https://www.science.org/content/prevention-hiv](https://www.science.org/content/prevention-hiv)
>
> **Tony Hawk's Pro Skyrider**: The creator of Tony Hawk's Pro Skyrider game is seeking feedback from users. [https://icode4.coffee/2023/02/16/Tony-Hawks-Pro-Skyrider-Feedback.html](https://icode4.coffee/2023/02/16/Tony-Hawks-Pro-Skyrider-Feedback.html)
>
> **Puppeteer Support for Firefox**: Mozilla has released Puppeteer support for Firefox, allowing developers to use the popular testing tool with their browser. [https://hacks.mozilla.org/2023/02/puppeteer-support-for-firefox](https://hacks.mozilla.org/2023/02/puppeteer-support-for-firefox)
>
> **How French Drains Work**: A new article on Practical Engineering explains how French drains work and when they might be used. [https://practical.engineering/how-french-drains-work](https://practical.engineering/how-french-drains-work)
>
> **Show HN: 3D Apartment Generator**: The creator of a web app that generates 3D apartments is seeking feedback from users. [https://roometron.com/](https://roometron.com/)
>
> **Official Proposal for Type Unions in C#**: Microsoft has proposed type unions for C#, a feature that would allow developers to specify multiple types for a variable. [https://github.com/dotnet/csharplang/issues/134](https://github.com/dotnet/csharplang/issues/134)
>
> ===========================================================================

## "hmm i wonder what anime spike is watching right now" 

llm eats rss feeds for breakfast.

take an rss url, for example my mal rss feed: https://myanimelist.net/rss.php?type=rw&u=spikedoanzz

curl into rss cleaning tool into llm

> § curl "https://myanimelist.net/rss.php?type=rw&u=spikedoanzz" | clean-rss | llm -s "what anime is this person watching"
>
> ===========================================================================
>
>This person is watching several anime shows, but here are the ones they seem to be actively following:
>
>1. **Monogatari Series: Off & Monster Season**: Watching, but not sure how many episodes are in the season (5 of ?).
>
>2. **Tokidoki Bosotto Russia-go de Dereru Tonari no Alya-san**: Also on episode 5 of 12.
>
>3. **Make Heroine ga Oosugiru!**: On episode 3 of 12.
>
> ===========================================================================

this works for all sorts of rss feeds. go crazy.

here are some of my favorites:

https://www.technologyreview.com/feed/ 

https://www.dwarkeshpatel.com/feed     

https://longnow.org/ideas/rss/

---

## vibe checker

short and sweet, code and writing sanity checker in the terminal.

cat, pipe, edit, repeat.

> cat llm-unix.md | llma -s "proofread this real quick, whatever you respond with will be put into the vibe check section obviously"
>
>
> ===========================================================================
>I've reviewed the content and it looks good overall. Here are a few minor suggestions:
>
>1. Consider capitalizing "LLM" consistently throughout the text, as it's an acronym.
>
>2. In the "summarization d(a)emon" section, you might want to capitalize "READ" for consistency with the second instance.
>
>3. The "vibe checker" section is quite short compared to the others. You might want to expand on this idea a bit more or provide an example of how it can be used.
>
>4. Consider adding a brief conclusion or wrap-up section to tie everything together.
>
>Overall, the content is engaging and informative, with a good mix of humor and practical examples. The formatting and structure are clear and easy to follow.
>
> ===========================================================================

---

if you have any questions, suggestions or feedback, do DM me over on [twitter](https://x.com/spikedoanz)
