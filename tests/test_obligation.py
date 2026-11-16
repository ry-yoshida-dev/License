from license_kit import Obligation


class TestObligation:
    def test_severity_ranks_copyleft_heaviest(self) -> None:
        assert sorted(Obligation, key=lambda obligation: obligation.severity) == [
            Obligation.ATTRIBUTION,
            Obligation.MODIFICATION_NOTICE,
            Obligation.SOURCE_DISCLOSURE,
            Obligation.DOWNSTREAM_TERMS,
            Obligation.SHARE_ALIKE,
        ]
        assert len({obligation.severity for obligation in Obligation}) == len(Obligation)
