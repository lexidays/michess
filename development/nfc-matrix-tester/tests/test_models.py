from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from nfc_matrix_tester.models import TagRead


def test_timestamp_defaults_to_now() -> None:
    before = datetime.now()
    tag = TagRead(uid="04a3b2c1")
    after = datetime.now()

    assert before <= tag.timestamp <= after
    assert tag.square is None


def test_is_immutable() -> None:
    tag = TagRead(uid="04a3b2c1")

    with pytest.raises(FrozenInstanceError):
        tag.uid = "changed"  # type: ignore[misc]
