# Commands and skills

Hermes SEO has two interfaces: Hermes skills for model-guided SEO workflows, and the `hermes seo` CLI for controlled execution of bundled scripts.

## Runtime CLI

```bash
hermes seo setup             # create/refresh the private Python environment
hermes seo doctor --json     # read-only runtime readiness check
hermes seo run fetch_page.py https://example.com --json
```

Run scripts only as `hermes seo run <script.py> [args...]`. The launcher uses the isolated runtime and rejects scripts outside its allowlist. Do not invoke copied Python files directly. Setup downloads pinned packages and, when requested by the runtime, Chromium; it may use substantial disk space.

`fetch_page.py` supports raw fetching by default and rendered fetching with `--render auto|always`; `--max-text N` caps returned text fields. `--json --output page.html` writes successful HTML while keeping the structured result on stdout. Consult `hermes seo run fetch_page.py --help` for the installed version's options.

## Skills

Use Hermes `skills_list` to discover the registered `hermes-seo:*` skills and `skill_view` to load one. Ask Hermes to run the workflow in natural language; do not type a skill name as a terminal command. The `hermes-seo:seo` skill routes requests to the matching workflow. Specialist role skills are intended for delegation through Hermes `delegate_task`, with relevant evidence and a goal in the task context.

Core workflows include site audits, page and technical analysis, content and schema review, GEO, images, sitemap, strategy, international SEO, programmatic SEO, local SEO, backlinks, clustering, drift monitoring, ecommerce, and FLOW. Skill output and external data availability depend on the loaded workflow and configured tools.

## Optional providers

Provider workflows need a compatible Hermes MCP server or provider credentials. The extension notes describe retained capabilities and limitations; configure each server and secret in Hermes using the provider's current documentation. A skill's presence does not mean its provider is connected. Do not run paid or externally mutating operations without approval for that operation.
