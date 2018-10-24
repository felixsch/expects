
import pytest
from receives.receiver import Receiver


@pytest.fixture
def receive():
    receiver = Receiver()
    yield receiver
    receiver.finalize()
