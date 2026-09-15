---
icon: lucide/code
---

# Python code

Rules for any Python in our repositories, whether written by a person or an agent. They are enforced by continuous integration, so a pull request that violates them does not merge, and by pre-commit, so most violations never reach a commit.

## Tooling in one table

| Concern | Tool | Command | Config |
|---------|------|---------|--------|
| Lint | [ruff](https://docs.astral.sh/ruff/) | `ruff check` | `.ruff.toml` |
| Format | ruff | `ruff format` | `.ruff.toml` |
| Types | [ty](https://docs.astral.sh/ty/) | `ty check` | `[tool.ty]` in `pyproject.toml` |
| Data models | [pydantic](https://docs.pydantic.dev/) | | |
| Tests | pytest, tox | `tox run-parallel` | `tox.ini` |
| Environment | [uv](https://docs.astral.sh/uv/) | `uv sync --extra dev` | `pyproject.toml` |
| Pre-commit | [pre-commit](https://pre-commit.com/) | `pre-commit install` | `.pre-commit-config.yaml` |

All tools are listed in the `dev` extra of `pyproject.toml`, so `uv sync --extra dev` installs everything and `uv run <tool>` runs it.

## ruff: lint and format

ruff replaces flake8, isort, pyupgrade, pydocstyle and black in one fast tool. Both the linter and the formatter run in CI and in pre-commit.

```bash
ruff check          # lint
ruff check --fix    # apply safe fixes
ruff format         # format in place
ruff format --check # what CI runs
```

Our `.ruff.toml`, copied between repositories:

```toml title=".ruff.toml"
line-length = 88
indent-width = 4
# oldest supported version, see `project.requires-python`
target-version = "py311"

[lint]
# Pyflakes (F) and a subset of pycodestyle (E), plus:
#   W  warnings, I import sorting, D docstrings (google), UP pyupgrade,
#   B bugbear, C4 comprehensions, SIM simplifications, RET returns,
#   G logging format, PIE misc, RUF ruff specific
select = [
    "E4", "E7", "E9", "F", "W", "I", "D", "UP", "B", "C4", "SIM", "RET", "G", "PIE", "RUF",
]
ignore = [
    # names such as `König` are not ambiguous unicode, they are german
    "RUF001", "RUF002", "RUF003",
]
fixable = ["ALL"]
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[lint.per-file-ignores]
"tests/**" = ["F403", "F405"]

[lint.pydocstyle]
convention = "google"

[format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

Rules of thumb:

- Never add `# noqa` to make CI green. Fix the code, or add a per-file ignore with a comment saying why.
- Docstrings follow the Google convention and are required on public functions, classes and modules (rule set `D`).
- Keep `target-version` at the oldest supported Python so `UP` does not introduce syntax the package cannot run on.

## ty: type checking

[ty](https://docs.astral.sh/ty/) is the type checker from the ruff authors. Every diagnostic is an error in our configuration; there is no warning level to ignore.

```toml title="pyproject.toml"
[tool.ty.environment]
# the package lives in the src layout; the checked python version is inferred
# from `project.requires-python`, i.e., the oldest supported version
root = ["./src", "."]

[tool.ty.src]
include = ["src", "tests"]

[tool.ty.terminal]
# warnings are failures: keep the codebase free of any diagnostic
error-on-warning = true
```

```bash
uv run ty check     # working tree
tox r -e ty         # what CI runs, with all extras installed
```

Rules of thumb:

- Annotate every function signature. `ty` infers locals; it cannot infer your intent at boundaries.
- Prefer precise types over `Any`. If `Any` is unavoidable, say why in a comment.
- Optional dependencies that a module imports must be installed for the check, otherwise `ty` cannot resolve them. The tox `ty` environment installs the relevant extras.

## pydantic: every data model validates

Wherever code has a data model (configuration, records read from files or APIs, results passed between modules, anything serialised), it is a [pydantic](https://docs.pydantic.dev/) `BaseModel` with validation. Not a dict, not a bare dataclass, not a `TypedDict`.

The reason is the same as for reproducing bugs before fixing them: errors should surface where they happen. A dict with a wrong key or a string where a float was expected fails three modules later with an unrelated message. A pydantic model fails at construction with the field name and the offending value.

### The pattern

```python
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Dose(BaseModel):
    """A single administration of a substance."""

    model_config = ConfigDict(
        extra="forbid",             # unknown fields are an error, typos do not pass silently
        frozen=True,                # immutable after construction
        validate_assignment=True,   # only relevant when frozen=False
        strict=True,                # no implicit coercion, "1.0" is not a float
    )

    substance: str = Field(min_length=1)
    amount: float = Field(gt=0, description="Dose amount in `unit`.")
    unit: str = Field(pattern=r"^(mg|g|mg/kg)$")
    route: str = Field(default="oral")

    @field_validator("substance")
    @classmethod
    def normalise_substance(cls, value: str) -> str:
        """Substances are stored lower case."""
        return value.strip().lower()

    @model_validator(mode="after")
    def check_route_and_unit(self) -> "Dose":
        """A weight-based dose needs a body-weight route."""
        if self.unit == "mg/kg" and self.route not in {"oral", "iv"}:
            raise ValueError(f"unit mg/kg not supported for route {self.route!r}")
        return self
```

Use it at every boundary:

```python
# reading external data: validate, do not trust
dose = Dose.model_validate(json.loads(text))
doses = TypeAdapter(list[Dose]).validate_python(rows)

# writing: the model is the schema
Path("dose.json").write_text(dose.model_dump_json(indent=2))
schema = Dose.model_json_schema()
```

### Rules of thumb

- `extra="forbid"` by default. Allow extras only for models that intentionally carry arbitrary payload, and say so in a comment.
- Constrain fields with `Field(...)`: ranges, patterns, lengths. A constraint in the model replaces an `assert` somewhere else.
- Cross-field rules go in a `model_validator`. Single-field normalisation goes in a `field_validator`.
- Prefer `frozen=True`. Mutable models need `validate_assignment=True` so a later assignment is validated too.
- Validate once at the boundary, then pass models, not dicts, through the code. Functions take and return models.
- Settings and configuration use `pydantic-settings` (`BaseSettings`), which validates environment variables and config files the same way.
- Keep models in a `models.py` (or a `models/` package) per module, next to the code that uses them, with docstrings on the class and on non-obvious fields. `ty` checks the annotations, pydantic checks the values.

## Continuous integration

Each concern is its own workflow and its own required check, so a failure is visible by name in the pull request:

| Check | Workflow | Runs |
|-------|----------|------|
| `ruff` | `ruff.yml` | `ruff check` and `ruff format --check --diff` via `astral-sh/ruff-action` |
| `ty` | `ty.yml` | `tox -e ty` via `astral-sh/setup-uv` |
| `tests` | `ci-cd.yml` | the pytest matrix, aggregated into one job so the check name is stable |
| `docs` | `docs.yml` | the zensical build |

Workflows run on `pull_request` and on pushes to the protected branches, with `persist-credentials: false` on checkout. See [repository policies](repository-policies.md) for how the checks are required.

## Pre-commit

```bash
uv run pre-commit install        # once per checkout
uv run pre-commit run --all-files
```

The hooks run ruff (lint and format) and ty, plus the standard hygiene hooks (yaml, toml and json syntax, trailing whitespace, end of file, large files, merge conflict markers, private keys, debug statements). On a commit only the changed files are checked; run `--all-files` after adding a hook.

## Telling the agent

Put the essentials in the project `AGENTS.md` so every session knows them without reading this page:

```markdown
## Python
- Run `uv run ruff check --fix && uv run ruff format && uv run ty check` before finishing.
- Every data model is a pydantic `BaseModel` with `extra="forbid"` and field constraints. No dicts across module boundaries.
- Do not add `# noqa` or `# type: ignore`; fix the code or explain a per-file ignore.
- Tests live in `tests/`, run with `uv run pytest`.
```
