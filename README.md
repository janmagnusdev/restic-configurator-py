# Restic Configurator (written in) Python

This project is a wrapper for restic.  
I grew annoyed with remembering restic commands, and I also wanted to run it robust as a SystemD service on a timer.

Specify systems in the `systems/` folder, and then execute restic with everything set up from that system configuration file.

Take a look at [`./systems/example-system/config.json`](./systems/example-system/config.json) for an example.

## Usage Examples

`python restic_backup.py --system_config "systems/example-system/config.json"`  
`python restic_forget.py --system_config "systems/example-system/config.json"`  
`python restic_ops.py --system_config "systems/example-system/config.json" --command="unlock"`