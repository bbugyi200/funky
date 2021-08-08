"""Entry point for funky. Simply execute funky (i.e. run `python funky`)."""

import importlib
import os
import sys


if os.environ.get("DEBUG_FUNKY", None):
    parent_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(parent_dir))
    __package__ = os.path.basename(  # pylint: disable=redefined-builtin
        parent_dir
    )
    importlib.import_module(__package__)

from funky import app


if __name__ == "__main__":
    sys.exit(app.main())
