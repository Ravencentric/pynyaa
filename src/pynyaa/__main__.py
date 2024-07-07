def main() -> None:
    """
    Pretty simple CLI implementation.
    """
    import argparse

    from ._clients import Nyaa

    parser = argparse.ArgumentParser(prog="pynyaa", description="Get the JSON representation of a Nyaa torrent page.")
    parser.add_argument("url", type=str, help="Nyaa URL", metavar="https://nyaa.si/view/...")
    parser.add_argument("--indent", "-i", type=int, default=None, help="indentation level")

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--include", "-inc", type=str, nargs="+", default=None, help="keys to include")
    group.add_argument("--exclude", "-exc", type=str, nargs="+", default=None, help="keys to exclude")

    args = parser.parse_args()
    url = args.url.strip()
    indent = args.indent
    include = args.include
    exclude = args.exclude

    json = Nyaa().get(url).model_dump_json(indent=indent, include=include, exclude=exclude)

    print(json)


if __name__ == "__main__":
    main()
