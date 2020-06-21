# Quantum Phase Estimation

This project implements a Quantum Phase Estimation circuit with an arbitrary number of qubits using `Qiskit==0.18.0`.

This is a project for a Quantum Algorithms course at NTU, offered by Professor Wen-Chin Chen (陳文進). References for the project include notes by Professor Chen as well as the documentation at [qiskit.org](https://qiskit.org/).

### Overview

A Quantum Phase Estimation circuit takes a unitary matrix *U* and, by applying it multiple times as a Controlled Unitary followed by a Quantum Fourier Transform, the Quantum Phase Estimation circuit is able to estimate the phase of *U*.

Phase estimation allows for more advanced circuits and algorithms, such as the HHL algorithm which can be used to solve linear systems *Ax = b*.

More details regarding Quantum Phase Estimation can be found in the Jupyter Notebook *QPE_Demonstration.ipynb*.

### Jupyter Setup

- Install [Anaconda](https://docs.anaconda.com/anaconda/install/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Activate the conda base environment from the terminal (`source anaconda3/bin/activate` or `. anaconda3/bin/activate`)
- Create a conda environment (`conda create -n quantum python=3.7`)
- Activate the conda environment (`conda activate quantum`)
- Install necessary packages (`pip install qiskit==0.18.0; conda install jupyter matplotlib numpy mypy`)
- Run Jupyter (`jupyter notebook`)
- Open *QPE_Demonstration.ipynb* and run the cells

### Running *phase_estimation.py*

Alternatively, *phase_estimation.py* can be run directly from the terminal to accept input from the user:
```
python phase_estimation.py
```

### Using a Different Unitary

To use a different Controlled Unitary with an unknown phase, modify `U_function` in *phase_estimation.py* to add the desired set of gates, and to not include the `angle` parameter. Note that `U_function` must return the `QuantumCircuit` that it modifies.

**Note**: Type checking can be performed with mypy:
```
mypy phase_estimation.py
```

