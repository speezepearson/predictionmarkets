An ill-considered web app for running prediction markets.

Useful commands:

- Test: `mypy . && pytest`
- Run: `python -m predictionmarkets.server.plain_html` <!-- if changed, update ctrl-f "invocation-cmd" -->

Todo:

- MVP:

    - persistence
    - display probabilities in better ways than log-odds (ideally, user choice)

- Fancy stuff:

    - let market-creator limit per-participant exposure
    - CSRF

- Architecture:

    - make `Market` an interface, with multiple possible implementations
