"""Command-line quantum coin toss simulator using Qiskit."""

from __future__ import annotations

import argparse
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qiskit import QuantumCircuit


SUPERPOSITION_EXPLANATION = """\
Superposition:
  A classical bit is either 0 or 1. A qubit can hold a combination of both
  possibilities until measurement.

Quantum coin toss:
  The circuit starts with one qubit in |0>. A Hadamard gate changes it into
  (|0> + |1>) / sqrt(2), giving 0 and 1 equal probability. Measuring the
  qubit collapses it to one result: 0 for heads or 1 for tails.
"""


def build_quantum_coin_toss_circuit() -> QuantumCircuit:
    """Create a one-qubit circuit for a fair quantum coin toss."""
    from qiskit import QuantumCircuit

    circuit = QuantumCircuit(1, 1)

    # Qubit 0 begins in the |0> state, which we will call "heads".
    # The classical bit begins empty and will store the measurement result.

    # Apply a Hadamard gate to qubit 0.
    # This turns |0> into (|0> + |1>) / sqrt(2), an equal superposition.
    circuit.h(0)

    # Measure qubit 0 and write the result into classical bit 0.
    # The superposition collapses to 0 or 1 when measured.
    circuit.measure(0, 0)

    return circuit


def positive_int(value: str) -> int:
    """Parse an argparse value that must be a positive integer."""
    try:
        parsed_value = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc

    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")

    return parsed_value


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Simulate a fair quantum coin toss with a Qiskit circuit.",
    )
    parser.add_argument(
        "-s",
        "--shots",
        type=positive_int,
        default=1024,
        help="number of simulated tosses to run (default: 1024)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="seed the simulator for repeatable results",
    )
    parser.add_argument(
        "--hide-circuit",
        action="store_true",
        help="only print the toss results, not the circuit diagram",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="print a short explanation of superposition before running",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="show a matplotlib bar chart of the measurement results",
    )
    parser.add_argument(
        "--save-plot",
        metavar="PATH",
        help="save the matplotlib bar chart to a file instead of opening a window",
    )

    return parser.parse_args(argv)


def run_quantum_coin_toss(shots: int, seed: int | None = None) -> tuple[QuantumCircuit, dict[str, int]]:
    """Run the circuit on Qiskit's local simulator."""
    from qiskit import transpile
    from qiskit_aer import AerSimulator

    circuit = build_quantum_coin_toss_circuit()

    # AerSimulator is Qiskit's local simulator backend.
    simulator = AerSimulator(seed_simulator=seed)

    # Transpile adapts the circuit to the simulator's supported operations.
    compiled_circuit = transpile(circuit, simulator)

    # Run the circuit many times so the random distribution becomes visible.
    result = simulator.run(compiled_circuit, shots=shots).result()
    return circuit, result.get_counts()


def print_results(circuit: QuantumCircuit, counts: dict[str, int], shots: int, show_circuit: bool) -> None:
    """Print the circuit and toss counts in a CLI-friendly format."""
    heads = counts.get("0", 0)
    tails = counts.get("1", 0)
    heads_percent = heads / shots * 100
    tails_percent = tails / shots * 100

    if show_circuit:
        print(circuit.draw(output="text"))

    print("Quantum coin toss results")
    print(f"Shots:       {shots}")
    print(f"Heads |0>:   {heads:>5} ({heads_percent:5.1f}%)")
    print(f"Tails |1>:   {tails:>5} ({tails_percent:5.1f}%)")


def visualize_results(counts: dict[str, int], shots: int, save_path: str | None = None) -> None:
    """Show or save a bar chart of the measurement results."""
    import matplotlib.pyplot as plt

    labels = ["Heads |0>", "Tails |1>"]
    values = [counts.get("0", 0), counts.get("1", 0)]
    colors = ["#2563eb", "#f97316"]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(labels, values, color=colors)

    ax.set_title("Quantum Coin Toss Measurement Results")
    ax.set_ylabel("Measurements")
    ax.set_ylim(0, max(values + [shots]) * 1.1)
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    for bar, value in zip(bars, values):
        percentage = value / shots * 100
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value} ({percentage:.1f}%)",
            ha="center",
            va="bottom",
        )

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved plot to {save_path}")
    else:
        plt.show()


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    args = parse_args(argv)

    if args.explain:
        print(SUPERPOSITION_EXPLANATION)

    try:
        circuit, counts = run_quantum_coin_toss(shots=args.shots, seed=args.seed)
    except ModuleNotFoundError as exc:
        if exc.name in {"qiskit", "qiskit_aer"}:
            print(
                "Missing dependency. Install Qiskit and the Aer simulator with:\n"
                "  pip install qiskit qiskit-aer matplotlib",
                file=sys.stderr,
            )
            return 1
        raise

    print_results(
        circuit=circuit,
        counts=counts,
        shots=args.shots,
        show_circuit=not args.hide_circuit,
    )

    if args.plot or args.save_plot:
        try:
            visualize_results(counts=counts, shots=args.shots, save_path=args.save_plot)
        except ModuleNotFoundError as exc:
            if exc.name == "matplotlib":
                print(
                    "Missing dependency. Install Matplotlib with:\n"
                    "  pip install matplotlib",
                    file=sys.stderr,
                )
                return 1
            raise

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
