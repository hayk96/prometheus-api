import argparse


def arg_parser() -> dict:
    """
    Reads command-line arguments and returns
    a dictionary of the passed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Extended HTTP API service for Prometheus",
        usage="python3 %(prog)s [option]")
    required_params = parser.add_argument_group("required parameters")

    required_params.add_argument(
        "--rule.path",
        required=True,
        type=str,
        help="Prometheus rules directory path")

    required_params.add_argument(
        "--config.file",
        required=True,
        type=str,
        help="Prometheus configuration file path")

    required_params.add_argument(
        "--prom.addr",
        required=True,
        type=str,
        help="URL of Prometheus server, e.g. http://localhost:9090")

    parser.add_argument(
        "--web.listen-address",
        required=False,
        type=str,
        default="0.0.0.0:5000",
        help="address to listen on for API"
    )

    parser.add_argument(
        "--file.prefix",
        required=False,
        type=str,
        help="a prefix of filenames generated by the server"
    )

    parser.add_argument(
        "--file.extension",
        required=False,
        type=str,
        default=".yml",
        help="rule files will be created with this suffix"
    )

    parser.add_argument(
        "--log.level",
        required=False,
        type=str,
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="only log messages with the given severity or above. One of: [debug, info, warning, error]"
    )

    parser.add_argument(
        "--web.enable-ui",
        required=False,
        type=str,
        default="false",
        choices=["true", "false"],
        help="enable web management UI"
    )

    return parser.parse_args().__dict__
