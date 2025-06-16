# Python Dot-Install Improvements

## Key Improvements

1. Centralized config registry system that makes adding new configs much easier
2. Each config only needs to be registered once with its source, destination, and optional post-actions  
3. XDG_CONFIG_HOME is properly used if available
4. Directory creation is handled automatically as part of the installation process
5. Commands are generated dynamically from the registry
6. Maintains the same command structure as the original script

## Adding New Configurations

To add a new configuration, simply register it using the `register_config` function:

```python
register_config(
    'new_config',                           # Name
    DOTFILES_DIR / "path" / "to" / "file",  # Source path (or list of paths)
    CONFIG_DIR / "destination" / "path",    # Destination path (or list of paths)
    [optional_post_action_functions],       # Optional post-installation actions
    "Description of this configuration"     # Description (for help text)
)
```