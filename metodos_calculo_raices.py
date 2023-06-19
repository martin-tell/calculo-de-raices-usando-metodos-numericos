from numpy import abs

def biseccion(func, a, b, tol, no):
    solucion = []
    i = 1
    while i <= no:
        p = a + (b - a) / 2
        q = func(p)
        error = (b - a) / 2
        fa = func(a)
        fb = func(b)
        solucion.append([i, a, b, p, fa, fb, q, error])
        if q == 0 or error < tol:
            return True, solucion
        i += 1
        if fa * q > 0:
            a = p
        else:
            b = p
    return False, solucion


def newton_raphson(func, derv, p0, tol, no):
    solucion = []
    i = 1
    while i <= no:
        q = func(p0)
        d = derv(p0)
        p = p0 - q / d
        fp = func(p)
        error = abs(p - p0) / abs(p)
        solucion.append([i, p0, p, q, fp, error])
        if error < tol:
            return True, solucion
        i += 1
        p0 = p
    return False, solucion


def metodo_de_la_secante(func, p0, p1, tol, no):
    solucion = []
    i = 2
    q0 = func(p0)
    q1 = func(p1)
    while i <= no:
        p = p1 - q1 * (p1 - p0) / (q1 - q0)
        error = abs(p - p1) / abs(p)
        solucion.append([i, p0, p1, q0, q1, error])
        if error < tol:
            return True, solucion
        i += 1
        p0 = p1
        q0 = q1
        p1 = p
        q1 = func(p)
    return False, solucion


def regla_falsa(func, p0, p1, tol, no):
    solucion = []
    i = 2
    q0 = func(p0)
    q1 = func(p1)
    while i <= no:
        p = p1 - q1 * (p1 - p0) / (q1 - q0)
        error = abs(p - p1) / abs(p)
        solucion.append([i, p0, p1, q0, q1, error])
        if error < tol:
            return True, solucion
        i += 1
        q = func(p)
        if q * q1 < 0:
            p0 = p1
            q0 = q1
        p1 = p
        q1 = q
    return False, solucion