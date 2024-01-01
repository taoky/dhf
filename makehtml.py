import dhf as d
import argparse
from pathlib import Path
from typing import TextIO
import html


def main(args, f: TextIO) -> None:
    cache = d.Cache(update_only=args.update)
    packages_path = cache.get(args.mirror, args.dist, args.arch)
    packages = d.parse_packages(packages_path)
    rev_packages: dict[str, d.Package] = {}
    for p in packages.values():
        for pname, pversion in p.provides:
            # print(f"{p} ({package.version} provides {pname} {pversion})")
            rev_packages[f"{pname} {pversion}"] = p
    e = html.escape
    title = e(f"Debian Haskell Packages for {args.dist} {args.arch}")
    f.write(
        f"""<!DOCTYPE html><html>
    <head><title>{title}</title></head>
    <body><h1>{title}</h1>
    <table><thead>
    <tr><th>Haskell Package</th><th>Debian Package</th><th>Description</th></tr>
    </thead><tbody>"""
    )
    for k, v in rev_packages.items():
        version = v.version if v.version else "(unknown version)"
        description = v.description if v.description else "(no description)"
        f.write(f"<tr><td>{e(k)}</td><td>{e(v.name)} {e(version)}</td><td>{e(description)}</td></tr>")
    f.write(
        """</tbody></body></html>"""
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("dhf-makehtml")
    parser.add_argument("output", help="HTML output file path", nargs="?", type=Path)
    d.dhf_args(parser)
    d.Cache.cache_args(parser)
    args = parser.parse_args()
    d.Cache.continue_or_clean(args)
    if args.output is None:
        parser.print_help()
        exit(1)
    with open(args.output, "w") as f:
        main(args, f)
