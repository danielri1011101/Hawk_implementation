# Can always call the field order, and reduce modulo that.

import galois
import numpy as np
import random

class BGW:
    def __init__(self, n, t, q, xis):
        self.field= galois.GF(q)
        self.nparties= n
        self.threshold= t
        self.players= [Player(j, xis[j], self) for j in range(n)]
        E= self.field
        alph= E.primitive_element
        alphas= [alph ** j for j in range(n)]
        self.alphas= alphas

	# Shamir secret share of the value @x among the players
        # via the polynomial with coefficients @coefs, which can be requested
        # from one of the @self.players
	def shamir_ss(self,x,coefs):
            poly= galois.Poly(coefs+[x], field=self.field)
            gf_sshare= poly(self.alphas)
            sshare= gf_sshare.tolist()
            n= self.nparties
            for j in range(n):
                player= self.players[j]
                player.secret_share= sshare[j]
            

class Player:
    def __init__(self, i, xi, bgw):
        self.id= i
        self.secret_share= xi #Initially the player holds its input
        self.bgw= bgw
        self.poly_coefs= None

    def random_polynomial(self):
        E= self.bgw.field
        q= E.order
        t= self.bgw.threshold
        coefs= random.choices([j for j in range(q)], k=t)
        self.poly_coefs= coefs

    # Random polynomial coefficients for Shamir secret-sharing.

# Operations modulo 7
xs= [4,5,2,2,3]
# Circuit (+ (* (* x0 x1) x2) (+ x3 x4))
