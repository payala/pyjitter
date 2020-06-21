import pytest
import sys
import gc
import weakref
from pyjitter.connection import Connection
from pyjitter.signal import Signal, Edge
from utils import create_basic_signal


def test_calculate_edges():
    sig_in = create_basic_signal()
    sig_out = Signal()

    con = Connection(sig_in, sig_out, 22e-9, 5e-9)

    edges = list(sig_out.edges)

    assert len(edges) == 3

    assert edges[0].time == 10e-9 + 22e-9
    assert edges[0].end_level == sig_in.edges[0].end_level
    assert edges[0].trans_time == sig_out.rise_time
    assert edges[0].uncertainty == 2e-9 + 5e-9

    assert edges[1].time == 20e-9 + 22e-9
    assert edges[1].end_level == sig_in.edges[1].end_level
    assert edges[1].trans_time == sig_out.rise_time
    assert edges[1].uncertainty == 3e-9 + 5e-9


def test_find_connections():

    # Remove any existing references to other Connections
    gc.collect()

    sig_a = Signal()
    sig_b = Signal()
    sig_c = Signal()
    sig_d = Signal()

    con_ab = Connection(sig_a, sig_b, 10e-9, 1e-9)
    con_bc = Connection(sig_b, sig_c, 20e-9, 2e-9)
    con_cd = Connection(sig_c, sig_d, 30e-9, 3e-9)

    assert len(list(Connection.get_connections())) == 3

    # Check that input and outputs correspond to expected
    for con in Connection.get_connections():
        expected = {
            sig_a: sig_b,
            sig_b: sig_c,
            sig_c: sig_d
        }
        assert con.output == expected[con.input]

    del expected, con
    # Delete a connection, it should be destroyed
    ref = weakref.ref(con_cd)
    print("\nRef before {}".format(sys.getrefcount(con_cd)))
    del sig_d, con_cd, sig_c
    print("Ref after {}".format(sys.getrefcount(ref())))

    gc.collect()

    assert len(list(Connection.get_connections())) == 2
