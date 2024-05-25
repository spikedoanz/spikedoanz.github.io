---
title: Life without sudo
---

# Life without sudo

---

So I have [this](https://www.apple.com/az/macbook-air-13-and-15-m2/) work laptop, and IT refuses to give me sudo access (admin privileges). This article catalogs my ongoing journey to turn it into a workable computer without needing sudo.

This article might also prove useful for you if you're working on a cloud instance and need some work tools.


## Ingredients ##
- M2 Air 24GB
- MacOS
- Terminal.app
- Chrome

## Recipe ##
Here are the things I need from a computer. This is immensely trimmed down and I don't expect this to be the only things people need from their computer, but it works for me.
- A sane browser (chrome is pre-installed, yippie)
- A sane terminal
- A sane IDE
- Multiplexer/Window manager
- Various tools
	- compilers (rustc, gcc, ghc, ...) 
	- package managers (cargo, conda, pip, ...) 
	- htop, or an equivalent 
	- keybinding mods (kmonad, ...)
- LLM runtime

## Cooking ##
### Package manager ###
[Brew](https://docs.brew.sh/Installation#untar-anywhere-unsupported): While the intended way to install brew requires sudo, there is technically an unsupported way to get brew into the system without needing sudo:

[Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html): the rust people are famous for writing everything from scratch. Some of this software is even good (see next section)! Fortunately, all of this software is intended to be installed exclusively in userland:

[Conda](https://docs.anaconda.com/free/miniconda/index.html): 99% of my work is ML, so I'm basically chained at the ankle to python and its ecosystem. This one is easy:

### Terminal ###
Terminal.app is honestly terrible. Let's try something different. I daily drive kitty on most systems, but let's give alacritty a try.
```
cargo install alacritty
```

### Multiplexer ###
I've had some issues trying to install tmux through brew (something related with having to give openssl privileges). So I've been using an [zellij](https://zellij.dev/), and it's been a pleasant experience.
```
cargo install zellij
```

### Editor ###
Nvim cannot be installed through normal means, so we'll need a workaround. Fortunately, the rustaceans gave us another way out, called [bob](https://github.com/MordechaiHadad/bob).
```
cargo install bob
```

Nvim doesn't really have all the bells and whistles I want from an editor, so let's spice it up with [nvchad](https://nvchad.com/)
### Misc ###
Some other stuff I found to be really helpful that were also installable without sudo:

[ytop](https://github.com/cjbassi/ytop), a htop alternative

[ghcup](https://www.haskell.org/ghcup/), for haskell stuff

[jdk](https://stackoverflow.com/questions/2549873/installing-jdk-without-sudo), because I'm reading [Crafting Interpreters](https://craftinginterpreters.com/)

## Appendix ##
While technically all of this software can be installed by simply compiling them from source, I am a lazy bastard and the thought of git cloning and building all of my software from source strikes dread in my heart. 

---

last update: 2024-05-03
