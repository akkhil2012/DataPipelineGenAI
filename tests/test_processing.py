from datapipeline_genai.processing import (
    classify_issue,
    normalise_whitespace,
    prepare_transcript,
    sentiment_score,
    tokenise,
)


def test_normalise_whitespace_trims_and_collapses():
    assert normalise_whitespace("  hello   world  ") == "hello world"


def test_tokenise_lowercases_and_splits():
    assert tokenise("Hello THERE") == ["hello", "there"]


def test_classify_issue_detects_keywords():
    issues, severity = classify_issue(["router", "update", "failed"])
    assert "connectivity" in issues
    assert severity >= 0.8


def test_prepare_transcript_enriches_metadata():
    result = prepare_transcript("Hi support, the app crashes and the notifications are late!")
    assert result["language"] == "en"
    assert "application" in result["issues"]
    assert result["cleaned_transcript"].startswith("Hi support")


def test_sentiment_score_balances_positive_and_negative():
    score = sentiment_score(["love", "app", "but", "lockout"])
    assert score < 0
