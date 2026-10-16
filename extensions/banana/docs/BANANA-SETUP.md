# Banana setup

The bundled extension contains prompts and helper scripts, not an installer. Configure a compatible image-generation MCP server in Hermes using the provider's current documentation. Store `GOOGLE_AI_API_KEY` in the active Hermes profile so the parent `hermes_seo_run` tool can inject it through `secret_scope`. Do not pass the key in command arguments or place it in Claude settings. The source project used `@ycse/nanobanana-mcp`; its historical settings examples are not a Hermes configuration template.

Ask Hermes to validate the bundled helper through the native tool so the
active profile secret is injected:

```json
{"script":"validate_setup.py","extension":"banana","args":["--model","<verified-model-id>"]}
```

Set the nonsecret `NANOBANANA_MODEL` runtime option to a verified model ID when using the direct REST helpers. Use `hermes-seo:seo-image-gen` through Hermes after confirming its required provider tools are available. Generation can consume paid credits; request approval for each specific paid operation. If tools are missing, check Hermes MCP status and provider authentication. Do not print or commit API keys.

ImageMagick is optional for local post-processing. Install it through your operating system package manager if conversion or cropping helpers require it.
