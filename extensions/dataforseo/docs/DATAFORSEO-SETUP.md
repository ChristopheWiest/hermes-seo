# DataForSEO setup

Create an account with DataForSEO and use its current documentation to configure a compatible MCP server in Hermes. Store `DATAFORSEO_USERNAME` and `DATAFORSEO_PASSWORD` as secrets in the active Hermes profile. The parent `hermes_seo_run` tool injects them only for DataForSEO scripts; do not pass credentials in command arguments or store them in plugin files. Do not use the old install scripts or Claude Code `mcpServers` examples; those were source-project setup and are not supported by this port.

The retained skill material documents the source server's modules and expected tool families. Verify the actual tools exposed by your Hermes server before using a workflow. The cost ledger can be invoked through the managed runtime if it is allowlisted:

```bash
hermes seo run dataforseo_costs.py --help
```

DataForSEO charges by endpoint and request; rates change. Review the provider's current pricing and expected request volume, then obtain approval for paid operations. No live account or MCP integration has been verified in this fork.
