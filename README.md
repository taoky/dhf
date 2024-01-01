# Debian Haskell Finder

Parse Packages.gz files and find Haskell packages in Debian.

This very simple script is written in Python,
as it sounds like a recursive problem if it was written in Haskell.

## Usage

Scripts does not require any dependencies.

### dhf.py

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
libghc-unordered-containers-dev (0.2.17.0-2+b2 provides unordered-containers 0.2.17.0-1d16d)
Efficient hashing-based container types
> python dhf.py base
ghc (9.0.2-4 provides base 4.15.1.0-6a406)
The Glasgow Haskell Compilation system
> python dhf.py containers
ghc (9.0.2-4 provides containers 0.6.4.1-31c3b)
The Glasgow Haskell Compilation system
> python dhf.py filepath
ghc (9.0.2-4 provides filepath 1.4.2.1-4459f)
The Glasgow Haskell Compilation system
> python dhf.py directory
ghc (9.0.2-4 provides directory 1.3.6.2-311c9)
The Glasgow Haskell Compilation system
> python dhf.py stm
ghc (9.0.2-4 provides stm 2.5.0.0-4cba8)
The Glasgow Haskell Compilation system
> python dhf.py --dist sid text-builder-dev
libghc-text-builder-dev-dev (0.3.3.2-1+b2 provides text-builder-dev 0.3.3.2-94185)
edge of developments for "text-builder"
```

### makehtml.py

This script generates HTML file with all Haskell packages in Debian.

```console
> python makehtml.py --help
usage: dhf-makehtml [-h] [--dist DIST] [--arch ARCH] [--mirror MIRROR] [--update] [--clean] [output]

positional arguments:
  output           HTML output file path

options:
  -h, --help       show this help message and exit
  --dist DIST      distribution to search in
  --arch ARCH      architecture to search for
  --mirror MIRROR  mirror to search in
  --update         always download Packages.gz for current request
  --clean          remove /tmp/dhf and other args are ignored
> python makehtml.py output.html
```

## Alternative

Install `dctrl-tools` and use `grep-aptavail` (thanks @billchenchina):

```console
> grep-aptavail -F Provides: libghc-containers-dev -s Package -n
ghc
> grep-aptavail -F Provides: libghc-unordered-containers-dev -s Package -n
libghc-unordered-containers-dev
```
