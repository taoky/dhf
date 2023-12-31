#!/usr/bin/env python3
# Parse Packages.gz files and find Haskell packages in Debian
import argparse
import shutil
import urllib.request
import gzip
from pathlib import Path
from typing import Optional
import re
from dataclasses import dataclass

# edit this to add mirrors you favor
MIRROR_URLS = {
    None: "http://deb.debian.org/debian/",
    "ustc": "http://mirrors.ustc.edu.cn/debian/",
    "tuna": "http://mirrors.tuna.tsinghua.edu.cn/debian/",
    "bfsu": "http://mirrors.bfsu.edu.cn/debian/",
}
CACHE_DIR = Path("/tmp/dhf")
PACKAGE_NAME = re.compile(r"^libghc-(.+)-dev-(\d.+)$")


def ungzip(from_: Path, to: Path) -> None:
    with gzip.open(from_, "rb") as f:
        content = f.read()
    with open(to, "wb") as f:
        f.write(content)


class Cache:
    def __init__(self, update_only: bool) -> None:
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

    @staticmethod
    def cache_args(parser: argparse.ArgumentParser) -> None:
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

    @staticmethod
    def continue_or_clean(args) -> None:
        if args.clean:
            shutil.rmtree(CACHE_DIR)
            print(f"Cache ({CACHE_DIR}) cleaned.")
            exit(0)


def dhf_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dist", help="distribution to search in", default="stable")
    parser.add_argument("--arch", help="architecture to search for", default="amd64")
    parser.add_argument("--mirror", help="mirror to search in", default=None)


def construct_url(mirror: Optional[str], dist: str, arch: str) -> str:
    return (
        MIRROR_URLS[mirror] + "dists/" + dist + "/main/binary-" + arch + "/Packages.gz"
    )


@dataclass
class Package:
    name: str
    description: Optional[str]
    version: Optional[str]
    provides: list[tuple[str, str]]


def parse_packages(packages_path: Path) -> dict[str, Package]:
    name = None
    description = None
    version = None
    ghc_packages: list[tuple[str, str]] = []
    res = {}
    with open(packages_path, "r") as f:
        for line in f:
            if line.startswith("Package: "):
                name = line[9:].strip()
            elif line.startswith("Description: "):
                description = line[13:].strip()
            elif line.startswith("Version: "):
                version = line[9:].strip()
            elif line.startswith("Provides: "):
                provides = [i.split(" ")[0] for i in line[10:].split(", ")]
                ghc_packages = []
                for i in provides:
                    m = PACKAGE_NAME.match(i)
                    if m:
                        ghc_packages.append((m.group(1), m.group(2)))
            elif line == "\n":
                if name is not None and ghc_packages:
                    res[name] = Package(name, description, version, ghc_packages)
                name = None
                description = None
                version = None
                ghc_packages = []
    return res


def main(args) -> None:
    cache = Cache(update_only=args.update)
    packages_path = cache.get(args.mirror, args.dist, args.arch)
    package_name = args.package
    packages = parse_packages(packages_path)
    for p in packages:
        package = packages[p]
        for pname, pversion in package.provides:
            if pname == package_name:
                print(f"{p} ({package.version} provides {package_name} {pversion})")
                print(packages[p].description)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("dhf")
    parser.add_argument("package", help="package name to search for", nargs="?")
    dhf_args(parser)
    Cache.cache_args(parser)
    args = parser.parse_args()
    Cache.continue_or_clean(args)
    if args.package is None:
        parser.print_help()
        exit(1)
    main(args)
