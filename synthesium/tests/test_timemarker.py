from synthesium.mation.timestamp import TimeStamp

def test(): 
    test_comparisons()

def test_comparisons():
    less = TimeStamp(1, 3, 2)
    more = TimeStamp(2, 2, 4)
    base = TimeStamp(2, 0, 1)

    assert less < base 
    assert more > base
    assert base == base
    assert less <= base
    assert more >= base
    assert not base > base
    assert not base <= less

test_comparisons()