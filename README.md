# Dotfiles

A collection of configuration files for various tools and applications I use, with an installation script to easily set them up on new systems.

## Installation

### Clone the repository

```bash
git clone git@github.com:sebaschi/dotfiles.git ~/.dotfiles
```
{

### Install configurations

The `dot-install` script can be used to install specific configurations or all of them at once:

```bash
# Install everything
~/.dotfiles/dot-install all

# Install specific configurations
~/.dotfiles/dot-install git nvim tmux

# Install only bash aliases
~/.dotfiles/dot-install bash:aliases
```

Run `~/.dotfiles/dot-install` without arguments to see all available options.

## Testing

A test script is included to verify the installation script works correctly:

```bash
~/.dotfiles/test-dot-install
```

This runs the installation in an isolated environment to ensure all symlinks are correctly created.
Nothing fancy, just creates mock home in `/tmp` and changes some envars used by the install script.
The "Testing" amounts to check symlinks exist. This is mostly usefull once extended to detect config packages (just the directories containing an a config), to remind me to add a function for it in `dot-install`.

## Included Configurations

* **Shells**: Bash, Fish, Zsh
* **Terminal**: Tmux, Zellij, Ghostty
* **Editors**: Vim, Neovim (with lazy.nvim)
* **Tools**: Git, Starship prompt, Borg backup
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
