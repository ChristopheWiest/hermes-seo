# Hermes SEO: agent instructions

This is a local Hermes port of AgriciDaniel/claude-seo v2.4.2. It is a native Hermes plugin, not a Claude Code plugin.

## Package structure

- `plugin.yaml` and `__init__.py`: Hermes plugin manifest and `register(ctx)` integration.
- `skills/seo-*/SKILL.md`: 26 SEO workflows registered as `hermes-seo:seo-*` plugin skills.
- `skills/role-seo-*/SKILL.md`: 19 specialist roles for Hermes `delegate_task` calls.
- `scripts/`: 56 bundled utilities and a stdlib-only isolated runtime launcher.
- `schema/`, `data/`, `extensions/`, `assets/`: templates, source data, optional integrations, and assets.
- `hooks/validate-schema.py`: JSON-LD validator used by the Hermes `transform_tool_result` hook.

## Runtime rules

- Run bundled Python only through `hermes seo run <script.py>`; never use global Python for plugin utilities.
- Run `hermes seo doctor --json` before work requiring the managed environment. Setup is user-initiated because it downloads dependencies and Chromium.
- Load bundled skill material using `skill_view(name="hermes-seo:seo-*", file_path="references/<file>")`; use `hermes seo show <relative-path>` only for non-skill bundled files.
- Use native Hermes tools (`read_file`, `write_file`, `patch`, `search_files`, `terminal`, `web_search`, `web_extract`, `delegate_task`). Invoke workflow skills by their `hermes-seo:seo-*` namespaced names.
- Delegate specialist work with `delegate_task`, asking the child to load `hermes-seo:role-seo-*`; run sequentially if delegation is unavailable.
- Never invoke cost-bearing API operations without explicit user approval. Do not read secrets from config files; use configured MCP providers or the supplied credential utility.
- Do not make live network calls in tests. Preserve SSRF checks and avoid storing runtime state in the plugin install tree.

## Licensing and validation

Keep the upstream MIT license and contributor attribution. FLOW prompt materials remain CC BY 4.0. Validate changes with `hermes plugins validate`, `hermes plugins doctor --ci`, and relevant `rtk pytest` suites.
