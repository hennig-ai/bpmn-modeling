"""Install git hooks for this repository.

Usage:
    python cowork/install_hooks.py
"""

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
HOOKS_DIR: Path = REPO_ROOT / ".git" / "hooks"
PRE_PUSH_HOOK: Path = HOOKS_DIR / "pre-push"

PRE_PUSH_CONTENT: str = """\
#!/bin/sh
# Pre-push reminders for main and cowork branches

branch=$(git symbolic-ref HEAD 2>/dev/null | sed 's|refs/heads/||')

if [ "$branch" = "cowork" ]; then
    echo ""
    echo "  REMINDER: Did you run 'python cowork/release.py' to create a release tag?"
    echo "  (If not, no ZIP will be built and no GitHub Release will be created.)"
    echo ""
fi

if [ "$branch" = "main" ]; then
    missing=$(git log cowork..main --oneline 2>/dev/null)
    if [ -n "$missing" ]; then
        echo ""
        echo "  REMINDER: The following commits are on 'main' but not yet on 'cowork':"
        echo "$missing" | sed 's/^/    /'
        echo ""
    fi
fi

exit 0
"""


def main() -> None:
    PRE_PUSH_HOOK.write_text(PRE_PUSH_CONTENT, encoding="utf-8")
    PRE_PUSH_HOOK.chmod(0o755)
    print(f"Installed: {PRE_PUSH_HOOK}")


if __name__ == "__main__":
    main()
