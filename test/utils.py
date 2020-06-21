from pyjitter.signal import Signal


def create_basic_signal() -> Signal:
    sig = Signal('basic')

    sig.add_edge(10e-9, Signal.Level.HIGH, 2e-9)
    sig.add_edge(20e-9, Signal.Level.LOW, 3e-9)
    sig.add_edge(25e-9, Signal.Level.LOW, 2e-9)  # This should not be added
    sig.add_edge(30e-9, Signal.Level.Z, 2e-9)

    return sig