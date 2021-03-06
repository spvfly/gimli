#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""For the manager look at BERT https://gitlab.com/resistivity-net/bert."""

import numpy as np
import matplotlib.pyplot as plt

import pygimli as pg

#TODO Gassmann's equation for fluid substitution

def slownessWyllie(phi, sat=1, vm=4000, vw=1484, va=343,
                   mesh=None, meshI=None, fill=None):
    r"""
    Return slowness :math:`s` after Wyllie time-average equation.

    .. math::
        s = (1-\phi) \cdot\frac{1}{v_m} + \phi \cdot S \cdot\frac{1}{v_w} +
        \phi \cdot(1 - S) \cdot\frac{1}{v_a}

    * :math:`\phi` - porosity 0.0 --1.0
    * :math:`S`    - fluid saturation 0.0 --1.0 [sat]
    * :math:`v_m`  - velocity of matrix [4000 m/s]
    * :math:`v_w`  - velocity of water [1484 m/s]
    * :math:`v_a`  - velocity of air [343 m/s]

    If mesh is not None the resulting values are calculated for each cell of
    the mesh.
    All parameter can be scalar, array of length mesh.cellCount()
    or callable(pg.cell).
    If meshI is not None the result is interpolated to meshI.cellCenters()
    and prolonged (if fill ==1).

    Examples
    --------

    WRITEME


    """
    if mesh is None:
        return 1./vm * (1.-phi) + 1./vw * phi * sat + 1./va * phi * (1. - sat)
    else:
        raise BaseException('TODO')

    if meshI:
        raise BaseException('TODO')

    if fill:
        raise BaseException('TODO')


def wyllie(phi, sat=1, vm=4000, vw=1600, va=330):
    """Return slowness after Wyllie time-average equation."""
    return 1./vm * (1-phi) + phi * sat * 1./vw + phi * (1 - sat) * 1./va


def transFwdWylliePhi(sat=1, vm=4000, vw=1600, va=330):
    """Wyllie transformation function porosity(slowness)."""
    if va != 330 or sat != 1.0:
        raise BaseException('TODO')
    return pg.RTransLin(1./vw - 1./vm, 1./vm)


def transInvWylliePhi(sat=1, vm=4000, vw=1600, va=330):
    """Inverse Wyllie transformation function porosity(slowness)."""
    if va != 330 or sat != 1.0:
        raise BaseException('TODO')
    a1 = 1./vm
    b1 = 1./vw - 1./vm
    return pg.RTransLin(1./b1, -a1/b1)


def transFwdWyllieS(phi, vm=4000, vw=1600, va=330):
    """Wyllie transformation function slowness(saturation)."""
    if va != 330.0:
        print(va, va is not 330.0)
        raise BaseException('TODO')
    return pg.RTransLin((1/vw-1./va)*phi, (1-phi)/vm+phi/va)


def transInvWyllieS(phi, vm=4000, vw=1600, va=330):
    """Inverse Wyllie transformation function slowness(saturation)."""
    a2 = 1./vm * (1 - phi) + phi * 1./va
    b2 = phi * (1./vw - 1./va)
    return pg.RTransLin(1./b2, -a2/b2)


def test_Wyllie():
    """Test Wyllie and Transformations."""
    import unittest

    phivec = np.arange(0, 0.5, 0.01)
    swvec = np.arange(0, 1, 0.01)

    phi0 = 0.4

    tIWPhi = transInvWylliePhi()
    tIWS = transInvWyllieS(phi0)
    tFWPhi = transFwdWylliePhi()
    tFWS = transFwdWyllieS(phi0)

    ax = plt.subplots()[1]
    # direct function
    rA = wyllie(phivec)
    rS = wyllie(phi0, swvec)

    ax.semilogy(phivec, rA, 'b-')
    ax.semilogy(swvec, rS, 'r-')
    # forward transformation
    fA = tFWPhi.trans(phivec)
    fS = tFWS.trans(swvec)
    np.testing.assert_allclose(rA, fA, rtol=1e-12)
    np.testing.assert_allclose(rS, fS, rtol=1e-12)

    ax.semilogy(phivec, fA, 'bx', markersize=10)
    ax.semilogy(swvec, fS, 'rx', markersize=10)

    # inverse transformation
    iA = tIWPhi.invTrans(phivec)
    iS = tIWS.invTrans(swvec)
    np.testing.assert_allclose(rA, iA, rtol=1e-12)
    np.testing.assert_allclose(rS, iS, rtol=1e-12)

    ax.semilogy(phivec, iA, 'bo')
    ax.semilogy(swvec, iS, 'ro')

    plt.show()


if __name__ == "__main__":
    pass
