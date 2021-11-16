import numpy as np
import sympy as sp
import schemdraw as schem
import schemdraw.elements as e
from IPython.display import display, Latex


def TZ(Z):
    return np.matrix([[1,Z],[0,1]])

def TY(Y):
    return np.matrix([[1,0],[Y,1]])

def Timg(gamma, Zi1, Zi2):
    return np.matrix([[np.cosh(gamma)*np.sqrt(Zi1/Zi2),np.sinh(gamma)*np.sqrt(Zi1*Zi2)],[np.sinh(gamma)/np.sqrt(Zi1*Zi2),np.cosh(gamma)*np.sqrt(Zi2/Zi1)]])

def alpha_n(alpha_db):
    return alpha_db/8.69

Z1, Z2= sp.symbols("Z1 Z2")

alpha_db = 30
Zi1 = Zi2 = Zo = 75

t_imagen = sp.Matrix(Timg(alpha_n(alpha_db), Zo, Zo))

display(Latex("Parametros T para "+ f"$\\alpha = {alpha_db}d_B$"))
display(Latex(f'$T_i=$'), sp.simplify(t_imagen))

t_z = sp.Matrix(np.dot(np.dot(TZ(Z1/2), TY(1/Z2)), TZ(Z1/2)))
t_z = sp.simplify(t_z)
display(Latex("Parametros T por impedancias:"))
display(Latex(f'$T_z=$'), t_z)

display(Latex("Igualando matrices:"))
display(sp.Eq(t_z, t_imagen))
display(sp.Eq(t_z - t_imagen, sp.Matrix([[0,0],[0,0]])))

Zs, = sp.nonlinsolve(t_z - t_imagen, Z1, Z2)
display(Latex("Resolviendo este sistema de ecuaciones:"))
display(Latex(f"$Z_1 = {Zs[0]}$"))
display(Latex(f"$Z_2 = {Zs[1]}$"))

t_z = (t_z.subs(Z1, Zs[0])).subs(Z2,Zs[1])
display(Latex("Reemplazando estos valores en $T_z:$"))
display(Latex(f'$T_z=$'), t_z)

# Construccion de esquematico

d = schem.Drawing(unit=2.5)
Zg = d.add(e.RES, d='right', label='$R_g$', botlabel='75') 
Z1_e = d.add(e.RES, d='right', label='$\\frac{Z_1}{2}$', botlabel=f'{round(float(Zs[0]/2),3)}')
d.add(e.DOT)
d.push()
Z2_e = d.add(e.RES, d='down', label='$Z_2$', botlabel=f'{round(float(Zs[1]),3)}')
d.pop()
Z1_e2 = d.add(e.RES, d='right', label='$\\frac{Z_1}{2}$', botlabel=f'{round(float(Zs[0]/2),3)}')
d.add(e.LINE, d='right', tox=Z2_e.end)
ZL = d.add(e.RES, d='down', label='$R_L$', botlabel='75')
d.add(e.LINE, d='left', tox=Z2_e.end)
d.add(e.DOT)
d.add(e.LINE, d='left', tox=Zg.start)
Vt = d.add(e.SourceSin(), xy=Zg.start, toy=Z1_e2.end, lblofst=0.3)
d.labelI(Vt, arrowlen=1.5, arrowofst=0.8, label='$V_t$')
d.draw()