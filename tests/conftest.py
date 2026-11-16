import pytest

from license_kit import IntendedUse


@pytest.fixture
def private_use() -> IntendedUse:
    """Non-commercial use, not limited to research, of the work as is, shared with nobody, to derive other uses from."""
    return IntendedUse(
        is_commercial=False,
        is_research_only=False,
        is_used_for_ai_training=False,
        is_modified=False,
        is_combined=False,
        is_redistributed=False,
        is_offered_over_network=False,
    )
