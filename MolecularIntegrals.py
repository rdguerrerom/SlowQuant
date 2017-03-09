import math
import numpy as np
import scipy.misc as scm
import scipy.special as scs
from numba import jit

##INTEGRAL FUNCTIONS
def Overlap(a, b, la, lb, Ax, Bx):
    #Obara-Saika scheme, 9.3.8 and 9.3.9 Helgaker
    #No normalization constants - corrected down in call of the function
    p = a + b
    u = a*b/p
    
    Px = (a*Ax+b*Bx)/p
    
    S00 = (math.pi/p)**(1/2) * math.exp(-u*(Ax-Bx)**2)
    
    Sij = np.zeros(shape=(la+2,lb+2))
    Sij[0,0] = S00
    
    
    for i in range(0, la+1):
        for j in range(0, lb+1):
            Sij[i+1,j] = (Px-Ax)*Sij[i,j] + 1/(2*p) * (i*Sij[i-1,j] + j*Sij[i,j-1])
            Sij[i,j+1] = (Px-Bx)*Sij[i,j] + 1/(2*p) * (i*Sij[i-1,j] + j*Sij[i,j-1])
    
    return Sij[la,lb]

def Kin_NOTTESTED(a, b, la, lb, Ax, Bx):
    #Obara-Saika scheme, 9.3.40 and 9.3.41 Helgaker
    Px = (a*Ax+b*Bx)/p
    XPA = Px - Ax
    XPB = Px - Bx
    
    Tij = np.zeros(shape=(la+2,lb+2))
    S = Overlap(a, b, la, lb, Ax, Bx)
    Tij[0,0] = [a-2*a**2*(XPA**2+1/(2*p))]*S[0,0]
    
    for i in range(0, la+1):
        for j in range(0, lb+1):
            Tij[i+1,j] = XPA*T[i,j] + 1/(2*p)*(i*T[i-1,j]+j*T[i,j-1]) + b/p*(2*a*S[i+1,j] - i*S[i-1,j])
            Tij[i,j+1] = XPB*T[i,j] + 1/(2*p)*(i*T[i-1,j]+j*T[i,j-1]) + a/p*(2*b*S[i,j+1] - i*S[i,j-1])
    
    return Tij[la, lb]

def Kin(a1, a2, Ax, Ay, Az, Bx, By, Bz, la, lb, ma, mb, na, nb, N1, N2, c1, c2):
    #Where is this from?
    N = N1*N2*c1*c2
    g = a1 + a2
    
    Px = (a1*Ax+a2*Bx)/g
    Py = (a1*Ay+a2*By)/g
    Pz = (a1*Az+a2*Bz)/g
    
    Ix = I(la, lb, (Px-Ax), (Px-Bx), g)
    Iy = I(ma, mb, (Py-Ay), (Py-By), g)
    Iz = I(na, nb, (Pz-Az), (Pz-Bz), g)
    S = math.exp(-a1*a2*((Ax-Bx)**2+(Ay-By)**2+(Az-Bz)**2)/g)
    
    
    Ixk = a2*(2*lb+1)*S*Ix*Iy*Iz - 2*a2**2*S*I(la, lb+2, (Px-Ax), (Px-Bx), g)*Iy*Iz - ((lb*(lb-1))/(2))*S*I(la, lb-2, (Px-Ax), (Px-Bx), g)*Iy*Iz
    Iyk = a2*(2*mb+1)*S*Ix*Iy*Iz - 2*a2**2*S*I(ma, mb+2, (Py-Ay), (Py-By), g)*Ix*Iz - ((mb*(mb-1))/(2))*S*I(ma, mb-2, (Py-Ay), (Py-By), g)*Ix*Iz
    Izk = a2*(2*nb+1)*S*Ix*Iy*Iz - 2*a2**2*S*I(na, nb+2, (Pz-Az), (Pz-Bz), g)*Ix*Iy - ((nb*(nb-1))/(2))*S*I(na, nb-2, (Pz-Az), (Pz-Bz), g)*Ix*Iy
    
    T = N*(Ixk + Iyk + Izk)
    
    return T

