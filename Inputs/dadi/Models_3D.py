import sys
import os
import numpy as np
import dadi
from datetime import datetime


##########################################################################################
# MODELS
##########################################################################################

def split_nomig(params, ns, pts):
    """
    Model with split between pop 1 and (2,3), then split between 2 and 3.
    Migration does not occur between any population pair.
    """
    #6 parameters	
    nu1, nuA, nu2, nu3, T1, T2 = params
    xx = dadi.Numerics.default_grid(pts)
    phi = dadi.PhiManip.phi_1D(xx)
    phi = dadi.PhiManip.phi_1D_to_2D(xx, phi)
    phi = dadi.Integration.two_pops(phi, xx, T1, nu1=nu1, nu2=nuA, m12=0, m21=0)
    phi = dadi.PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = dadi.Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=0, m21=0, m23=0, m32=0, m13=0, m31=0)
    fs = dadi.Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def split_symmig_all(params, ns, pts):
    """
    Model with split between pop 1 and (2,3), then split between 2 and 3.
    Migration is symmetrical between all population pairs (ie 1<->2, 2<->3, and 1<->3).
    """
    #10 parameters
    nu1, nuA, nu2, nu3, mA, m1, m2, m3, T1, T2 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1=nu1, nu2=nuA, m12=mA, m21=mA)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=m1, m21=m1, m23=m2, m32=m2, m13=m3, m31=m3)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def split_symmig_adjacent(params, ns, pts):
    """
    Model with split between pop 1 and (2,3), then split between 2 and 3. Assume 2 occurs
    in between populations 1 and 3, which do not come in to contact with one another.
    Migration is symmetrical between 'adjacent' population pairs (ie 1<->2, 2<->3, but not 1<->3).
    """
    #9 parameters
    nu1, nuA, nu2, nu3, mA, m1, m2, T1, T2 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1=nu1, nu2=nuA, m12=mA, m21=mA)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=m1, m21=m1, m23=m2, m32=m2, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def refugia_1(params, ns, pts):
    """
    Model with split between pop 1 and (2,3), gene flow does not occur. Split between pops
    2 and 3, gene flow does not occur. Period of symmetric secondary contact occurs between 
    adjacent populations (ie 1<->2, 2<->3, but not 1<->3) after all splits are complete. 
    longest isolation
    """
    #9 parameters
    nu1, nuA, nu2, nu3, m1, m2, T1, T2, T3 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1=nu1, nu2=nuA, m12=0, m21=0)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=0, m21=0, m23=0, m32=0, m13=0, m31=0)
    phi = Integration.three_pops(phi, xx, T3, nu1=nu1, nu2=nu2, nu3=nu3, m12=m1, m21=m1, m23=m2, m32=m2, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def refugia_2(params, ns, pts):
    """
    Model with split between pop 1 and (2,3), gene flow does not occur. Split between pops
    2 and 3, with gene flow. After appearance of 2 and 3, gene flow also occurs between 1 
    and 2.
    shorter isolation
    """
    #8 parameters
    nu1, nuA, nu2, nu3, m1, m2, T1, T2 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1=nu1, nu2=nuA, m12=0, m21=0)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=m1, m21=m1, m23=m2, m32=m2, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def refugia_3(params, ns, pts):
    """
    Model with split between pop 1 and (2,3), gene flow does not occur, but then 
    secondary contact occurs. Split between pops 2 and 3 occurs with gene flow, and gene flow
    happens between 1 and 2 as well.
    shortest isolation
    """
    #10 parameters
    nu1, nuA, nu2, nu3, mA, m1, m2, T1a, T1b, T2 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1a, nu1=nu1, nu2=nuA, m12=0, m21=0)
    phi = Integration.two_pops(phi, xx, T1b, nu1=nu1, nu2=nuA, m12=mA, m21=mA)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=m1, m21=m1, m23=m2, m32=m2, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def ancmig_3(params, ns, pts):
    """
    Model with split between pop 1 and (2,3), with gene flow, which then stops. Split 
    between pops 2 and 3, gene flow does not occur at all.
    longest isolation
    """
    #8 parameters
    nu1, nuA, nu2, nu3, mA, T1a, T1b, T2 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1a, nu1=nu1, nu2=nuA, m12=mA, m21=mA)
    phi = Integration.two_pops(phi, xx, T1b, nu1=nu1, nu2=nuA, m12=0, m21=0)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=0, m21=0, m23=0, m32=0, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def ancmig_2(params, ns, pts):
    """
    Model with split between pop 1 and (2,3), with gene flow. Split 
    between pops 2 and 3, and all gene flow ceases.
    shorter isolation
    """
    #7 parameters
    nu1, nuA, nu2, nu3, mA, T1, T2 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1=nu1, nu2=nuA, m12=mA, m21=mA)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=0, m21=0, m23=0, m32=0, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def ancmig_1(params, ns, pts):
    """
    Model with split between pop 1 and (2,3), with gene flow. Split 
    between pops 2 and 3 with gene flow, then all gene flow ceases.
    shortest isolation
    """
    #10 parameters
    nu1, nuA, nu2, nu3, mA, m1, m2, T1, T2, T3 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1=nu1, nu2=nuA, m12=mA, m21=mA)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=m1, m21=m1, m23=m2, m32=m2, m13=0, m31=0)
    phi = Integration.three_pops(phi, xx, T3, nu1=nu1, nu2=nu2, nu3=nu3, m12=0, m21=0, m23=0, m32=0, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def sim_split_no_mig(params, ns, pts):
    """
    Model with simultaneous split between pop 1, 2 and 3, gene flow does not occur. 
    """
    #4 parameters
    nu1, nu2, nu3, T1 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T1, nu1=nu1, nu2=nu2, nu3=nu3, m12=0, m21=0, m23=0, m32=0, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def sim_split_sym_mig_all(params, ns, pts):
    """
    Model with simultaneous split between pop 1, 2 and 3
    Migration is symmetrical between all population pairs (ie 1<->2, 2<->3, and 1<->3).
    """
    #7 parameters
    nu1, nu2, nu3, m1, m2, m3, T1 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T1, nu1=nu1, nu2=nu2, nu3=nu3, m12=m1, m21=m1, m23=m2, m32=m2, m13=m3, m31=m3)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def sim_split_sym_mig_adjacent(params, ns, pts):
    """
    Model with simultaneous split between pop 1, 2 and 3
    Migration is symmetrical between 'adjacent' population pairs (ie 1<->2, 2<->3, but not 1<->3).
    """
    #6 parameters
    nu1, nu2, nu3, m1, m2, T1 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T1, nu1=nu1, nu2=nu2, nu3=nu3, m12=m1, m21=m1, m23=m2, m32=m2, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs
    
