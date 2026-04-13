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
# Remind to run release script when pushing to cowork branch

branch=$(git symbolic-ref HEAD 2>/dev/null | sed 's|refs/heads/||')

if [ "$branch" = "cowork" ]; then
    echo ""
    echo "  You are pushing to the 'cowork' branch."
    echo "  Did you run 'python cowork/release.py' to create a release tag?"
    echo "  (If not, no ZIP will be built and no GitHub Release will be created.)"
    echo ""
    printf "  Continue push without release tag? [y/N] "
    read answer < /dev/tty
    if [ "$answer" != "y" ] && [ "$answer" != "Y" ]; then
        echo "  Push aborted. Run 'python cowork/release.py' first."
        exit 1
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
