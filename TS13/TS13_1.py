import schemdraw as schem
import schemdraw.elements as e
import sympy as sp
from IPython.display import display, Latex

def paralelo(a, b):
    return (a*b)/(a+b)

s = sp.symbols("s", complex=True)

Z22 = (6*(s+2)*(s+6))/((s+4)*(s+1))

RL = 1
Z2 = sp.factor(sp.simplify(sp.expand(Z22 - 1)))
print('Remocion de RL\nSiendo:', end="")
display(Latex("$Z_2 = Z_{22} - K_\infty$"))
print("con ", end="")
display(Latex(f"$K_\infty=R_L={RL}\\rightarrow Z_2 = {sp.latex(Z2)}$"))

K1 = sp.limit(sp.expand(Z2*(s+1)), s, -1)
Z4 = sp.factor(sp.simplify(sp.expand( Z2 - ((K1)/(s+1)) )))
print('Remocion de tanque R3-C2\nSiendo:', end="")
display(Latex("$Z_4 = Z_2 - \\frac{K_1}{s+1}$"))
print("con ", end="")
display(Latex(f"$K_1={K1}\\rightarrow Z_4 = {sp.latex(Z4)}$"))

K2 = sp.limit(sp.expand(Z4*(s+4)), s, -4)
Z6 = sp.factor(sp.simplify(sp.expand( Z4 - ((K2)/(s+4)) )))
print('Remocion de tanque R2-C1\nSiendo:', end="")
display(Latex("$Z_6 = Z_4 - \\frac{K_2}{s+4}$"))
print("con ", end="")
display(Latex(f"$K_2={K2}\\rightarrow Z_6 = {sp.latex(Z6)}$"))

G1 = 1/Z6
print("Finalmente G1:", end="")
display(Latex(f"$G_1 = {G1}$"))

Ta = sp.Matrix([[1, 0],[G1, 1]])
Tb = sp.Matrix([[1, paralelo(K1, (K1/s)) + paralelo(1/(4/K2), K2/s) + RL],[0, 1]])
                             
TT = Ta * Tb

verif = sp.factor(sp.simplify(sp.expand(1/TT[1,1])))
print("Verificamos la transferencia:", end="")
display(Latex('$\\frac{-I_2}{I_1}= '+f'{sp.latex(verif)}$'))
#%%
d = schem.Drawing(unit=2.5)

It = d.add(e.SourceI(), d='up')
d.labelI(It, arrowlen=1.5, arrowofst=0.8, label='$I_1$')

d.add(e.LINE, d='right', l=2)
d.add(e.DOT)
d.push()
R1 = d.add(e.RES, d='down', label='$R_1$', botlabel=f'{1/G1}')
d.pop()

d.add(e.LINE, d='right', l=2)
d.add(e.DOT)
d.push()
d.add(e.LINE, d='up', l=1)
R2 = d.add(e.RES, d='right', label='$R_2$', botlabel=f'{1/(4/K2)}')
d.add(e.LINE, d='down', l=1)
d.pop()
d.add(e.LINE, d='down', l=1)
C1 = d.add(e.CAP, d='right', label='$C_1$', botlabel=f'{1/K2}')
d.add(e.LINE, d='up', l=1)
d.add(e.DOT)

d.add(e.LINE, d='right', l=1)
d.add(e.DOT)
d.push()
d.add(e.LINE, d='up', l=1)
R3 = d.add(e.RES, d='right', label='$R_3$', botlabel=f'{K1}')
d.add(e.LINE, d='down', l=1)
d.pop()
d.add(e.LINE, d='down', l=1)
C2 = d.add(e.CAP, d='right', label='$C_2$', botlabel=f'{1/K1}')
d.add(e.LINE, d='up', l=1)
d.add(e.DOT)

d.add(e.LINE, d='right', l=2)
RL = d.add(e.RES, d='down', label='$R_L$', botlabel=f'{RL}')
d.add(e.LINE, d='left', tox=R1.end)
d.add(e.DOT)
d.add(e.LINE, d='left', tox=It.end)

d.draw()
