# Project conventions

Follow the [KPEX conventions](https://github.com/iic-jku/kpex/blob/main/AGENTS.md).

- This repository prepares a `KQCircuits` exporter for partner development
- Describe incomplete capabilities explicitly; registration does not mean export works
- Use the full copyright and GPL header of neighboring Python files, including tests
- Keep `klayout_pex_plugins` an implicit namespace without `__init__.py`
- Discovery and factory construction must not import optional geometry or solver libraries
- Follow the provisional `PEX25DSceneExporter` contract; do not mutate scenes or options
- Add public options only with a caller, validation and observable contract tests
- Use boundary-value analysis and independent physical references for geometry and numeric tests
- Run `poetry run pytest`, then build and check both distributions before handover
- Give each concern a focused commit only when requested; otherwise leave changes for review
- Branch names describe the change without authoring-tool, model or provider identifiers
- Do not add authoring attribution or co-author trailers to code or review text
- Use short paragraphs and bullets, with identifiers in backticks
