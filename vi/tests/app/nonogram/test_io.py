from vi.grid import Coordinate
from vi.app.nonogram import build_domain, reduce_domain

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

def test_reduce_domains():
    spec_a   = [2, 1, 3]
    domain_a = build_domain(10, spec_a)

    spec_b   = [3, 4]
    domain_b = build_domain(10, spec_b)

    domain_a, domain_b = reduce_domain(domain_a, domain_b, 6, 2)

    assert len(domain_a) == 4

    assert (True,  True,  False, True,  False, True,  True,  True,  False, False) in domain_a
    assert (True,  True,  False, True,  False, False, True,  True,  True,  False) in domain_a
    assert (True,  True,  False, False, True,  False, True,  True,  True,  False) in domain_a
    assert (False, True,  True,  False, True,  False, True,  True,  True,  False) in domain_a