def elnuc(a1, a2, Ax, Ay, Az, Bx, By, Bz, l1, l2, m1, m2, n1, n2, N1, N2, c1, c2, input):
    #SUPER UGLY
    N = N1*N2*c1*c2
    gp = a1 + a2
    ep = (a1*a2)/gp
    
    Px = (a1*Ax+a2*Bx)/gp
    Py = (a1*Ay+a2*By)/gp
    Pz = (a1*Az+a2*Bz)/gp
    
    Fzeta = 0
    for C in range(1, len(input)):
        Zc = input[C][0]
        rcx = input[C][1]
        rcy = input[C][2]
        rcz = input[C][3]
        
        for i1 in range(0, int(l1/2)+1):
            for i2 in range(0, int(l2/2)+1):
                for o1 in range(0, l1-2*i1+1):
                    for o2 in range(0,l2-2*i2+1):
                        for r in range(0, int((o1+o2)/2)+1):
                            ux = l1+l2-2*(i1+i2)-(o1+o2)
                            for u in range(0, int(ux/2)+1):
                                for j1 in range(0, int(m1/2)+1):
                                    for j2 in range(0, int(m2/2)+1):
                                        for p1 in range(0, m1-2*j1+1):
                                            for p2 in range(0, m2-2*j2+1):
                                                for s in range(0, int((p1+p2)/2)+1):
                                                    uy = m1+m2-2*(j1+j2)-(p1+p2)
                                                    for v in range(0, int(uy/2)+1):
                                                        for k1 in range(0, int(n1/2)+1):
                                                            for k2 in range(0, int(n2/2)+1):
                                                                for q1 in range(0, n1-2*k1+1):
                                                                    for q2 in range(0, n2-2*k2+1):
                                                                        for t in range(0, int((q1+q2)/2)+1):
                                                                            uz = n1+n2-2*(k1+k2)-(q1+q2)
                                                                            for w in range(0, int(uz/2)+1):

                                                                                Fzeta += A(l1, l2, a1, a2, Ax, Bx, Px, rcx, i1, i2, o1, o2, r, u)*A(m1, m2, a1, a2, Ay, By, Py, rcy, j1, j2, p1, p2, s, v)*A(n1, n2, a1, a2, Az, Bz, Pz, rcz, k1, k2, q1, q2, t, w)*2*F(gp*((Px-rcx)**2+(Py-rcy)**2+(Pz-rcz)**2), ux+uy+uz-(u+v+w)) * Zc
            
    Vn = -N*math.pi/gp * math.exp(-ep*((Ax-Bx)**2+(Ay-By)**2+(Az-Bz)**2)) * Fzeta

    return Vn

