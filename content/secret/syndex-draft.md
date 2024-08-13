# Syndex

A syndex is a (syn)dicated-in(dex), aka a distributed bookmark.

This repository contains the spec and draft implemenentation of syndex the cli and syndex the browser extension.

---

## 1. RSS spec

Everything in the [RSS spec](https://www.rssboard.org/rss-specification) is accepted. Though this is the standard:

- title: whatever you want
- link: url to wherever you're hosting the syndex/path-to-xml-file.xml
- description: whatever you want

- Every bookmark is just an item in an RSS feed. Minimal requirements are:
    - link: ```<link>url to bookmark that can be curled</link>```
    - THATS IT
    - Optional tags (syndex includes these by default):
        - title: human / llm readable text, default: ```<title unspecified="true" />```
        - description: human / llm readable text, default: ```<description unspecified="true" />```
            - if bookmarking tweets, contents go in here
        - pubDate: bookmarked time

Everything is super loose because everything should work with llms.

You can spread things out to as many files you want (TODO: is this ideal or is a single feed better?) (I'm leaning towards single feed)

## 2. Git commandments

0. Don't commit links that might rot. They will be autodeleted on a cycle.
1. Never commit links that cannot be curled (reddit, twitter, etc)
2. If you must commit links that cannot be curled, archive them yourself, or embed them in the description.
    - TODO: need a spec for twitter and reddit

## 3. Syndex, the cli 
- Syndex the cli is a minimal command-line interface (CLI) which provides three functionalities:
    - bookmark : creates an item in a the rss file with some title and some description (optional in that order)

```bash
        syndex [file-path] [url] [title] [description]
```

    - validation: -v --validate:  will check if links are curlable

```bash
        syndex -v [file-paths]
```

    - listen: -l --listen: will start a local http server which lets you append things to the rss file.
```bash
        syndex file-path -l
```

## 4. Syndex, the browser extension
- Syndex the browser extension is also a minimal piece of software that simply:
    - Yanks whatever url you're currently on
    - Gives you a box to insert a title, description
    - Formats a curl request, sends it off to listening syndex cli session.

## 5. Forking

Syndexes can be extended by forking them through github.

They can be combined by creating multi repos.

## 6. User Space
- All downloading, filtering, and search tools should be implemented in the user space, independent of the spec in this document.
    - TODO: Search
    - TODO: RAG
    - TODO: Recommendation

## 7. Community managed syndexes
- Software that lets people merge two syndexes automatically would be interesting:
    - Deduplication.
    - PRs as the system to insert new bookmarks.
    - Train a model to learn how to do PRs -> Autofiltering preference model?
