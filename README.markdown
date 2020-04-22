An ill-considered web app for running prediction markets.

Useful commands:

- Test: `mypy . && pytest`
- Run: `python -m predictionmarkets.server`

Todo:

- MVP:

    - persistence
    - store and display market history
    - add authentication
    - let market-creator limit per-participant exposure
    - display probabilities in better ways than log-odds (ideally, user choice)
    - input validation

- Architecture:

    - make `Market` an interface, with multiple possible implementations
