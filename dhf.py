#!/usr/bin/env python3
# Parse Packages.gz files and find Haskell packages in Debian
import argparse
import shutil
import urllib.request
import gzip
from pathlib import Path
from typing import Optional

# edit this to add mirrors you favor
MIRROR_URLS = {
    None: "http://deb.debian.org/debian/",
    "ustc": "http://mirrors.ustc.edu.cn/debian/",
    "tuna": "http://mirrors.tuna.tsinghua.edu.cn/debian/",
    "bfsu": "http://mirrors.bfsu.edu.cn/debian/",
}
CACHE_DIR = Path("/tmp/dhf")


def ungzip(from_: Path, to: Path) -> None:
    with gzip.open(from_, "rb") as f:
        content = f.read()
    with open(to, "wb") as f:
        f.write(content)


class Cache:
    def __init__(self, update_only) -> None:
        self.update_only = update_only
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def get(self, mirror: Optional[str], dist: str, arch: str) -> Path:
        raw_name = str(mirror) + "-" + dist + "-" + arch + ".Packages"
        gz_name = raw_name + ".gz"
        raw_path = CACHE_DIR / raw_name
        gz_path = CACHE_DIR / gz_name
        if not self.update_only:
            if not raw_path.exists() and gz_path.exists():
                ungzip(gz_path, raw_path)
            if raw_path.exists():
                return raw_path
        url = construct_url(mirror, dist, arch)
        request = urllib.request.Request(url)
        with urllib.request.urlopen(request) as f:
            content = f.read()
        with open(gz_path, "wb") as f:
            f.write(content)
        content = gzip.decompress(content)
        with open(raw_path, "wb") as f:
            f.write(content)
        return raw_path


def construct_url(mirror: Optional[str], dist: str, arch: str) -> str:
    return (
        MIRROR_URLS[mirror] + "dists/" + dist + "/main/binary-" + arch + "/Packages.gz"
    )


def construct_name(package: str) -> str:
    return "libghc-" + package + "-dev"


def parse_packages(packages_path: Path, package: str) -> list[str]:
    name = None
    res = []
    with open(packages_path, "r") as f:
        for line in f:
            if line.startswith("Package: "):
                name = line[9:].strip()
            elif line.startswith("Provides: "):
                if package in line[10:]:
                    assert name is not None
                    res.append(name)
            elif line == "\n":
                name = None
    return res


def main(args):
    cache = Cache(update_only=args.update)
    packages_path = cache.get(args.mirror, args.dist, args.arch)
    package_name = construct_name(args.package)
    res = parse_packages(packages_path, package_name)
    print(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Debian Haskell Finder: find Haskell packages in Debian"
    )
    parser.add_argument("package", help="package name to search for", nargs="?")
    parser.add_argument("--dist", help="distribution to search in", default="stable")
    parser.add_argument("--arch", help="architecture to search for", default="amd64")
    parser.add_argument("--mirror", help="mirror to search in", default=None)
    parser.add_argument(
        "--update",
        help="always download Packages.gz for current request",
        action="store_true",
    )
    parser.add_argument(
        "--clean",
        help="remove /tmp/dhf and other args are ignored",
        action="store_true",
    )
    args = parser.parse_args()
    if args.clean:
        shutil.rmtree(CACHE_DIR)
        print(f"Cache ({CACHE_DIR}) cleaned.")
    else:
        if args.package is None:
            parser.print_help()
            exit(1)
        main(args)
