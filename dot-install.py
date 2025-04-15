#!/usr/bin/env python3
"""
dot-install: Create symlinks for dotfiles configurations
"""

import os
import sys
import click
import shutil
from pathlib import Path


# Global variables
DOTFILES_DIR = Path(__file__).resolve().parent
CONFIG_DIR = Path(os.environ.get('XDG_CONFIG_HOME', '')) if os.environ.get('XDG_CONFIG_HOME') else Path.home() / ".config"


# Config registry to hold all configurations
CONFIG_REGISTRY = {}


def register_config(name, src_paths, dest_paths, post_actions=None, description=None):
    """Register a configuration in the central registry"""
    if not isinstance(src_paths, list):
        src_paths = [src_paths]
    if not isinstance(dest_paths, list):
        dest_paths = [dest_paths]
    
    CONFIG_REGISTRY[name] = {
        'src_paths': src_paths,
        'dest_paths': dest_paths,
        'post_actions': post_actions or [],
        'description': description or f"Install {name} configuration"
    }


# Helper functions
def ensure_dir(directory):
    """Create directory if it doesn't exist"""
    if not directory.exists():
        directory.mkdir(parents=True)
        click.echo(f"Created directory: {directory}")


def link_file(src, dest):
    """Create a symlink and handle existing files"""
    # Check if destination already exists
    if dest.exists():
        if dest.is_symlink():
            # If it's already a symlink, check if it points to our file
            if dest.resolve() == src.resolve():
                click.echo(f"Link already exists: {dest} -> {src}")
                return
            else:
                click.echo(f"Removing existing link: {dest}")
                dest.unlink()
        else:
            # If it's a regular file or directory
            backup = Path(f"{dest}.bak")
            click.echo(f"Backing up existing file: {dest} -> {backup}")
            shutil.move(dest, backup)
    
    # Create the symlink
    dest.symlink_to(src)
    click.echo(f"Created link: {dest} -> {src}")


def add_source_to_bashrc(file):
    """Add source command to bashrc if needed"""
    bashrc = Path.home() / ".bashrc"
    config_path = f"$HOME/.config/bash/{file}"
    
    if bashrc.exists():
        with open(bashrc, 'r') as f:
            content = f.read()
        
        if f"source {config_path}" not in content:
            click.echo(f"Adding source command for {file} to .bashrc")
            with open(bashrc, 'a') as f:
                f.write(f"\n[ -f {config_path} ] && source {config_path}\n")
    else:
        click.echo(f"Warning: {bashrc} does not exist. You'll need to manually source {file}.")


def install_config(name):
    """Install a configuration from the registry"""
    if name not in CONFIG_REGISTRY:
        click.echo(f"Unknown configuration: {name}")
        return
    
    cfg = CONFIG_REGISTRY[name]
    click.echo(f"Installing {name} configuration...")
    
    # Ensure directories exist for all destination paths
    for dest in cfg['dest_paths']:
        ensure_dir(dest.parent)
    
    # Create symlinks
    for src, dest in zip(cfg['src_paths'], cfg['dest_paths']):
        link_file(src, dest)
    
    # Run any post-installation actions
    for action in cfg['post_actions']:
        action()


# Register bash components
def register_bash_configs():
    # Bash aliases
    register_config(
        'bash:aliases',
        DOTFILES_DIR / "bash" / "bash_aliases",
        CONFIG_DIR / "bash" / "bash_aliases",
        [lambda: add_source_to_bashrc("bash_aliases")],
        "Install bash aliases"
    )
    
    # Bash completion
    register_config(
        'bash:completion',
        DOTFILES_DIR / "bash" / "bash_completion",
        CONFIG_DIR / "bash" / "bash_completion",
        [lambda: add_source_to_bashrc("bash_completion")],
        "Install bash completion"
    )
    
    # Bash environment
    register_config(
        'bash:env',
        DOTFILES_DIR / "bash" / "bash_env",
        CONFIG_DIR / "bash" / "bash_env",
        [lambda: add_source_to_bashrc("bash_env")],
        "Install bash environment"
    )
    
    # Bash functions
    register_config(
        'bash:functions',
        DOTFILES_DIR / "bash" / "bash_functions",
        CONFIG_DIR / "bash" / "bash_functions",
        [lambda: add_source_to_bashrc("bash_functions")],
        "Install bash functions"
    )
    
    # Fedora aliases
    register_config(
        'bash:fedora',
        DOTFILES_DIR / "bash" / "fedora_aliases",
        CONFIG_DIR / "bash" / "fedora_aliases",
        [lambda: add_source_to_bashrc("fedora_aliases")],
        "Install fedora aliases"
    )
    
    # Full bash (meta-configuration)
    register_config(
        'bash',
        [],  # No direct files, will call each component
        [],  # No direct destinations
        [
            lambda: install_config('bash:aliases'),
            lambda: install_config('bash:completion'),
            lambda: install_config('bash:env'),
            lambda: install_config('bash:functions'),
            lambda: install_config('bash:fedora'),
            lambda: link_file(CONFIG_DIR / "bash", Path.home() / ".bash_dir")
        ],
        "Install all bash configuration"
    )


