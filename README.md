# kpex-plugin-kqcircuits

Development scaffold for exporting [KPEX](https://iic-jku.github.io/kpex-website/)
`PEX25D` scenes through [KQCircuits](https://iqm-finland.github.io/KQCircuits/)
to `Elmer`.

**The exporter is not implemented yet.** This repository provides package discovery,
the exporter interface, contract tests and release infrastructure for the partners
who will implement the scene translation. Calling the exporter reports that it is
not implemented and writes no solver files.

## Intended use

The planned route is:

```text
resolved PEX25D scene → KQCircuits simulation inputs → Gmsh/Elmer run
```

The motivation is access to the `KQCircuits` simulation workflow, including its
mesh-refinement controls. This is an alternative to the existing
[`kpex-plugin-elmer`](https://github.com/iic-jku/kpex-plugin-elmer).
It does not depend on that plugin or copy its mesher.

## Install for development

Use Python `3.12` or later and Poetry `2`:

```bash
poetry install
poetry run pex25d exporters
```

The exporter list includes `kpex-plugin-kqcircuits:kqcircuits`.
Discovery and factory construction work without `KQCircuits`, `Gmsh` or `Elmer`
installed. The scaffold does not declare a `KQCircuits` dependency until an actual
adapter has been qualified against a specific version and installation method.

This command demonstrates the current implementation boundary:

```bash
poetry run pex25d export testdata/two_nets.pex25d \
  --to kqcircuits --out-dir output_kqcircuits
```

It exits with status `3` and explains that export is not implemented. It does not
create the output directory. Installing this package therefore does not yet provide
capacitance extraction through `KQCircuits`.

## Check changes

```bash
poetry run pytest
poetry build
poetry run twine check --strict dist/*
```

Tests cover registration through the real KPEX registry, lazy loading, coexistence
with other namespace packages, the CLI failure status and preservation of inputs
and existing files. Numerical export and simulation tests belong with the actual
adapter implementation.

`klayout_pex_plugins` is an implicit namespace. Do not add an `__init__.py` at that
level: it would interfere with sibling plugins. Only the `kqcircuits` child package
belongs to this distribution.

## Migration

Moving from `klayout-pex-plugin-kqcircuits`? Install the renamed plugins in a fresh
environment with `kpex>=0.12.0` to avoid registering the same exporters twice.

## Compatibility and licence

- `kpex>=0.12.0,<1`
- Plugin API `v1` is provisional and may change before it is declared stable
- GPL-3.0-or-later, matching the existing KPEX plugins; see [LICENSE](https://github.com/iic-jku/kpex-plugin-kqcircuits/blob/main/LICENSE)

## Acknowledgements

This project is funded by the JKU/SAL [IWS Lab](https://research.jku.at/de/projects/jku-lit-sal-intelligent-wireless-systems-lab-iws-lab/), a collaboration of [Johannes Kepler University](https://jku.at) and [Silicon Austria Labs](https://silicon-austria-labs.com).

This project is further funded by the European project [ODE4EC-AMS](https://ode4ec.eu/projects/ams/), which has received funding from the Chips Joint Undertaking (Chips JU) under Grant Agreement No 101252962.

Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the Chips Joint Undertaking. Neither the European Union nor the granting authority can be held responsible for them.

<p align="center">
  <a href="https://iic.jku.at" target="_blank">
    <img src="https://github.com/iic-jku/kpex-website/raw/main/figures/funding/iic-jku.svg" alt="Johannes Kepler University: Institute for Integrated Circuits and Quantum Computing" width="300"/>
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://silicon-austria-labs.com" target="_blank">
    <img src="https://github.com/iic-jku/kpex-website/raw/main/figures/funding/silicon-austria-labs-logo.svg" alt="Silicon Austria Labs" width="300"/>
  </a>
</p>

<p align="center">
  <a href="https://ode4ec.eu/projects/ams/" target="_blank">
    <img src="https://github.com/iic-jku/kpex-website/raw/main/figures/funding/eu-cofunded.svg" alt="Co-funded by the European Union" width="300"/>
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.chips-ju.europa.eu" target="_blank">
    <img src="https://github.com/iic-jku/kpex-website/raw/main/figures/funding/chips-ju.png" alt="Chips Joint Undertaking" width="300"/>
  </a>
</p>