def elelrep(a1, a2, a3, a4, Ax, Ay, Az, Bx, By, Bz, Cx, Cy, Cz, Dx, Dy, Dz, la, lb, lc, ld, ma, mb, mc, md, na, nb, nc, nd, N1, N2, N3, N4, c1, c2, c3, c4):
    #SUPER UGLY
    N = N1*N2*N3*N4*c1*c2*c3*c4
    
    gp = a1 + a2
    gq = a3 + a4
    
    Px = (a1*Ax+a2*Bx)/gp
    Py = (a1*Ay+a2*By)/gp
    Pz = (a1*Az+a2*Bz)/gp
    
    Qx = (a3*Cx+a4*Dx)/gq
    Qy = (a3*Cy+a4*Dy)/gq
    Qz = (a3*Cz+a4*Dz)/gq
    
    K1 = math.exp(-a1*a2*((Ax-Bx)**2 +(Ay-By)**2 +(Az-Bz)**2)/gp)
    K2 = math.exp(-a3*a4*((Cx-Dx)**2 +(Cy-Dy)**2 +(Cz-Dz)**2)/gq)
    
    Fzeta = 0

    for lp in range(0, la+lb+1):
        for lq in range(0, lc+ld+1):
            for u1 in range(0, int(lp/2) +1):
                for u2 in range(0, int(lq/2) +1):
                    for tp in range(0, int((lp+lq-2*u1-2*u2)/2) +1):
                        for mp in range(0, ma+mb+1):
                            for mq in range(0, mc+md+1):
                                for v1 in range(0, int(mp/2) +1):
                                    for v2 in range(0, int(mq/2) +1):
                                        for tpp in range(0, int((mp+mq-2*v1-2*v2)/2) +1):
                                            for np in range(0, na+nb+1):
                                                for nq in range(0, nc+nd+1):
                                                    for om1 in range(0, int(np/2) +1):
                                                        for om2 in range(0, int(nq/2) +1):
                                                            for tppp in range(0, int((np+nq-2*om1-2*om2)/2) +1):
                                                                Fzeta += F(((((Px-Qx)**2+(Py-Qy)**2+(Pz-Qz)**2)*gp*gq)/(gp+gq)),(lp+lq+np+nq+mp+mq-2*u1-2*u2-2*v1-2*v2-2*om1-2*om2-tp-tpp-tppp)) * G(lp, lq, u1, u2, tp, gp, gq, la, lb, (Px-Ax), (Px-Bx), lc, ld, (Qx-Cx), (Qx-Dx), (Px-Qx)) * G(mp, mq, v1, v2, tpp, gp, gq, ma, mb, (Py-Ay), (Py-By), mc, md, (Qy-Cy), (Qy-Dy), (Py-Qy)) * G(np, nq, om1, om2, tppp, gp, gq, na, nb, (Pz-Az), (Pz-Bz), nc, nd, (Qz-Cz), (Qz-Dz), (Pz-Qz))

    
    V = N*((2*math.pi**(5/2)*K1*K2)/(gp*gq*math.sqrt(gp+gq)))*Fzeta

    return V


def nucrep(input):
    #Classical nucleus nucleus repulsion
    Vnn = 0
    for i in range(1, len(input)):
        for j in range(1, len(input)):
            if i < j:
                Vnn += (input[i][0]*input[j][0])/(math.sqrt((input[i][1]-input[j][1])**2+(input[i][2]-input[j][2])**2+(input[i][3]-input[j][3])**2))
    return Vnn

##UTILITY FUNCTIONS
def f(l1, l2, PAc, PBc, k):
    f = 0
    for q in range(max(-k, k-2*l2), min(k, 2*l1-k)+1, 2):
        f += math.factorial(l1)/(math.factorial((k+q)/(2))*math.factorial(l1-(k+q)/(2)))*math.factorial(l2)/(math.factorial((k-q)/(2))*math.factorial(l2-(k-q)/(2)))*PAc**(l1-(k+q)/(2))*PBc**(l2-(k-q)/(2))
    return f

def F(u, v):
    # Return wrong values at T very close at zero, why u is defined to be nearly 0
    if u >= 0 and u < 0.0000001:
        F = 1/(2*v+1)
    else:
        part1 = math.sqrt(math.pi)/(4**v * u**(v+1/2)) * math.erf(math.sqrt(u))
        part2 = 0 
        for k in range(0, v):
            part2 += math.factorial(v-k)/(4**k * math.factorial(2*v-2*k)*u**(k+1))
        F = math.factorial(2*v)/(2*math.factorial(v)) * (part1 - math.exp(-u)*part2)
    return F


def G(lp, lq, u1, u2, tp, gp, gq, la, lb, PAx, PBx, lc, ld, QCx, QDx, PQx):
    part1 = (-1)**(lp+tp) * f(la, lb, PAx, PBx, lp)*f(lc, ld, QCx, QDx, lq)
    part2 = PQx**(lp+lq-2*u1-2*u2-2*tp) * ((gp*gq)/(gp+gq))**(lp+lq-2*u1-2*u2-tp)
    part3 = gp**(u1-lp) * gq**(u2-lq) * math.factorial(lp) * math.factorial(lq) * math.factorial(lp+lq-2*u1-2*u2) * 4**(-u1-u2-tp)
    part4 = math.factorial(u1) * math.factorial(u2) * math.factorial(lp-2*u1) * math.factorial(lq-2*u2) * math.factorial(lp+lq-2*u1-2*u2-2*tp) * math.factorial(tp)
    G = part1*part2*(part3/part4)
    return G

