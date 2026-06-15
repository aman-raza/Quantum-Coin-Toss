# Quantum Coin Toss

## Superposition

In classical computing, a bit is either `0` or `1`. A qubit can be in a
superposition, meaning its state can contain both possibilities at once until
it is measured.

For a quantum coin toss, we start with one qubit in `|0>`. Applying a Hadamard
gate creates an equal superposition:

```text
(|0> + |1>) / sqrt(2)
```

When we measure the qubit, it collapses to either `0` or `1`. Because the
Hadamard made both outcomes equally likely, this behaves like a fair coin toss:
`0` can represent heads, and `1` can represent tails.

## CLI Usage

Install Qiskit, the Aer simulator, and Matplotlib:

```bash
pip install qiskit qiskit-aer matplotlib
```

Run the CLI directly:

```bash
python quantum_coin_toss.py
```

Change the number of simulated tosses:

```bash
python quantum_coin_toss.py --shots 5000
```

Print the explanation from the CLI:

```bash
python quantum_coin_toss.py --explain
```

Hide the circuit diagram:

```bash
python quantum_coin_toss.py --hide-circuit
```

Use a repeatable simulator seed:

```bash
python quantum_coin_toss.py --shots 20 --seed 7
```

Show a Matplotlib bar chart of the measurement results:

```bash
python quantum_coin_toss.py --plot
```

Save the chart to an image file:

```bash
python quantum_coin_toss.py --save-plot results.png
```

You can also install it as a command-line application from this folder:

```bash
pip install .
quantum-coin-toss --shots 1024
```

The output shows the circuit, unless hidden, and the number of heads and tails
observed over the requested number of simulated tosses.

<img width="866" height="177" alt="image" src="https://github.com/user-attachments/assets/dc04af52-0fdd-4f3f-b9dd-fac338354d01" />

<img width="1913" height="958" alt="image" src="https://github.com/user-attachments/assets/8186053a-fcdd-4af3-9aae-b932480850cc" />
