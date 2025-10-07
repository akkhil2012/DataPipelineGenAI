# DataPipeline GenAI

This project implements a lightweight customer-support analytics pipeline inspired by LLM-enabled workflows. It ingests raw conversation transcripts, applies deterministic natural-language cleaning and tagging, and produces rich summaries that can later be replaced by calls to a hosted large language model. The goal is to demonstrate how a pragmatic data engineering stack can prepare information for generative AI experiences while remaining fully runnable in an offline environment.

## Features

- **Configurable pipeline** powered by `dataclasses` and YAML/JSON friendly settings.
- **Data ingestion** from CSV files containing support conversations.
- **Text standardisation** including whitespace normalisation, punctuation tidying, and language tagging heuristics.
- **Issue classification** using keyword rules plus severity scoring.
- **Heuristic summariser** that emulates an LLM by condensing the most frequent problems and sentiments.
- **Command line interface** for running the pipeline end-to-end and writing aggregated insights as JSON.
- **Extensibility hooks** so that real LLM providers can be injected without changing orchestration logic.

## Getting Started

Install the package in editable mode (or add the repository to your ``PYTHONPATH``) and run the CLI against the bundled sample data set:

```bash
pip install -e .
python -m datapipeline_genai run --input data/sample_calls.csv --output build/report.json
```

A rich JSON report will be created under `build/report.json` with conversation-level annotations and high-level summaries.

## Tests

The project ships with a small test-suite that exercises the data cleaning heuristics and the summariser logic. Execute it with:

```bash
pytest
```

## Project Structure

```
.
├── data
│   └── sample_calls.csv
├── src
│   └── datapipeline_genai
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── ingestion.py
│       ├── llm.py
│       ├── pipeline.py
│       └── processing.py
├── tests
│   ├── test_processing.py
│   └── test_summary.py
└── pyproject.toml
```

## Extending the Pipeline

1. Replace the `HeuristicSummariser` with a real LLM client by implementing the `Summariser` protocol in `llm.py`.
2. Add new processors under `processing.py` for more advanced NLP tasks like entity extraction or topic modelling.
3. Feed the generated JSON into downstream analytics dashboards or knowledge bases to power support operations.
