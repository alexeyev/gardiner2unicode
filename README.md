# gardiner2unicode: Mapping Egyptian Hieroglyphs

A Python 3.9+ package that
* provides a convenient out-of-the-box way to access the mapping 
of [Gardiner's Sign List](https://en.wikipedia.org/wiki/Gardiner%27s_sign_list) codes to unicode IDs;
* generates hieroglyphs as images.

A list of hieroglyphs was copied from 
[this Wikipedia template](https://en.wikipedia.org/w/index.php?title=Template:List_of_hieroglyphs&action=edit).

A 2.06 version of [NewGardiner font](https://mjn.host.cs.st-andrews.ac.uk/egyptian/fonts/newgardiner.html) is used
by default. Please note that since 2.05 its license is [OFL 1.1](https://scripts.sil.org/cms/scripts/page.php?item_id=OFL_web).

One can use any other font with `UnicodeGlyphGenerator`.


![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)
[![PyPI version][pypi_badge]][pypi_link]
[![Downloads](https://pepy.tech/badge/gardiner2unicode)](https://pepy.tech/project/gardiner2unicode)
[![CI](https://github.com/alexeyev/gardiner2unicode/actions/workflows/ci.yml/badge.svg)](https://github.com/alexeyev/gardiner2unicode/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[pypi_badge]: https://badge.fury.io/py/gardiner2unicode.svg
[pypi_link]: https://pypi.python.org/pypi/gardiner2unicode

## Installation

    pip install -U gardiner2unicode

### Breaking changes in 1.0.0

* `UnicodeGlyphGenerator(bkgr_color=...)` -> `UnicodeGlyphGenerator(fill_color=...)`
  (the argument is the *text fill* colour; the old name was misleading).
* `GardinerToUnicodeMap.to_gardiner_from_hex(hex=...)` -> `to_gardiner_from_hex(hex_code=...)`
  (the previous name shadowed the built-in `hex`).
* `GardinerToUnicodeMap` now precomputes all derived lookup tables at construction
  time, so every `to_*` method is an O(1) dictionary access (no `@lru_cache`,
  no per-call `int(..., 16)` / `chr(...)`).
* Minimum supported Python is now 3.9.

## Usage example

```python
from gardiner2unicode import GardinerToUnicodeMap, UnicodeGlyphGenerator

g2u = GardinerToUnicodeMap()
print(g2u.to_unicode_hex("A1"))

ugg = UnicodeGlyphGenerator()
ugg.generate_image("𓉓", save_path_png="O3_image.png")
```
Output:

`00013000`

![O3](O3_image.png?raw=true "Generated O3 image: a combination of a house, an oar, a tall loaf and a beer jug.")

## How to cite

Please cite this repository if you use this work in your research.

```bibtex
@misc{gardiner2unicode2021alekseev,
  title     = {{alexeyev/gardiner2unicode: Mapping Egyptian Hieroglyphs}},
  author    = {Anton Alekseev}, 
  year      = {2021},
  url       = {https://github.com/alexeyev/gardiner2unicode},
  language  = {english},
  publisher = {GitHub}, 
  journal   = {GitHub repository},  
  howpublished = {\url{https://github.com/alexeyev/gardiner2unicode/}}, 
}
```

## Development

Install the package together with the development dependencies and run the
linter and the test suite:

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

`pytest` is configured (see `pyproject.toml`) to also produce a coverage report.

## Links

* [NewGardiner font](https://mjn.host.cs.st-andrews.ac.uk/egyptian/fonts/newgardiner.html)
* [Gardiner's Sign List](https://en.wikipedia.org/wiki/Gardiner%27s_sign_list)