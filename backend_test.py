import backend

assert backend.main('@x((-Ax+Dx) > (-(-Bx * Cx)))') == False
assert backend.main('@x@y(-Bx*(Cx*Dx))') == False
assert backend.main('@x(Ax>(Ax*Bx))') == False
assert backend.main('@x(Ax>(Ax+Bx))') == True
assert backend.main('@x!y((x=y))') == True
assert backend.main('!y@x(Fy>Fx)') == True
assert backend.main('@xAx') == False
assert backend.main('@x((Ax>Bx))') == False
assert backend.main('@x!t((Ax>Bx))') == False
assert backend.main('@x!t(Ax>Bx)') == False
assert backend.main('@x!d(Px+-Pd)') == True
assert backend.main('@x@y(Px>(Px*Py))') == False