def sim_split_refugia_sym_mig_all(params, ns, pts):
    """
    Model with simultaneous split between pop 1, 2 and 3 followed by isolation. Period of symmetric secondary contact occurs between 
    all populations after all splits are complete. 
 
    """
    #8 parameters
    nu1, nu2, nu3, m1, m2, m3, T1, T2 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T1, nu1=nu1, nu2=nu2, nu3=nu3, m12=0, m21=0, m23=0, m32=0, m13=0, m31=0)
    phi = Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=m1, m21=m1, m23=m2, m32=m2, m13=m3, m31=m3)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def sim_split_refugia_sym_mig_adjacent(params, ns, pts):
    """
    Model with simultaneous split between pop 1, 2 and 3 followed by isolation. Period of symmetric secondary contact occurs between 
    adjacent populations (ie 1<->2, 2<->3, but not 1<->3) after all splits are complete. 
 
    """
    #7 parameters
    nu1, nu2, nu3, m1, m2, T1, T2 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T1, nu1=nu1, nu2=nu2, nu3=nu3, m12=0, m21=0, m23=0, m32=0, m13=0, m31=0)
    phi = Integration.three_pops(phi, xx, T2, nu1=nu1, nu2=nu2, nu3=nu3, m12=m1, m21=m1, m23=m2, m32=m2, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs

def split_nomig_human(params, ns, pts):
    """
    Model with split between pop 1 and (2,3), then split between 2 and 3.
    Migration does not occur between any population pair, size change
    """
    #10 parameters	
    nu1a, nuA, nu2a, nu3a, nu1b, nu2b, nu3b, T1, T2, T3 = params
    xx = Numerics.default_grid(pts)
    phi = PhiManip.phi_1D(xx)
    phi = PhiManip.phi_1D_to_2D(xx, phi)
    phi = Integration.two_pops(phi, xx, T1, nu1a, nu2a=nuA, m12=0, m21=0)
    phi = PhiManip.phi_2D_to_3D_split_2(xx, phi)
    phi = Integration.three_pops(phi, xx, T2, nu1a, nu2a, nu3a, m12=0, m21=0, m23=0, m32=0, m13=0, m31=0)
    phi = Integration.three_pops(phi, xx, T3, nu1b, nu2b, nu3b, m12=0, m21=0, m23=0, m32=0, m13=0, m31=0)
    fs = Spectrum.from_phi(phi, ns, (xx,xx,xx))
    return fs
 