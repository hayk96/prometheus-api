# Contributing

The prometheus-api uses GitHub to manage and review pull requests.

* If you are a new contributor see: [Steps to Contribute](#steps-to-contribute)

* If you have a minor fix or enhancement, feel free to submit a pull request.
* If you're considering a more complex change, please first share your ideas on our discussion [discussions](https://github.com/hayk96/prometheus-api/discussions/new/choose).
  This approach will prevent unnecessary effort and will undoubtedly provide both you and us with a great deal of inspiration.

* Relevant coding style guidelines and formatings are the [PEP 8](https://peps.python.org/pep-0008/).

* Be sure to sign off on the [DCO](https://github.com/probot/dco#how-it-works).

## Steps to Contribute

If you'd like to tackle an issue, please claim it by commenting on the GitHub issue to indicate your intention to work on it. This helps avoid multiple contributors working on the same issue simultaneously.

To quickly run the project locally and test your changes, please do the following:

```bash
git clone https://github.com/hayk96/prometheus-api.git
cd prometheus-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir docs/examples/docker/rules # this path is already included in .gitignore
python3 main.py --rule.path docs/examples/docker/rules --prom.addr http://localhost:9090 --web.enable-ui=true
```

We use [`ruff-action`](https://github.com/chartboost/ruff-action) for linting the code. This means the committed code can be reported by the linter when it exits with failures. In some cases, your changes can also be fixed or modified by the linter.

All our issues are regularly tagged, allowing you to filter down to the issues related to the components you are interested in working on.

## Pull Request Checklist

* Branch from the main branch and, if needed, rebase to the current main branch before submitting your pull request. If it doesn't merge cleanly with main you may be asked to rebase your changes.

* Commits should be as small as possible, while ensuring that each commit is correct independently.
* PR descriptions should contain comprehensive descriptions of all commits introduced by the appropriate PR. You can find and example [here](https://github.com/hayk96/prometheus-api/pull/11).