# Register all other configurations
def register_all_configs():
    register_bash_configs()
    
    # Borg backup profiles
    register_config(
        'borg',
        DOTFILES_DIR / "borg-backup-profiles",
        CONFIG_DIR / "borg",
        description="Install borg backup profiles"
    )
    
    # Fish shell
    register_config(
        'fish',
        DOTFILES_DIR / "fish",
        CONFIG_DIR / "fish",
        description="Install fish shell configuration"
    )
    
    # Ghostty terminal
    register_config(
        'ghostty',
        DOTFILES_DIR / "ghostty",
        CONFIG_DIR / "ghostty",
        description="Install ghostty terminal configuration"
    )
    
    # Git
    register_config(
        'git',
        DOTFILES_DIR / "git" / "gitconfig",
        Path.home() / ".gitconfig",
        description="Install git configuration"
    )
    
    # Neovim
    register_config(
        'nvim',
        DOTFILES_DIR / "nvim",
        CONFIG_DIR / "nvim",
        description="Install neovim configuration"
    )
    
    # Rsync filter rules
    register_config(
        'rsync',
        DOTFILES_DIR / "sync-filter-fedora" / "dot-rsync-filter-home",
        Path.home() / ".rsync-filter-home",
        description="Install rsync filter rules"
    )
    
    # Starship prompt
    register_config(
        'starship',
        DOTFILES_DIR / "dot-config" / "starship.toml",
        CONFIG_DIR / "starship.toml",
        description="Install starship prompt configuration"
    )
    
    # Tmux
    register_config(
        'tmux',
        DOTFILES_DIR / "tmux" / "tmux.conf",
        Path.home() / ".tmux.conf",
        description="Install tmux configuration"
    )
    
    # Vim
    register_config(
        'vim',
        [
            DOTFILES_DIR / "vim" / "vimrc",
            DOTFILES_DIR / "vim" / "initvim"
        ],
        [
            Path.home() / ".vimrc",
            Path.home() / ".vim" / "init.vim"
        ],
        description="Install vim configuration"
    )
    
    # Vim config as neovim config
    register_config(
        'vimnvim',
        DOTFILES_DIR / "vim" / "initvim",
        CONFIG_DIR / "nvim" / "init.vim",
        description="Install vim config as config for neovim"
    )
    
    # Zellij
    register_config(
        'zellij',
        DOTFILES_DIR / "dot-config" / "zellij.kdl",
        CONFIG_DIR / "zellij" / "config.kdl",
        description="Install zellij configuration"
    )
    
    # Zsh
    register_config(
        'zsh',
        DOTFILES_DIR / "zsh" / "zshrc",
        Path.home() / ".zshrc",
        description="Install zsh configuration"
    )
    
    # All (meta-configuration)
    all_configs = [
        'bash', 'borg', 'fish', 'ghostty', 'git', 'nvim',
        'rsync', 'starship', 'tmux', 'vim', 'zellij', 'zsh'
    ]
    
    register_config(
        'all',
        [],
        [],
        [lambda cfg=cfg: install_config(cfg) for cfg in all_configs],
        "Install all configurations"
    )


# Register all configurations
register_all_configs()


# Main CLI command group
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Create symlinks for dotfiles configurations"""
    # If no subcommand is provided, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Dynamically create commands for each configuration
for name, cfg in CONFIG_REGISTRY.items():
    # Skip bash sub-commands to handle them specially
    if ':' in name:
        continue
    
    # Create a command function dynamically
    def make_command(name=name):
        @cli.command(name=name)
        def cmd():
            install_config(name)
        cmd.__doc__ = cfg['description']
        return cmd
    
    # Add the command to the CLI
    make_command()


# Create bash command group
@cli.group()
def bash():
    """Bash configuration files"""
    pass


# Create bash subcommands
for name, cfg in CONFIG_REGISTRY.items():
    if name.startswith('bash:'):
        sub_name = name.split(':')[1]
        
        def make_subcommand(name=name, sub_name=sub_name):
            @bash.command(name=sub_name)
            def cmd():
                install_config(name)
            cmd.__doc__ = cfg['description']
            return cmd
        
        make_subcommand()


# Add bash "all" command
@bash.command('all')
def bash_all():
    """Install all bash configurations"""
    install_config('bash')


if __name__ == "__main__":
    cli()