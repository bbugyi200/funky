"""Entry point for localalias. Simply execute localalias."""

import sys

import localalias.app as app

if __name__ == "__main__":
    try:
        app.main()
    except Exception:
        sys.exit(1)
