from dataclasses import replace

from license_kit import IntendedUse, UseKind


class TestIntendedUse:
    def test_private_use_involves_only_non_research_use(self, private_use: IntendedUse) -> None:
        assert private_use.involved_kinds == {UseKind.NON_RESEARCH_USE}
        assert replace(private_use, is_research_only=True).involved_kinds == frozenset()

    def test_each_item_involves_its_kind(self, private_use: IntendedUse) -> None:
        research: IntendedUse = replace(private_use, is_research_only=True)
        assert replace(research, is_commercial=True).involved_kinds == {UseKind.COMMERCIAL_USE}
        assert replace(research, is_used_for_ai_training=True).involved_kinds == {UseKind.AI_TRAINING}
        assert replace(research, is_modified=True).involved_kinds == {UseKind.MODIFICATION}
        assert replace(research, is_redistributed=True).involved_kinds == {UseKind.REDISTRIBUTION}
        assert replace(research, is_offered_over_network=True).involved_kinds == {UseKind.NETWORK_SERVICE}

    def test_redistributing_a_modification_involves_modified_redistribution(self, private_use: IntendedUse) -> None:
        use: IntendedUse = replace(private_use, is_research_only=True, is_modified=True, is_redistributed=True)
        assert use.involved_kinds == {UseKind.MODIFICATION, UseKind.REDISTRIBUTION, UseKind.MODIFIED_REDISTRIBUTION}

    def test_combination_involves_no_kind(self, private_use: IntendedUse) -> None:
        assert replace(private_use, is_research_only=True, is_combined=True).involved_kinds == frozenset()
