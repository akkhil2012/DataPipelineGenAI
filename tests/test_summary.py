from datapipeline_genai.llm import ConversationInsight, HeuristicSummariser


def test_heuristic_summariser_highlights_top_issues():
    summariser = HeuristicSummariser()
    insights = [
        ConversationInsight("1", "Router keeps dropping", ["connectivity"], -0.3, 0.8),
        ConversationInsight("2", "Router light dead", ["hardware"], -0.6, 0.9),
        ConversationInsight("3", "More router drops", ["connectivity"], -0.5, 0.8),
    ]

    summary = summariser.summarise(insights, max_words=200)

    assert "Connectivity" in summary
    assert "Average severity" in summary
