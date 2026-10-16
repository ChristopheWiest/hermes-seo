"""Static installer/runtime contract checks that do not mutate a real home."""

import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(
    os.name != "posix", reason="the executable bit is a POSIX mode bit; Windows has none"
)
def test_launcher_is_executable() -> None:
    assert (ROOT / "scripts/hermes-seo").stat().st_mode & 0o100


def test_launcher_uses_safe_exec() -> None:
    text = (ROOT / "scripts/hermes-seo").read_text(encoding="utf-8")
    assert '"${HERMES_SEO_PYTHON}" "${runtime}" "$@"' in text
    assert 'exec py -3 "${runtime}" "$@"' in text
    assert 'exec python3 "${runtime}" "$@"' in text
    assert 'exec python "${runtime}" "$@"' in text
    assert "eval " not in text


def test_runtime_and_manifest_use_hermes_contract() -> None:
    runtime = (ROOT / "scripts/runtime.py").read_text(encoding="utf-8")
    manifest = (ROOT / "plugin.yaml").read_text(encoding="utf-8")
    assert '"${HERMES_SEO_ROOT}/scripts/hermes-seo"' in runtime
    assert 'os.environ.get("HERMES_SEO_DATA_DIR")' in runtime
    assert "name: hermes-seo" in manifest
    assert "version:" in manifest


def test_yukari_sandbox_installation_keeps_code_read_only_and_state_external() -> None:
    text = (ROOT / "docs/INSTALLATION.md").read_text(encoding="utf-8")
    section = text.split("## Docker sandbox", 1)[1].split("\n## ", 1)[0]

    assert "/opt/hermes-seo:ro" in section
    assert "/var/lib/hermes-seo:rw" in section
    assert "HERMES_SEO_ROOT=/opt/hermes-seo" in section
    assert "HERMES_SEO_DATA_DIR=/var/lib/hermes-seo" in section
    assert "./scripts/hermes-seo setup" in section
    assert "./scripts/hermes-seo doctor --json" in section
    assert "./scripts/hermes-seo run portability_check.py --json" in section
    assert "Do not mount host credentials" in section


def test_sandbox_hermes_bridge_is_executable() -> None:
    assert (ROOT / "scripts/hermes").stat().st_mode & 0o100


def test_sandbox_hermes_bridge_forwards_only_seo(tmp_path: Path) -> None:
    import json
    import subprocess

    root = tmp_path / "plugin"
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    launcher = scripts / "hermes-seo"
    launcher.write_text(
        '#!/usr/bin/env python3\n'
        'import json, os, sys\n'
        'open(os.environ["CAPTURE"], "w").write(json.dumps({"args": sys.argv[1:], "data_dir": os.environ.get("HERMES_SEO_DATA_DIR")}))\n',
        encoding="utf-8",
    )
    launcher.chmod(0o755)
    capture = tmp_path / "args.json"
    env = {**os.environ, "HERMES_SEO_ROOT": str(root), "CAPTURE": str(capture)}

    result = subprocess.run(
        [str(ROOT / "scripts/hermes"), "seo", "doctor", "--json"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert json.loads(capture.read_text(encoding="utf-8")) == {
        "args": ["doctor", "--json"],
        "data_dir": "/var/lib/hermes-seo",
    }


def test_sandbox_hermes_bridge_rejects_other_commands() -> None:
    import subprocess

    result = subprocess.run(
        [str(ROOT / "scripts/hermes"), "plugins", "doctor"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 127
    assert "only 'hermes seo' is available in this sandbox" in result.stderr


def test_yukari_sandbox_docs_route_hermes_seo_to_local_launcher() -> None:
    text = (ROOT / "docs/INSTALLATION.md").read_text(encoding="utf-8")
    section = text.split("## Docker sandbox", 1)[1].split("\n## ", 1)[0]

    assert "scripts/hermes:/usr/local/bin/hermes:ro" in section
    assert "HERMES_SEO_DATA_DIR=/var/lib/hermes-seo" in section
    assert "accepts only `hermes seo`" in section


def test_sandbox_hermes_bridge_shows_only_files_within_bundle(tmp_path: Path) -> None:
    import subprocess

    root = tmp_path / "plugin"
    root.mkdir()
    (root / "guide.md").write_text("Bundled reference\n", encoding="utf-8")
    outside = tmp_path / "outside.md"
    outside.write_text("private host file\n", encoding="utf-8")
    (root / "escape.md").symlink_to(outside)
    env = {**os.environ, "HERMES_SEO_ROOT": str(root)}

    shown = subprocess.run(
        [str(ROOT / "scripts/hermes"), "seo", "show", "guide.md"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    traversal = subprocess.run(
        [str(ROOT / "scripts/hermes"), "seo", "show", "../outside.md"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    symlink_escape = subprocess.run(
        [str(ROOT / "scripts/hermes"), "seo", "show", "escape.md"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert shown.returncode == 0
    assert shown.stdout == "Bundled reference\n"
    assert traversal.returncode == 2
    assert symlink_escape.returncode == 2
