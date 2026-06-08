
import pytest

@pytest.mark.usefixtures("log_on_failure","page")
class BaseTest:
    pass