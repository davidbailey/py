from sympy import *

Ra, Rrlf, Rrlr, Ff, Fr, W, Thetag, m, a, Rho, CD, Af, V, hpRa, frl, Rrl, hpRrl, Rg, G, Wf, Wr, h, lf, lr, L, F, Fmax, Mu = symbols('Ra Rrlf Rrlr Ff Fr W Thetag m a Rho CD Af V hpRa frl Rrl hpRrl Rg G Wf Wr h lf lr L')

# Equation 2.1
solve(-Ff -Fr +m*a +Ra +Rrlf +Rrlr +Rg, variable)

# Equation 2.2
solve(-F +m*a + Ra +Rrl +Rg, variable)

# Equation 2.3
solve(-Ra + Rational(1,2)*Rho*CD*Af*V**2, variable)

# Equation 2.4
solve(-hpRa + Rational(1,1100)*Rho*CD*Af*V**2, variable)

# Equation 2.5
solve(-frl + .01*(1+V/147), variable)

#Equation 2.6
solve(-Rrl + frl*W, variable)

#Equation 2.7
solve(-hpRrl + Rational(1,550)*frl*W*V, variable)

#Equation 2.8
solve(-Rg + W*sin(Thetag), variable)

#Equation 2.9
solve(-Rg + W*G, variable)

#Equation 2.10
solve(-Wr + (Ra*h + W*lf*cos(Thetag)+m*a*h+W*h*sin(Thetag))/L, variable)

#Equation 2.11
solve(-Wr +lf*W/L + h*(F-Rrl)/L, variable)

#Equation 2.12
solve(-Fmax + Mu*Wr, variable)
