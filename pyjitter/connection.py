from pyjitter.signal import Signal, Edge
from typing import List
import weakref


class Connection:
    """
    This class represents the connection between two signals. There is an
    input signal and an output signal, the output is generated based on the
    _edges of the input + some delay + delay uncertainty.
    """
    _all_connections = []   # Keeps weakrefs to all instantiated connections

    def __init__(self, input: Signal, output: Signal, delay, delay_uncertainty):
        """
        :param input: The input signal
        :param output: The output signal
        :param delay: The deterministic part of the delay between in -> out
        :param delay_uncertainty: The peak to peak delay uncertainty
        """

        self.input: Signal = input
        self.output: Signal = output
        self.output.connection = self

        self.delay = delay
        self.delay_uncertainty = delay_uncertainty

        self._all_connections.append(weakref.ref(self))

    @classmethod
    def get_connections(cls):
        for conn_ref in cls._all_connections:
            conn = conn_ref()
            if conn is not None:
                yield conn

    def calculate_edges(self):
        for edge in self.input.edges:
            total_uncertainty = edge.uncertainty + self.delay_uncertainty
            output_edge_avg = edge.time + self.delay
            output_edge = Edge(output_edge_avg, edge.end_level,
                               edge.trans_time, total_uncertainty)
            yield output_edge