def I(l1, l2, PAc, PBc, g):
    I = 0
    for i in range(0, (int((l1+l2)/2) +1)):
        I += f(l1, l2, PAc, PBc, 2*i) * (scm.factorial2(2*i-1)/(2*g)**i)*math.sqrt(math.pi/g)
    return I

def A(l1, l2, a1, a2, Ax, Bx, Px, rcx, i1, i2, o1, o2, r, u):
    gp = a1 + a2
    A = 0
    uc = l1 + l2 - 2*(i1+i2)-(o1+o2)
    part1 = (-1)**(l1+l2)*math.factorial(l1)*math.factorial(l2)
    part2 = (-1)**(o2+r)*math.factorial(o1+o2)
    part3 = 4**(i1+i2+r)*math.factorial(i1)*math.factorial(i2)*math.factorial(o1)*math.factorial(o2)*math.factorial(r)
    part4 = a1**(o2-i1-r)*a2**(o1-i2-r)*(Ax-Bx)**(o1+o2-2*r)
    part5 = math.factorial(l1-2*i1-o1)*math.factorial(l2-2*i2-o2)*math.factorial(o1+o2-2*r)
    part6 = (-1)**(u)*math.factorial(uc)*(Px-rcx)**(uc-2*u)
    part7 = 4**u*math.factorial(u)*math.factorial(uc-2*u)*gp**(o1+o2-r+u)
    A = part1*((part2)/(part3))*((part4)/(part5))*((part6)/(part7))
    return A

