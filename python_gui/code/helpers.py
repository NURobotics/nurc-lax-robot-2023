import numpy as np
import sympy as sym
import dill
import time
from tqdm import tqdm

from geometry import *

#-----------GEOMETRIC FUNCTIONS-----------#

def SOnAndRnToSEn(R, p):
           
    #do type checking for the matrix types
    if type(R) == list:
        R = np.matrix(R)
        
    n = R.shape[0]
    if ((R.shape[0] != R.shape[1]) or                               #R is NP array or Sym matrix
        ((type(p) is np.ndarray and max(p.shape) != R.shape[0]) or  #p is NP array and shape mismatch or.. 
          ((isinstance(p, list) or isinstance(p, sym.Matrix)) and 
            ( len(p) != R.shape[0] ))   )  ):                       #p is Sym matrix or "list" and shape mismatch
        raise Exception(f"Shape of R {R.shape} and p ({len(p)}) mismatch; exiting.")
        return None
        
    #construct a matrix based on returning a Sympy Matrix
    if isinstance(R, sym.Matrix) or isinstance(p, sym.Matrix): 
        #realistically one of these needs to be symbolic to do this

        if isinstance(R, np.ndarray) or isinstance(p, np.ndarray):
            raise Exception("R and p cannot mix/match Sympy and Numpy types")
            return None
        
        G = sym.zeros(n+1)
        G[:n, n] = sym.Matrix(p)
    
    #construct a matrix based on returning a Numpy matrix
    elif isinstance(R, np.ndarray) or isinstance(R, list):
        G = np.zeros([n+1, n+1])
        # print(f"\nSOnAndRnToSEn Debug: \n\nR:\n{R}    \n\np:\n{p}   ")
        G[:n, n] = np.array(p).T
        
    else:
        raise Exception("Error: type not recognized")
        return None
    
    G[:n,:n] = R
    G[-1,-1] = 1
    return G  

def SEnToSOnAndRn(SEnmat):
    '''Decomposes a SE(n) vector into its rotation matrix and displacement components.
    '''
    if isinstance(SEnmat, list):
        SEnmat = np.matrix(SEnmat)
    n = SEnmat.shape[0]
    return SEnmat[:(n-1), :(n-1)], SEnmat[:(n-1), n-1]

def HatVector3(w):
    '''Turns a vector in R3 to a skew-symmetric matrix in so(3). 
    Works with both Sympy and Numpy matrices.
    '''   
    #create different datatype representations based on type of w
    if isinstance(w, list) or isinstance(w, np.ndarray) \
        or isinstance(w, np.matrix):
        f = np.array 
    elif isinstance(w, sym.Matrix): #NP and Sym
        f = sym.Matrix

    return f([
        [    0, -w[2],  w[1]],
        [ w[2],     0, -w[0]],
        [-w[1],  w[0],     0]
    ])

