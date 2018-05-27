import unittest.mock as mock

import pytest

from localalias.utils import log


@pytest.fixture(scope='module')
def debug_mode():
    """Enable debug logging."""
    log.init_logger(debug=True)
