# Hermes SEO

<p align="center">
  <a href="assets/hermes-seo-promo.mp4">
    <img src="assets/hermes-seo-promo.gif" width="960" alt="Hermes SEO promo: 45 SEO skills, technical audits and schema feedback">
  </a>
</p>

Hermes SEO 0.1.0 packages the SEO analysis workflows, their Python utilities, and specialist roles from [Claude SEO v2.4.2](https://github.com/AgriciDaniel/claude-seo) as a native Hermes plugin. The port keeps 25 workflow skills plus the `seo` router, 19 delegated role skills, 56 utility scripts, Schema.org templates, and optional provider integrations. Claude SEO was created by Daniel Agrici and remains attributed under its MIT license.

This is an independent community port maintained at [yuzushi-dev/hermes-seo](https://github.com/yuzushi-dev/hermes-seo). It is not an official Nous Research or Hermes Agent plugin, and catalog inclusion has not been requested or granted.

## Install locally

Clone the public repository, then copy the plugin directory to the active Hermes home at `plugins/hermes-seo`, then enable it:

```bash
git clone https://github.com/yuzushi-dev/hermes-seo.git
mkdir -p "${HERMES_HOME:-$HOME/.hermes}/plugins"
cp -a hermes-seo "${HERMES_HOME:-$HOME/.hermes}/plugins/hermes-seo"
hermes plugins enable hermes-seo
hermes plugins doctor hermes-seo --ci
```

The plugin registers namespaced skills such as `hermes-seo:seo-audit` and `hermes-seo:role-seo-technical`; use `skills_list` and `skill_view` to discover/load them. Ask Hermes to audit or analyze a site, or load `hermes-seo:seo` as the router. The runtime is available as `hermes seo setup|doctor|run`. Credentialed utilities use the native `hermes_seo_run` tool, which resolves only the script's allowlisted secret names from the active Hermes profile vault. Skills instruct the agent to request approval before external or paid operations.

`hermes seo setup` creates a private virtual environment and downloads pinned Python packages; browser setup also downloads Chromium. It may use substantial disk space. Run it only when asked. `hermes seo doctor --json` checks readiness without changing the system. Use `hermes_seo_run` for credentialed utilities; noncredentialed utilities may use `hermes seo run <script.py>`. Both paths use the isolated environment and script allowlist.

To update this local copy, pull a reviewed commit in the repository and run `hermes plugins doctor hermes-seo --ci`. No public catalog entry or release is currently provided by this port.

## Compatibility

The native plugin requires Hermes Agent 0.22.2 or newer and supports Linux and macOS. Windows is not declared because the registered runtime currently launches through Bash. Python 3.10 or newer with `venv` support is required for the managed SEO runtime.

## Optional integrations

The package preserves nine optional provider integrations: DataForSEO, Banana image generation, Firecrawl, Ahrefs, SE Ranking, Profound, Bing Webmaster, Matomo, and Unlighthouse. They require compatible MCP servers or individual service credentials and are inactive unless configured in Hermes. Setup scripts that wrote Claude Code configuration were removed. See [extension notes](docs/EXTENSIONS.md) for what is retained and what remains unverified.

Do not call paid endpoints, spend API credits, or submit data to external services without the user's explicit approval for that operation. Skills request that approval before the tool call; `hermes_seo_run` does not enforce an approval policy. The skills must report when a provider or credential is unavailable. CI skips the suite's explicit live-network render check and does not call provider APIs.

Google Search Console, GA4, Google Ads, and Indexing API OAuth flows remain disabled until Hermes provides a profile-scoped Google authorization route. Supported profile-vault names are `GOOGLE_API_KEY`, `MOZ_API_KEY`, `BING_WEBMASTER_API_KEY`, `KEYWORDSEVERYWHERE_API_KEY`, `MATOMO_API_TOKEN` or `MATOMO_TOKEN`, `MATOMO_URL`, `MATOMO_SITE_ID` or `MATOMO_IDSITE`, `HERMES_SEO_LOCAL_TARGETS`, `DATAFORSEO_USERNAME`, `DATAFORSEO_PASSWORD`, `INDEXNOW_KEY`, and Banana's `GOOGLE_AI_API_KEY`. IndexNow's nonsecret key-location URL stays a normal script argument. Secrets are never catalog metadata or repository files.

## Security and data

The runtime allowlists bundled scripts, rejects path traversal, and uses the source project's SSRF and DNS-rebinding protections. Runtime files and browser binaries use the active Hermes plugin data directory; credentials remain in the active Hermes profile vault and are injected only for an allowlisted script. No credential files belong in this repository. Schema feedback runs after Hermes file-write tools and returns findings to the model; it does not block or roll back a write.

The plugin can start local subprocesses for its managed Python runtime through `hermes_seo_run`. This native tool runs in the Hermes host plugin process; a Docker terminal sandbox does not contain it. Script arguments may therefore name host paths accessible to that process. `hermes seo setup` downloads Python packages and, unless skipped, Chromium. Audit workflows fetch user-selected websites. Optional integrations send data to their named third-party providers and may incur charges; they remain inactive until separately configured. The plugin stores its managed environment, cache, and runtime configuration in Hermes plugin data storage. It does not include telemetry or a self-updater.

The core project is MIT licensed. The FLOW framework and its prompt materials remain CC BY 4.0 with source attribution. See [LICENSE](LICENSE) and [the FLOW skill](skills/seo-flow/SKILL.md).

## Validation

```bash
hermes plugins validate /path/to/hermes-seo
hermes plugins doctor /path/to/hermes-seo --ci
rtk pytest -q
```

The source suite covers local script behavior and security boundaries. API-backed behavior needs the corresponding service account and was not validated as part of the local port.

Catalog preparation metadata is available in [docs/catalog-submission-template.yaml](docs/catalog-submission-template.yaml). It is a template, not a submission: the final 40-character release commit SHA remains pending until a release exists.
