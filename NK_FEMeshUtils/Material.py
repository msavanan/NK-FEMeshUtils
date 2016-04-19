class Material:
    MatID=0
    Rho=0.0
    E=0.0

    def __init__(self, MatID, Rho, E):
        self.MatID=MatID
        self.Rho=float(Rho)
        self.E=float(E)