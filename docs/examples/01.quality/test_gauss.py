#!/usr/bin/env -S python3

from unicodedata import name
import pytest

N=100
SMALL = 1e-5

@pytest.fixture(scope='module', name='solver_function')
def import_solver_funciton():
    import impl_gauss as ig
    if 'vgauss' in ig.__dict__:
        return ig.vgauss
    elif 'vector_gauss' in ig.__dict__:
        return ig.vector_gauss
    elif 'gauss' in ig.__dict__:
        return ig.gauss
    else:
        assert False, "No (v)gauss function(s)"

@pytest.mark.parametrize('n,small', [(N,SMALL)])
def test_sane_error(solver_function, n, small):
    from numpy.linalg import norm, det
    from numpy.linalg import solve as solve_out_of_the_box
    from numpy.random import uniform

    # Сгенерируем хорошо обусловленную систему
    while True:
        a = uniform(0.0, 1.0, (n, n))
        b = uniform(0.0, 1.0, (n,  ))

        d = det(a)
        if abs(d) <= small:  # Определитель маленький — плохо
            # print(f"det: {d}")
            continue  # Попробуем ещё
        if d < 0.0:  # Отрицательный — поменяем знак
            # print(f"det: {d}")
            a = -a

        try:
            oob_solution = solve_out_of_the_box(a, b)
        except Exception as e:  # Всё-таки система плохая
            # print(f"exc: {e}")
            continue  # Попробуем ещё

        sb = a @ oob_solution
        if norm(sb - b, ord=1) > small:
            # print("Bad solution...")
            continue  # Всё же не очень система получилась =)

        break # Всё, считаем, что мы случайно сгенерировали хорошую систему

    tested_solution = solver_function(a, b)
    e = norm(tested_solution - oob_solution, ord=1)
    assert e <= small, f"Error is too big: {e}"
