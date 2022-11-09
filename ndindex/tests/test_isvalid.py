from pytest import raises, fail

from hypothesis import given

from numpy import arange, prod

from ..ndindex import ndindex
from .helpers import ndindices, shapes

@given(ndindices, shapes)
def test_isvalid_hypothesis(idx, shape):
    index = ndindex(idx)

    if isinstance(shape, int):
        a = arange(shape)
    else:
        a = arange(prod(shape)).reshape(shape)

    valid = index.isvalid(shape)

    if valid:
        a[idx] # doesn't raise
    else:
        with raises(IndexError):
            try:
                a[idx]
            except Warning as w:
                if "Out of bound index found. This was previously ignored when the indexing result contained no elements. In the future the index error will be raised. This error occurs either due to an empty slice, or if an array has zero elements even before indexing." in w.args[0]:
                    raise IndexError
                else: # pragma: no cover
                    fail(f"Unexpected warning raised: {w}")
