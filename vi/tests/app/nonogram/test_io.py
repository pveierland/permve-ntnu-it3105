from vi.grid import Coordinate
from vi.app.nonogram import build_domain

def test_build_domain_1():
    spec   = [2, 1, 3]
    domain = build_domain(10, spec)

    assert len(domain) == 10

    assert (True,  True,  False, True,  False, True,  True,  True,  False, False) in domain
    assert (True,  True,  False, True,  False, False, True,  True,  True,  False) in domain
    assert (True,  True,  False, False, True,  False, True,  True,  True,  False) in domain
    assert (False, True,  True,  False, True,  False, True,  True,  True,  False) in domain
    assert (True,  True,  False, True,  False, False, False, True,  True,  True ) in domain
    assert (True,  True,  False, False, True,  False, False, True,  True,  True ) in domain
    assert (False, True,  True,  False, True,  False, False, True,  True,  True ) in domain
    assert (True,  True,  False, False, False, True,  False, True,  True,  True ) in domain
    assert (False, True,  True,  False, False, True,  False, True,  True,  True ) in domain
    assert (False, False, True,  True,  False, True,  False, True,  True,  True ) in domain

def test_build_domain_2():
    spec   = [3, 4]
    domain = build_domain(10, spec)

    assert len(domain) == 6

    assert (True,  True,  True,  False, True,  True,  True,  True,  False, False) in domain
    assert (True,  True,  True,  False, False, True,  True,  True,  True,  False) in domain
    assert (True,  True,  True,  False, False, False, True,  True,  True,  True ) in domain
    assert (False, True,  True,  True,  False, True,  True,  True,  True,  False) in domain
    assert (False, True,  True,  True,  False, False, True,  True,  True,  True ) in domain
    assert (False, False, True,  True,  True,  False, True,  True,  True,  True ) in domain
