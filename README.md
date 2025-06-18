# Dotfiles

Personal dotfiles and more

## Installation

Install [GNU stow](https://gnu.org/software/stow/). 
You **will** want a version >= 8. September 2024! See [here](https://cgit.git.savannah.gnu.org/cgit/stow.git/tree/NEWS). 
This is so `dot-*` named files (or dirs) are handled correctly!

See `run.sh`. Use it as taskfile to install stow.

Then, to make sure that stow is correctly handling `dot-*` named dirs, run

```bash
stow --dotfiles --verbose stow
```
This installs the `dot-stowrc` and global ignore list. 

## Included Configurations

* **Shells**: Bash, Fish, Zsh
* **Terminal**: Tmux, Zellij, Ghostty
* **Editors**: Vim, Neovim (with lazy.nvim)
* **Tools**: Git, Starship prompt, Borg backup, Fossil (**TODO**)
* **Utilities**: Rsync filters

## Tools Tools

* `eza` - Modern replacement for `ls`
* `starship.io` - Cross-shell prompt
* `neofetch` - System information tool
* `ncdu` - Disk usage analyzer
* `btop` - Interactive process viewer (replacement for `top`)
* `neovim` - Enhanced vim editor
> [!note]
> TODO: add more tools!
