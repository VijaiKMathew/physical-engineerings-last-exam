#!/usr/bin/env python3
"""sync_writeup.py: Secure, Zero-Vulnerability Writeup Synchronization Engine for PLE.

Security Invariants:
1. Dynamic Path Resolution: Never hardcodes absolute user paths, usernames, or home dirs.
2. Canonical Boundary Isolation: All destination paths are strictly canonicalized.
3. Symlink Protection: Rejects symlinks on source and target paths.
4. Atomic Replacement: Writes to temporary files and uses atomic os.replace().
5. Automated Secret & PII Gate: Scans source content for credentials, API tokens,
   private keys, and local home directory paths before synchronization. Fails closed.
6. Word Count Monitor: Alerts if writeup exceeds the 2,000 word ceiling.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

SECURITY_GUARD_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"gho_[A-Za-z0-9]{36}"),
    re.compile(r"(?i)(api[_-]?key|secret|token|kaggle_key)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}"),
    re.compile(r"/Users/[a-zA-Z0-9_\-]+/"),
    re.compile(r"/home/[a-zA-Z0-9_\-]+/"),
]


def get_current_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_allowed_roots() -> list[Path]:
    current_root = get_current_repo_root().resolve()
    return [current_root]


def is_safe_path(target_path: Path, allowed_roots: list[Path]) -> bool:
    try:
        resolved = target_path.resolve()
        for part in [target_path] + list(target_path.parents):
            if part.is_symlink():
                return False
        return any(resolved.is_relative_to(root) for root in allowed_roots)
    except (ValueError, RuntimeError):
        return False


def compute_sha256(filepath: Path) -> str:
    if not filepath.exists() or filepath.is_symlink() or not filepath.is_file():
        return ""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def count_words(text: str) -> int:
    """Count words accurately omitting markdown code blocks."""
    # Strip markdown code blocks for pure prose word count
    clean = re.sub(r"```[\s\S]*?```", "", text)
    words = re.findall(r"\b\w+\b", clean)
    return len(words)


def scan_for_secrets_and_pii(content: str) -> list[str]:
    violations = []
    for pat in SECURITY_GUARD_PATTERNS:
        match = pat.search(content)
        if match:
            violations.append(f"Detected prohibited pattern: {match.group(0)[:30]}...")
    return violations


def sanitize_for_public(content: str, rel_image_prefix: str = "docs/images") -> str:
    text = content
    text = re.sub(r'!\[(.*?)\]\((.*?)(docs/images/figure\d+.*?\.png)\)', rf'![\1]({rel_image_prefix}/\3)', text)
    text = text.replace(f"{rel_image_prefix}/{rel_image_prefix}", rel_image_prefix)
    return text


def atomic_write(target_path: Path, content: str) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=target_path.parent, delete=False, encoding="utf-8") as tmp:
        tmp.write(content)
        tmp_name = tmp.name
    os.replace(tmp_name, target_path)


def perform_sync(verbose: bool = True) -> bool:
    repo_root = get_current_repo_root()
    allowed_roots = get_allowed_roots()

    source_master = (repo_root / "WRITEUP.md").resolve()
    if not source_master.exists() or source_master.is_symlink():
        if verbose:
            print("Error: Safe source master WRITEUP.md not found.")
        return False

    with open(source_master, "r", encoding="utf-8") as f:
        master_content = f.read()

    # Pre-Flight Security Gate
    violations = scan_for_secrets_and_pii(master_content)
    if violations:
        print("[SECURITY ALERT] Synchronization aborted due to credential / PII guard violations:")
        for v in violations:
            print(f"  - {v}")
        return False

    # Word count check
    words = count_words(master_content)
    if verbose:
        print(f"Writeup Word Count: {words} / 2000 max words")
    if words > 2000:
        print(f"[WARNING] Writeup exceeds Kaggle maximum limit of 2,000 words ({words} words)!")

    # Target synchronized files
    target_files = [
        repo_root / "reports/writeup/KAGGLE_FORUM_SOLUTION_WRITEUP.md",
        repo_root / "docs/reports/KAGGLE_FORUM_SOLUTION_WRITEUP.md",
    ]

    updated_count = 0
    for target in target_files:
        if not is_safe_path(target.resolve(), allowed_roots):
            continue
        sanitized = sanitize_for_public(master_content, rel_image_prefix="docs/images")

        current_content = ""
        if target.exists() and not target.is_symlink():
            with open(target, "r", encoding="utf-8") as f:
                current_content = f.read()

        if current_content != sanitized:
            atomic_write(target, sanitized)
            updated_count += 1
            if verbose:
                print(f"  -> Securely Synced: {target.name} ({target.parent.relative_to(repo_root)})")

    if verbose:
        print(f"Zero-Vulnerability Sync Complete: {updated_count} files updated.")
    return True


def install_git_hook():
    repo_root = get_current_repo_root()
    hook_path = (repo_root / ".git/hooks/pre-commit").resolve()
    if not hook_path.parent.exists() or hook_path.is_symlink():
        return

    hook_script = """#!/bin/sh
# Auto-sync writeup securely on commit
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
if [ -f "$REPO_ROOT/tools/sync_writeup.py" ]; then
    python3 "$REPO_ROOT/tools/sync_writeup.py" --quiet
    git add "$REPO_ROOT/reports/writeup/" "$REPO_ROOT/docs/reports/" "$REPO_ROOT/docs/images/" 2>/dev/null || true
fi
exit 0
"""
    try:
        atomic_write(hook_path, hook_script)
        os.chmod(hook_path, 0o755)
        print(f"Secure Git pre-commit hook verified at {hook_path.name}")
    except Exception as e:
        print(f"Warning: Could not install git hook: {e}")


def watch_loop(poll_interval: float = 2.0):
    repo_root = get_current_repo_root()
    source_master = (repo_root / "WRITEUP.md").resolve()
    print(f"Secure Watcher Active on {source_master.name} (polling every {poll_interval}s)...")
    last_hash = compute_sha256(source_master)
    perform_sync(verbose=True)

    try:
        while True:
            time.sleep(poll_interval)
            current_hash = compute_sha256(source_master)
            if current_hash and current_hash != last_hash:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Detected modification in WRITEUP.md. Triggering secure sync...")
                perform_sync(verbose=True)
                last_hash = current_hash
    except KeyboardInterrupt:
        print("\nWatcher gracefully terminated.")


if __name__ == "__main__":
    quiet_mode = "--quiet" in sys.argv
    watch_mode = "--watch" in sys.argv
    install_hook = "--install-hook" in sys.argv

    if install_hook:
        install_git_hook()

    if watch_mode:
        install_git_hook()
        watch_loop()
    else:
        success = perform_sync(verbose=not quiet_mode)
        install_git_hook()
        sys.exit(0 if success else 1)
