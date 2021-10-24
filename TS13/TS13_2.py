import schemdraw as schem
import schemdraw.elements as e
import sympy as sp
from IPython.display import display, Latex

def paralelo(a, b):
    return (a*b)/(a+b)

s = sp.symbols('s', complex=True)

Z22 = (2*(s**2 + (1/2)))/(s*((s**2) + 2))

C3 = sp.simplify(sp.expand(1/(Z22*s))).subs(s**2, -9)

Y2 = sp.factor(sp.simplify(sp.expand((1/Z22) - (C3*s))))
print('Remocion de C3\nSiendo:', end="")
display(Latex("$Y_2 = \\frac{1}{Z_{22}} - K_\infty s$"))
print("con ", end="")
display(Latex(f"$K_\infty={C3}\\rightarrow Y_2 = {sp.latex(Y2)}$"))

#IMPORTANTE! Sympy no me logra calcular K1 (nan), asi que lo impondre segun mis calculos
#K1 = sp.simplify(sp.expand((1/Y2)*(((s**2) + 9)/s))).subs(s**2, -9)

K1 = 289/27
Z4 = sp.factor(sp.simplify(sp.expand( (1/Y2) - ((K1*s)/((s**2) + 9)) )))
print('Remocion de tanque L1-C2\nSiendo:', end="")
display(Latex("$Z_4 = Z_2 - \\frac{K_1 s}{s^2 + 1}$"))
print("con ", end="")
display(Latex(f"$K_1={K1}\\rightarrow Z_4 = {sp.latex(Z4)}$"))

C1 = sp.simplify(sp.expand(1/(Z4*s))).subs(s**2, sp.oo)
print("Finalmente C1:", end="")
display(Latex(f"$C_1 = {C1}$"))

Ta = sp.Matrix([[1, 0],[C1*s, 1]])
Tb = sp.Matrix([[1, paralelo((K1/9)*s, (K1/s))],[0, 1]])
Tc = sp.Matrix([[1, 0],[s*C3 + 1, 1]])
                             
TT = Ta * Tb * Tc

verif = sp.factor(sp.simplify(sp.expand(1/TT[1,0])))
print("Verificamos la transferencia:", end="")
display(Latex('$\\frac{V_2}{I_1}= '+f'{sp.latex(verif)}$'))

print("Ahora desnormalizamos los componente por RL=9:")
Ta = sp.Matrix([[1, 0],[(3/17)*s, 1]])
Tb = sp.Matrix([[1, paralelo( 289*s/27, 1/(s*(3/289)) )],[0, 1]])
Tc = sp.Matrix([[1, 0],[(s*7/153) + (1/9), 1]])
                             
TT = Ta * Tb * Tc

verif = sp.factor(sp.simplify(sp.expand(1/TT[1,0])))
print("Verificamos la transferencia:", end="")
display(Latex('$\\frac{V_2}{I_1}= '+f'{sp.latex(verif)}$'))
#%%
d = schem.Drawing(unit=2.5)

It = d.add(e.SourceI(), d='up')
d.labelI(It, arrowlen=1.5, arrowofst=0.8, label='$I_1$')

d.add(e.LINE, d='right', l=2)
d.add(e.DOT)
d.push()
C1 = d.add(e.CAP, d='down', label='$C_1$', botlabel='$\\frac{3}{17}$')
d.pop()

d.add(e.LINE, d='right', l=2)
d.add(e.DOT)
d.push()
d.add(e.LINE, d='up', l=1)
L1 = d.add(e.INDUCTOR, d='right', label='$L_1$', botlabel='$\\frac{289}{243}$')
d.add(e.LINE, d='down', l=1)
d.pop()
d.add(e.LINE, d='down', l=1)
C2 = d.add(e.CAP, d='right', label='$C_2$', botlabel='$\\frac{3}{289}$')
d.add(e.LINE, d='up', l=1)
d.add(e.DOT)

d.add(e.LINE, d='right', l=2)
d.add(e.DOT)
d.push()
C3 = d.add(e.CAP, d='down', label='$C_3$', botlabel='$\\frac{7}{153}$')
d.pop()

d.add(e.LINE, d='right', l=2)
RL = d.add(e.RES, d='down', label='$R_L$', botlabel='9')
d.add(e.LINE, d='left', tox=C1.end)
d.add(e.DOT)
d.add(e.LINE, d='left', tox=It.end)

d.draw()
