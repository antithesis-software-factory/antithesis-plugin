# Snouty setup guide

## Install snouty

Install with `cargo binstall` (preferred):

```bash
cargo binstall snouty
```

Or with the installer script, which also enables `snouty update`:

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/antithesishq/snouty/releases/latest/download/snouty-installer.sh | sh
```

Source: https://github.com/antithesishq/snouty. To update a `cargo binstall` install, reinstall.

## Configure snouty

Configure the tenant, registry and credentials with `snouty login`; it is interactive. In a headless environment, use environment variables or a settings file instead (see `snouty launch --help` and `snouty settings --help`).

## Verify snouty

Run `snouty doctor`.
