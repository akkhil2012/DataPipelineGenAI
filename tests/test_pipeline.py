from pathlib import Path

from datapipeline_genai.config import PipelineConfig
from datapipeline_genai.pipeline import Pipeline


def test_pipeline_generates_summary(tmp_path: Path):
    input_path = Path("data/sample_calls.csv").resolve()
    output_path = tmp_path / "report.json"
    config = PipelineConfig(input_path=input_path, output_path=output_path)

    pipeline = Pipeline(config)
    result = pipeline.run()

    assert result.summary
    assert len(result.conversations) > 1

    written = pipeline.write_output(result)
    assert written.exists()
