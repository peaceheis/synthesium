from synthesium.mation.timemarker import TimeMarker

def test(): 
    test_comparisons()

def test_comparisons():
    less = TimeMarker(1, 3, 2)
    more = TimeMarker(2, 2, 4)
    base = TimeMarker(2, 0, 1)

    assert less < base 
    assert more > base
    assert base == base
    assert less <= base
    assert more >= base
    assert not base > base
    assert not base <= less

test_comparisons()