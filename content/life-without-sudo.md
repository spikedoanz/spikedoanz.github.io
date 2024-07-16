---
title: life without sudo
---

# life without sudo

---

so i have [this](https://www.apple.com/az/macbook-air-13-and-15-m2/) work laptop, and it refuses to give me sudo access (admin privileges). this article catalogs my ongoing journey to turn it into a workable computer without needing sudo.

this article might also prove useful for you if you're working on a cloud instance and need some work tools.


## ingredients ##
- m2 air 24gb
- macos
- terminal.app
- chrome

## recipe ##
here are the things i need from a computer. this is immensely trimmed down and i don't expect this to be the only things people need from their computer, but it works for me.
- a sane browser (chrome is pre-installed, yippie)
- a sane terminal
- a sane ide
- multiplexer/window manager
- various tools
	- compilers (rustc, gcc, ghc, ...) 
	- package managers (cargo, conda, pip, ...) 
	- htop, or an equivalent 
	- keybinding mods (kmonad, ...)
- llm runtime

## cooking ##
### package manager ###
[brew](https://docs.brew.sh/installation#untar-anywhere-unsupported): while the intended way to install brew requires sudo, there is technically an unsupported way to get brew into the system without needing sudo:

[cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html): the rust people are famous for writing everything from scratch. some of this software is even good (see next section)! fortunately, all of this software is intended to be installed exclusively in userland:

[conda](https://docs.anaconda.com/free/miniconda/index.html): 99% of my work is ml, so i'm basically chained at the ankle to python and its ecosystem. this one is easy:

### terminal ###
terminal.app is honestly terrible. let's try something different. i daily drive kitty on most systems, but let's give alacritty a try.
```
cargo install alacritty
```

### multiplexer ###
i've had some issues trying to install tmux through brew (something related with having to give openssl privileges). so i've been using an [zellij](https://zellij.dev/), and it's been a pleasant experience.
```
cargo install zellij
```

### editor ###
nvim cannot be installed through normal means, so we'll need a workaround. fortunately, the rustaceans gave us another way out, called [bob](https://github.com/mordechaihadad/bob).
```
cargo install bob
```

nvim doesn't really have all the bells and whistles i want from an editor, so let's spice it up with [nvchad](https://nvchad.com/)
### misc ###
some other stuff i found to be really helpful that were also installable without sudo:

[ytop](https://github.com/cjbassi/ytop), a htop alternative

[ghcup](https://www.haskell.org/ghcup/), for haskell stuff

[jdk](https://stackoverflow.com/questions/2549873/installing-jdk-without-sudo), because i'm reading [crafting interpreters](https://craftinginterpreters.com/)

## appendix ##
while technically all of this software can be installed by simply compiling them from source, i am a lazy bastard and the thought of git cloning and building all of my software from source strikes dread in my heart. 

---

last update: 2024-05-03
