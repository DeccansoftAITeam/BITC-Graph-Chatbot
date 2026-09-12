from course_knowledge.safety import ContentSafetyGate


class FakeClient:
    def __init__(self, severities):
        self.severities = severities

    def analyze_text(self, request):
        items = [type("Category", (), {"category": name, "severity": severity}) for name, severity in self.severities.items()]
        return type("Response", (), {"categories_analysis": items})()


def test_safety_allows_low_severity_content() -> None:
    result = ContentSafetyGate(FakeClient({"Hate": 0, "Violence": 2})).assess("safe")

    assert result.allowed


def test_safety_blocks_content_above_threshold() -> None:
    result = ContentSafetyGate(FakeClient({"Violence": 4}), max_allowed_severity=2).assess("unsafe")

    assert not result.allowed
