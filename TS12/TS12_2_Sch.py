import sympy as sp

def paralelo(a, b):
    return (a*b)/(a+b)

s = sp.symbols('s', complex=True)

Z11 = ((s+2)*(s*4))/((s+3)*(s+1))

K1 = sp.limit( Z11*(s+1), s, -1)

Z2 = sp.factor(sp.simplify(sp.expand( Z11 - (K1/(s+1) ))))

R2 = sp.limit(Z2, s, sp.oo)

Z4 = sp.factor(sp.simplify(sp.expand( Z2 - R2 )))

C2 = sp.limit(Y4/s, s, sp.oo)

Y6 = sp.factor(sp.simplify(sp.expand( Y4 - (C2*s) )))

R3 = 1/Y6

Ta = sp.Matrix([[1, paralelo()],[0, 1]])
Tb = sp.Matrix([[1, 0],[paralelo(s*K1, 1/((1/K1)*s)), 1]])
Tc = sp.Matrix([[1, 1/(s*(1/C3)) + (s*L2)],[0, 1]])

TT = Ta * Tb * Tc

verif = sp.factor(sp.simplify(sp.expand(1/TT[1,1])))

display(verif)
#%%
import schemdraw as schem
import schemdraw.elements as e
d = schem.Drawing(unit=2.5)
Linit = d.add(e.LINE, d='right')
d.add(e.DOT)
d.push()
d.add(e.LINE, d='up', l=0.5)
C1 = d.add(e.CAP, d='right', label='$C_1$')
d.add(e.LINE, d='down', l=0.5)
d.pop()
d.add(e.LINE, d='down', l=0.5)
R1 = d.add(e.RES, d='right', botlabel='$R_1$')
d.add(e.LINE, d='up', l=0.5)
d.add(e.DOT)
R2 = d.add(e.RES, d='right', botlabel='$R_2$')
d.add(e.DOT)
d.push()
C2 = d.add(e.CAP, d='down', botlabel='$C_2$')
d.pop()
d.add(e.LINE, d='right', l=2)
R3 = d.add(e.RES, d='down', botlabel='$R_3$')
d.add(e.LINE, d='left', tox=C2.end)
d.add(e.DOT)
d.add(e.LINE, d='left', tox=Linit.start)
Vt = d.add(e.SourceSin(), xy=Linit.start, lblofst=0.3)
d.labelI(Vt, arrowlen=1.5, arrowofst=0.8, label='$V_t$')
d.draw()
d.save('7_resistors_3_loops.png')