# Installation

Hermes SEO is a local Hermes plugin. This fork does not publish a catalog or release; install from a reviewed checkout.

## Requirements

- Hermes with plugin support
- Python 3.10+ and `venv` support (the managed runtime installs pinned dependencies)
- Git to obtain or update the checkout

Playwright/Chromium is optional and is provisioned by setup for workflows that need browser rendering. Setup downloads packages and a browser and can use substantial disk space.

## Install from a checkout

```bash
mkdir -p "${HERMES_HOME:-$HOME/.hermes}/plugins"
cp -a /path/to/hermes-seo "${HERMES_HOME:-$HOME/.hermes}/plugins/hermes-seo"
hermes plugins enable hermes-seo
hermes plugins doctor hermes-seo --ci
```

Initialize the isolated runtime only when needed:

```bash
hermes seo setup
hermes seo doctor --json
```

`hermes seo setup` installs pinned Python dependencies and optional Chromium into Hermes plugin data storage. `hermes seo doctor --json` checks readiness without changing the system. Use `hermes seo run <script.py> [args...]` for offline utilities. Credentialed utilities must use the native `hermes_seo_run` tool so the selected profile-vault values are scoped to one child process.

## Docker sandbox

Keep the reviewed bundle immutable and give its runtime a separate persistent data directory. Configure the container with these mounts (replace the host source path with the reviewed checkout):

```yaml
volumes:
  - /host/reviewed/hermes-seo:/opt/hermes-seo:ro
  - /host/reviewed/hermes-seo/scripts/hermes:/usr/local/bin/hermes:ro
  - hermes-seo-data:/var/lib/hermes-seo:rw
environment:
  HERMES_SEO_ROOT: /opt/hermes-seo
  HERMES_SEO_DATA_DIR: /var/lib/hermes-seo
```

Do not mount host credentials, the host Hermes profile, SSH configuration, or cloud-provider configuration into this container. The data volume is the only location Hermes SEO needs to write. Runtime setup requires outbound access to the configured Python package source and, unless `--skip-browser` is used, the Chromium download source.

In the container terminal, bind the runtime to those paths before setup, diagnosis, or execution:

```bash
export HERMES_SEO_ROOT=/opt/hermes-seo
export HERMES_SEO_DATA_DIR=/var/lib/hermes-seo
cd "$HERMES_SEO_ROOT"
```

The mounted `scripts/hermes` compatibility command accepts only `hermes seo` and forwards it to the bundle launcher. It does not expose the host Hermes CLI. Use it for setup, diagnosis, and offline utilities:

```bash
hermes seo setup
hermes seo doctor --json
hermes seo run portability_check.py --json
```

The bundled launcher remains available directly if the compatibility command is not mounted:

```bash
./scripts/hermes-seo setup
./scripts/hermes-seo doctor --json
./scripts/hermes-seo run portability_check.py --json
```

The launcher selects an available Python 3.10+ interpreter and then dispatches through the managed environment under `/var/lib/hermes-seo`. `scripts/hermes-seo` is a shell launcher, so do not pass it to `python3`; `python3 scripts/runtime.py ...` is the lower-level equivalent when a shell cannot execute the launcher.

Credentialed calls are different: `hermes_seo_run` executes from the Hermes
host plugin process and does not inherit the Docker terminal's filesystem or
network isolation. Script arguments can reference paths visible to that host
process. Review file arguments and ask for approval before paid, external, or
mutating operations; the tool itself does not enforce that approval policy.

## Use the skills

Discover skills with Hermes `skills_list` and load them with `skill_view`. Ask Hermes to perform an audit or analysis, or load `hermes-seo:seo` as the router. Skills are prompt workflows; they are not shell commands. Provider-backed workflows require a separately configured compatible Hermes MCP server and account.

Google Search Console, GA4, Google Ads, and Indexing API OAuth flows stay disabled until Hermes provides a profile-scoped Google authorization route. The native tool supports these active-profile vault names: `GOOGLE_API_KEY`, `MOZ_API_KEY`, `BING_WEBMASTER_API_KEY`, `KEYWORDSEVERYWHERE_API_KEY`, `MATOMO_API_TOKEN` or `MATOMO_TOKEN`, `MATOMO_URL`, `MATOMO_SITE_ID` or `MATOMO_IDSITE`, `HERMES_SEO_LOCAL_TARGETS`, `DATAFORSEO_USERNAME`, `DATAFORSEO_PASSWORD`, `INDEXNOW_KEY`, and Banana's `GOOGLE_AI_API_KEY`. IndexNow's key-location URL is nonsecret and remains a normal argument. Do not put secret values in the checkout, catalog entry, or tool arguments.

## Update

Review the new checkout, replace the local plugin copy, then run:

```bash
hermes plugins doctor hermes-seo --ci
```

## Remove

Disable the plugin with `hermes plugins disable hermes-seo`, then remove its directory under `${HERMES_HOME:-$HOME/.hermes}/plugins/hermes-seo` if desired. Runtime data is held in Hermes plugin data storage; inspect Hermes' configured data location before removing it.
