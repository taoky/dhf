# Debian Haskell Finder

Parse Packages.gz files and find Haskell packages in Debian.

This very simple script is written in Python,
as it sounds like a recursive problem if it was written in Haskell.

## Usage

```console
> python dhf.py --help
usage: Debian Haskell Finder: find Haskell packages in Debian
       [-h] [--dist DIST] [--arch ARCH] [--mirror MIRROR] [--update] [--clean]
       [package]

positional arguments:
  package          package name to search for

options:
  -h, --help       show this help message and exit
  --dist DIST      distribution to search in
  --arch ARCH      architecture to search for
  --mirror MIRROR  mirror to search in
  --update         always download Packages.gz for current request
  --clean          remove /tmp/dhf and other args are ignored
> python dhf.py unordered-containers
['libghc-unordered-containers-dev']
> python dhf.py base
['ghc']
> python dhf.py containers
['ghc']
> python dhf.py filepath
['ghc']
> python dhf.py directory
['ghc']
> python dhf.py stm
['ghc']
```
