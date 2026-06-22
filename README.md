# Restic Configurator (written in) Python

Wrapper for Restic.  

I grew annoyed with remembering `restic` commands, and I wanted to run it as a SystemD service on a timer.

Executes restic with everything setup from system configuration `.toml` files.

Take a look at [`./systems/example.config.toml`](./systems/example-system/config.json) for an example.