##CALC OF INTEGRALS
def runIntegrals(input, basis):
    # Set up indexes for integrals
    See = {}
    for i in range(1, len(basis)+1):
        for j in range(1, len(basis)+1):
            if i >= j:
                See[str(int(i))+';'+str(int(j))] = 0
    
    Vee = {}
    for i in range(1, len(basis)+1):
        for j in range(1, len(basis)+1):
            for k in range(1, len(basis)+1):
                for l in range(1, len(basis)+1):
                    if i>=j and i>=k and i>=l and k>=l:
                        if i == k or i == l:
                            if i*j >= k*l:
                                Vee[str(int(i))+';'+str(int(j))+';'+str(int(k))+';'+str(int(l))] = 0
                        else:
                            Vee[str(int(i))+';'+str(int(j))+';'+str(int(k))+';'+str(int(l))] = 0
    #END OF set up indexes for integrals
    
    # Nuclear-nuclear repulsion
    output = open('enuc.txt', 'w')
    calc = nucrep(input)
    output.write(str(calc))
    output.close()
    #END OF nuclear-nuclear repulsion
    
    # Two electron integrals
    output = open('twoint.txt', 'w')
    for key in Vee.keys():
        a = key.split(";")
        for i in range(len(a)):
            a[i] = int(a[i])-1
        calc = 0
        for i in range(basis[a[0]][4]):
            for j in range(basis[a[1]][4]):
                for k in range(basis[a[2]][4]):
                    for l in range(basis[a[3]][4]):
                        calc += elelrep(basis[a[0]][5][i][1], basis[a[1]][5][j][1], basis[a[2]][5][k][1], basis[a[3]][5][l][1], basis[a[0]][1], basis[a[0]][2], basis[a[0]][3], basis[a[1]][1], basis[a[1]][2], basis[a[1]][3], basis[a[2]][1], basis[a[2]][2], basis[a[2]][3], basis[a[3]][1], basis[a[3]][2], basis[a[3]][3], basis[a[0]][5][i][3], basis[a[1]][5][j][3], basis[a[2]][5][k][3], basis[a[3]][5][l][3], basis[a[0]][5][i][4], basis[a[1]][5][j][4], basis[a[2]][5][k][4], basis[a[3]][5][l][4], basis[a[0]][5][i][5], basis[a[1]][5][j][5], basis[a[2]][5][k][5], basis[a[3]][5][l][5], basis[a[0]][5][i][0], basis[a[1]][5][j][0], basis[a[2]][5][k][0], basis[a[3]][5][l][0], basis[a[0]][5][i][2], basis[a[1]][5][j][2], basis[a[2]][5][k][2], basis[a[3]][5][l][2])
        output.write(key)
        output.write(";")
        output.write(str(calc))
        output.write("\n")
    output.close()
    #END OF two electron integrals
    
    # Overlap
    output = open('overlap.txt', 'w')
    for key in See.keys():
        a = key.split(";")
        for i in range(len(a)):
            a[i] = int(a[i])-1
        calc = 0
        for i in range(basis[a[0]][4]):
            for j in range(basis[a[1]][4]):
                # Normalization multiplied here and not in the function!
                calc += Overlap(basis[a[0]][5][i][1], basis[a[1]][5][j][1], basis[a[0]][5][i][3], basis[a[1]][5][j][3], basis[a[0]][1], basis[a[1]][1])*Overlap(basis[a[0]][5][i][1], basis[a[1]][5][j][1], basis[a[0]][5][i][4], basis[a[1]][5][j][4], basis[a[0]][2], basis[a[1]][2])*Overlap(basis[a[0]][5][i][1], basis[a[1]][5][j][1], basis[a[0]][5][i][5], basis[a[1]][5][j][5], basis[a[0]][3], basis[a[1]][3])*basis[a[0]][5][i][0]*basis[a[0]][5][i][2]*basis[a[1]][5][j][0]*basis[a[1]][5][j][2]
        output.write(key)
        output.write(";")
        output.write(str(calc))
        output.write("\n")
    output.close()
    #END OF overlap
    
    # Kinetic energy
    output = open('kinen.txt', 'w')
    for key in See.keys():
        a = key.split(";")
        for i in range(len(a)):
            a[i] = int(a[i])-1
        calc = 0
        for i in range(basis[a[0]][4]):
            for j in range(basis[a[1]][4]):
                calc += Kin(basis[a[0]][5][i][1], basis[a[1]][5][j][1], basis[a[0]][1], basis[a[0]][2], basis[a[0]][3], basis[a[1]][1], basis[a[1]][2], basis[a[1]][3], basis[a[0]][5][i][3], basis[a[1]][5][j][3], basis[a[0]][5][i][4], basis[a[1]][5][j][4],basis[a[0]][5][i][5], basis[a[1]][5][j][5], basis[a[0]][5][i][0], basis[a[1]][5][j][0], basis[a[0]][5][i][2], basis[a[1]][5][j][2])
        output.write(key)
        output.write(";")
        output.write(str(calc))
        output.write("\n")
    output.close()
    #END OF kinetic energy
    
    # Nucleus electron attraction
    output = open('nucatt.txt', 'w')
    for key in See.keys():
        a = key.split(";")
        for i in range(len(a)):
            a[i] = int(a[i])-1
        calc = 0
        for i in range(basis[a[0]][4]):
            for j in range(basis[a[1]][4]):
                calc += elnuc(basis[a[0]][5][i][1], basis[a[1]][5][j][1], basis[a[0]][1], basis[a[0]][2], basis[a[0]][3], basis[a[1]][1], basis[a[1]][2], basis[a[1]][3], basis[a[0]][5][i][3], basis[a[1]][5][j][3], basis[a[0]][5][i][4], basis[a[1]][5][j][4],basis[a[0]][5][i][5], basis[a[1]][5][j][5], basis[a[0]][5][i][0], basis[a[1]][5][j][0], basis[a[0]][5][i][2], basis[a[1]][5][j][2], input)
        output.write(key)
        output.write(";")
        output.write(str(calc))
        output.write("\n")
    
    output.close()
    #END OF nucleus electron attraction
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    