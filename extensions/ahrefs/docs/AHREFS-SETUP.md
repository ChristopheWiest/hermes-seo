# Ahrefs setup

The source extension targets the official [`@ahrefs/mcp`](https://www.npmjs.com/package/@ahrefs/mcp) server. This fork does not install it or edit provider settings. Configure a Hermes-compatible Ahrefs MCP server using the provider's current documentation, keep the token in Hermes' secret/config mechanism, then confirm the expected tools are available in Hermes before asking it to use the `hermes-seo:seo-ahrefs` workflow.

The source setup previously pinned `@ahrefs/mcp@0.0.11`; treat that version and its configuration details as historical, not as a current compatibility claim. Ahrefs API usage may consume units. Check current account pricing before calls. The bundled DataForSEO cost tracker is available, when allowlisted, through `hermes seo run dataforseo_costs.py`.

If tools are missing, check the Hermes MCP server status and provider authentication. Do not put tokens in shell history or this repository. No live provider call has been verified in this fork.
