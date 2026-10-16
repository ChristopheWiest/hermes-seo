# Troubleshooting

## Plugin is missing

Check that the plugin is enabled and valid:

```bash
hermes plugins list
hermes plugins validate "${HERMES_HOME:-$HOME/.hermes}/plugins/hermes-seo"
hermes plugins doctor hermes-seo --ci
```

If the checkout is elsewhere, pass its actual path to `plugins validate`. Then use Hermes `skills_list` to confirm the namespaced skills are registered.

## Script runtime is not ready

```bash
hermes seo doctor --json
```

If dependencies or the browser are missing, run `hermes seo setup` when you want to download them. This writes to Hermes plugin data storage, not system Python. If setup fails, retain its error output and check Python/venv availability, disk space, and network access to package and browser sources.

Run utilities through `hermes seo run <script.py> [args...]`; direct Python invocation bypasses the supported runtime contract and may fail due to missing dependencies.

## Provider tools are unavailable

A bundled skill does not install or configure an MCP server. Check that the provider's Hermes-compatible server is configured and enabled in Hermes, then consult that provider's current setup documentation. Keep credentials in Hermes' secret/config mechanism, not in this repository. Local plugin validation does not test external accounts or services.

## Request fails or times out

Check the target site's availability and network access. Some sites block automated requests or require browser rendering. Use the relevant workflow's options and report which data sources were unavailable rather than inferring missing data.

## Schema feedback

The JSON-LD hook is advisory: it adds findings after a file-write tool returns and does not block or roll back the write. Check the returned findings and validate the markup with the appropriate current external validator.

## Get diagnostics

Capture the command, Hermes version, and relevant error output. Remove tokens and other secrets before sharing logs. Historical source-project issues may be useful background, but Claude Code installer paths and settings do not apply to this Hermes port.