def UnhatMatrix3(w_hat):
    '''Turns a skew-symmetric matrix in so(3) into a vector in R3.
    '''
    if isinstance(w_hat, list) or isinstance(w_hat, np.ndarray) \
        or isinstance(w_hat, np.matrix):
        f = np.array
        w_hat = np.array(w_hat)
    elif isinstance(w_hat, sym.Matrix) or isinstance(w_hat, sym.ImmutableMatrix):
        f = sym.Matrix
    else:
        raise Exception(f"UnhatMatrix3: Unexpected type of w_hat: {type(w_hat)}")
    
    #matrix checking, for use in potential debug. generalized to both Sympy and Numpy
    same = np.array([w_hat + w_hat.T == f([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    ) ] )
    
#     if (not same.all()):
#         raise Exception("UnhatMatrix3: w_hat not skew_symmetric")
    
    #NP and Sym
    return f([
        -w_hat[1,2],
        w_hat[0,2],
        -w_hat[0,1],
    ])

def InvSEn(SEnmat):
    '''Takes the inverse of a SE(n) matrix.
    Compatible with Numpy, Sympy, and list formats.
    '''
    if isinstance(SEnmat, list):
        SEnmat = np.matrix(SEnmat)
    ###
    n = SEnmat.shape[0]
    R = SEnmat[:(n-1), :(n-1)]
    p = SEnmat[:(n-1),   n-1 ]
        
    return SOnAndRnToSEn(R.T, -R.T @ p)
    
def InertiaMatrix6(m, scriptI):
    '''Takes the mass and inertia matrix properties of an object in space,
    and constructs a 6x6 matrix corresponding to [[mI 0]; [0 scriptI]].
    Currently only written for Sympy matrix representations.
    '''
    if (m.is_Matrix or not scriptI.is_square):
        raise Exception("Type error: m or scriptI in InertiaMatrix6")
        
    mat = sym.zeros(6)
    mI = m * sym.eye(3)
    mat[:3, :3] = mI
    mat[3:6, 3:6] = scriptI
    return mat

def HatVector6(vec):
    '''Convert a 6-dimensional body velocity into a 4x4 "hatted" matrix,
    [[w_hat v]; [0 0]], where w_hat is skew-symmetric.
    w = 
    '''
    if isinstance(vec, np.matrix) or isinstance(vec, np.ndarray):
        vec = np.array(vec).flatten()
    
    v = vec[:3]
    w = vec[3:6]
    
    #this ensures if there are symbolic variables, they stay in Sympy form
    if isinstance(vec, sym.Matrix):
        v = sym.Matrix(v)
        w = sym.Matrix(w)
        
    w_hat = HatVector3(w)
    
    #note that the result isn't actually in SE(3) but 
    #that the function below creates a 4x4 matrix from a 3x3 and
    #1x3 matrix - with type checking - so we'll use it
    mat = SOnAndRnToSEn(w_hat, v)
    return mat

def UnhatMatrix4(mat):
    '''Convert a 4x4 "hatted" matrix,[[w_hat v]; [0 0]], into a 6-dimensional
    body velocity [v, w].
    '''
    #same as above - matrices aren't SE(3) and SO(3) but the function
    #can take in a 4x4 mat and return a 3x3 and 3x1 mat
    [w_hat, v] = SEnToSOnAndRn(mat)
    w = UnhatMatrix3(w_hat)
    
    if (isinstance(w, np.matrix) or isinstance(w, np.ndarray)):
        return np.array([v, w]).flatten()
    elif isinstance(w, sym.Matrix):
        return sym.Matrix([v, w])
    else:
        raise Exception("Unexpected datatype in UnhatMatrix4")
    
def CalculateVb6(G,t):
    '''Calculate the body velocity, a 6D vector [v, w], given a trans-
    formation matrix G from one frame to another.
    '''
    G_inv = InvSEn(G)
    Gdot = G.diff(t) #for sympy matrices, this also carries out chain rule 
    V_hat = G_inv @ Gdot 
    
#     if isinstance(G, sym.Matrix):
#         V_hat = sym.simplify(V_hat)
        
    return UnhatMatrix4(V_hat)

#-----------EULER-LAGRANGE AND IMPACTS-----------#

def compute_EL_lhs(lagrangian, q, t):
    '''
    Helper function for computing the Euler-Lagrange equations for a given system,
    so I don't have to keep writing it out over and over again.
    
    Inputs:
    - lagrangian: our Lagrangian function in symbolic (Sympy) form
    - q: our state vector [x1, x2, ...], in symbolic (Sympy) form
    
    Outputs:
    - eqn: the Euler-Lagrange equations in Sympy form
    '''
    
    # wrap system states into one vector (in SymPy would be Matrix)
    #q = sym.Matrix([x1, x2])
    qd = q.diff(t)
    qdd = qd.diff(t)

    # compute derivative wrt a vector, method 1
    # wrap the expression into a SymPy Matrix
    L_mat = sym.Matrix([lagrangian])
    dL_dq = L_mat.jacobian(q)
    dL_dqdot = L_mat.jacobian(qd)

    #set up the Euler-Lagrange equations
    #LHS = dL_dq - dL_dqdot.diff(t)
    LHS = dL_dqdot.diff(t) - dL_dq
    
    return LHS.T

def format_solns(soln):
    eqns_solved = []
    #eqns_new = []

    for i, sol in enumerate(soln):
        for x in list(sol.keys()):
            eqn_solved = sym.Eq(x, sol[x])
            eqns_solved.append(eqn_solved)

    return eqns_solved

def decompose_factors_dict(factors_dict):
    '''Take the dictionary of factors in the impact equations, and breaks
    them down further. This process can be repeated to get the factors only
    in terms of sines, cosines, numbers, and symbolic variables.
    
    Returns: new_factors_dict. Contains the same data as factors_dict
        in smaller terms.
    '''
    new_factors_array = np.array([])
    new_factors_dict = factors_dict.copy()

    for factor in factors_dict.keys():
        if factor.is_Add:
            #add components to list of factors and remove from old dictionary
            new_factors_array = np.append(new_factors_array, factor.as_ordered_terms())
            del new_factors_dict[factor]

        if factor.is_Pow:        
            new_factors_array = np.append(new_factors_array, list(factor.as_powers_dict().keys()))
            del new_factors_dict[factor]

        if factor.is_Mul:
            new_factors_array = np.append(new_factors_array, list(factor.as_coeff_mul()[-1]) )
            del new_factors_dict[factor]

    #fdo data checking and add terms back into the dictionary
    for factor in new_factors_array:
        if factor in new_factors_dict.keys():
            new_factors_dict[factor] += 1
        else:
            new_factors_dict[factor] = 1
            
    return new_factors_dict

#-----------DATA SAVING FUNCTIONS-----------#


def dill_dump(filename, data):
    dill.settings['recurse'] = True
    with open(filename, 'wb') as f:
        dill.dump(data, f)
        
def dill_load(filename):
    dill.settings['recurse'] = True
    with open(filename, 'rb') as f:
        data = dill.load(f)
    return data
