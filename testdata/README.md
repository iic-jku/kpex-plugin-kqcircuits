# Scene fixture

`two_nets.pex25d` is the hand-written fixture from
[`kpex-plugin-gmsh` at `f170951`](https://github.com/iic-jku/kpex-plugin-gmsh/blob/f170951/testdata/two_nets.pex25d),
under GPL-3.0-or-later.

It contains two named nets, a floating conductor, a via, a ground plane and nested
conformal dielectrics. It is used here to exercise KPEX parsing, resolution and
dispatch into the unfinished exporter. Its dimensions are synthetic; it is not a
PDK calibration reference or evidence that these geometries can already be exported.
