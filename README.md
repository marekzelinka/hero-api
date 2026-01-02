# Hero DB

This project is represents an simpple API with teams, heroes and missions.

## Features

- Data stored in SQLite
- CRUD for teams, heroes and missions
- OpenAPI-based REST API

## Setup

This project uses the modern `pyproject.toml` standard for dependency management and requires the `uv` tool to manage the environment.

1.  **Ensure `uv` is installed** globally on your system. If not, follow the official installation guide for [`uv`](https://docs.astral.sh/uv/).

2.  **Install deps**

    ```sh
    uv sync
    ```

3.  **Start app in dev mode**

    ```sh
    uv run uvicorn app.main:app --reload
    ```

4.  **Visit OpenAPI docs in browser**

    ```sh
    open http://localhost:8000/docs
    ```

## Development

1. Setup your editor to work with [ruff](https://docs.astral.sh/ruff/editors/setup/) and [ty](https://docs.astral.sh/ty/editors/).

2. Install the [justfile extension](https://just.systems/man/en/editor-support.html) for your editor, and use the provided `./justfile` to run commands.

## Todo

- [ ] public APIs
- [ ] explore using `neon` as db provider
