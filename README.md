# Restic Configurator (written in) Python

This project is a wrapper for restic.  
Because restic is primarily a CLI tool, having configuration files is handy.

Specify systems in the `systems/` folder, and then execute restic with everything set up from that system configuration file.

Take a look at [`./systems/example-system/config.json`](./systems/example-system/config.json) for an example.

## Usage Examples

`python restic_backup.py --system_config "systems/example-system/config.json"`  
`python restic_forget.py --system_config "systems/example-system/config.json"`  
`python restic_ops.py --system_config "systems/example-system/config.json" --command="unlock"`

---

Under heavy development.