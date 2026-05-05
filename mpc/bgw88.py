# Can always call the field order, and reduce modulo that.

import galois
import numpy as np
import random

class BGW:
    def __init__(self, n, t, q, xis, alpha):
        self.field= galois.GF(q)
        self.nparties= n
        self.threshold= t
        self.players= [Player(j, xis[j]) for j in range(n)]
        r_alphas= [alpha**i % q for i in range(n)]

	# Shamir secret share of the value @x among the players
    # via the polynomial with coefficients @coefs, which can be requested
    # from one of the @self.players
	def shamir_ss(self,x,coefs):
        poly= galois.Poly(coefs+[x], field=self.field)
        gf= lambda y: self.field(y)
        gf_sshare= [poly(gf(a)) for a in self.r_alphas]
        sshare= gf_sshare.tolist()
        n= self.nparties
        for j in range(n):
            player= self.players[j]
            player.secret_share= sshare[j]
        

class Player:
    def __init__(self, i, xi):
        self.id= i
        self.poly_coefs= None
        self.secret_share= xi #Initially the player holds its input

    # Random polynomial coefficients for Shamir secret-sharing.
    def random_polynomial(self, t, q):
        cs= [a for a in range(q)]
        self.poly_coefs= random.choices(cs, k=t)

# Operations modulo 7
alphas= [1,3,2,6,4]

B= [[a**k % 7 for a in alphas] for k in range(5)]

for k in range(5):
    print(B[k])

F7= galois.GF(7)
points= F7(alphas)

xs= [4,5,2,2,3]
shamir_ss(xs)
