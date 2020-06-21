import pytest
from pyjitter.signal import Signal, Edge

from utils import create_basic_signal


class ConnectionMock:
    def __init__(self, edges):
        self.edges = edges

    def calculate_edges(self):
        for edge in self.edges:
            yield edge


def test_independent_signal_edges():
    sig = create_basic_signal()

    edges = tuple(sig.edges)
    assert len(sig.edges) == 3

    # Check that edges have assigned rise and fall times
    for edge in edges:
        if edge.end_level == Signal.Level.HIGH:
            assert edge.trans_time == sig.rise_time
        elif edge.end_level == Signal.Level.LOW:
            assert edge.trans_time == sig.fall_time
        else:
            assert edge.trans_time == max(sig.fall_time,
                                          sig.rise_time)


def test_dependent_signal():
    sig = Signal('I depend')

    edges = [
        Edge(10e-9, Signal.Level.HIGH, 1e-9, 2e-9),
        Edge(20e-9, Signal.Level.LOW, 1e-9, 2e-9),
        Edge(30e-9, Signal.Level.HIGH, 1e-9, 2e-9)
    ]
    conmock = ConnectionMock(edges)

    sig.connection = conmock

    # Adding an edge to a dependent signal should fail
    with pytest.raises(ValueError):
        sig.add_edge(25e-9, Signal.Level.LOW)

    assert len(sig.edges) == 3
