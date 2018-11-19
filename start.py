import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_dir)

from funky import app  # noqa


if __name__ == "__main__":
    sys.exit(app.main())
