import numpy as np
import qiskit as qs
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
from typing import Tuple, Callable
from functools import partial

def U_function(angle: float, circuit: QuantumCircuit, control: int, target: int) -> QuantumCircuit:
    """
    Adds desired Controlled Unitary gates to a given circuit
    
    [ Required Parameters ]
    circuit: the circuit to add the controlled unitary gates to
    control: the control qubit
    target: the target qubit to which the unitary gets applied
    
    [ Remove this parameter for a U with unknown phase ]
    angle: λ, where U|ψ} = e^(λi)|ψ}
    
    Modify this function to perform the operations of your desired Controlled Unitary
    """
    circuit.cu1(angle, control, target)
    return circuit


def phase_estimation(U: Callable[[QuantumCircuit, int, int], QuantumCircuit], bits: int, show: bool = True, shots: int = 2048) -> Tuple[float, QuantumCircuit]:
    """
    Estimates θ, given a unitary operator U, such that U|ψ} = e^(2πiθ)|ψ}
    
    U: A function that adds controlled unitary gates to a given circuit, and returns the circuit
    bits: bit-size of phase estimation circuit (excluding ψ)
    
    show: if True, displays circuit and histogram of results (Jupyter notebook only)
    shots: number of shots (runs) to be executed
    
    Returns the tuple: (estimated theta, quantum estimation circuit)
    """
    backend = Aer.get_backend('qasm_simulator')
#     q = QuantumCircuit(bits+1, bits)
    qr = QuantumRegister(bits, 'q')
    psi = QuantumRegister(1, 'psi')
    cr = ClassicalRegister(bits, 'c')
    q = QuantumCircuit(qr, psi, cr)
    
    # Apply Unitaries
    q.x(bits) # Initialize |ψ}
    for i in range(bits):
        q.h(i)
        for _ in range(2**i):
            q = U(q, bits, i) # apply controlled unitary
    q.barrier()
    
    # Inverse QFT
    swapped = []
    for a,b in enumerate(range(bits)[::-1]):
        if (a == b) or (a in swapped) or (b in swapped):
            break
        q.swap(a,b) # swap bits
        swapped += [a,b]

    for i in range(bits):
        # apply inverse QFT controlled unitaries
        [q.cu1(-np.pi/2**k, i, qubit) for qubit, k in enumerate(range(1,i+1)[::-1]) if (i > 0) and (qubit < i)]
        q.h(i)
        q.barrier()
    
    # Measure
    [q.measure(i,i) for i in range(bits)]

    if show:
        try:
            display(q.draw(output='mpl'))
        except:
            pass

    counts = execute(q, backend=backend, shots=shots).result().get_counts()
    ans = [int(c,2) for c,v in counts.items() if v == max(counts.values())][0] # result with max counts
    estimated_theta = ans/(2**bits)
    if show:
        try:
            display(plot_histogram(counts))
            print("Highest Count Value: ", bin(ans), " = ", ans)
            print(f"Estimated theta: {ans}/2^{bits} = ", estimated_theta)
        except:
            pass
    return estimated_theta, q

def main():
    bits = int(input("Number of bits: "))
    inp = input("Input a theta to estimate: ")
    try:
        theta = float(inp)
    except ValueError:
        i = inp.split('/')
        try:
            theta = float(i[0])/float(i[1])
        except:
            print(f"Invalid theta {inp}. Using theta = 1/7")
            theta = 1/7
    
    # Create a Unitary function with phase theta
    U = partial(U_function, 2*np.pi*theta)
    
    est_theta, circuit = phase_estimation(U=U, bits=bits, show=False)
    print(f"Estimated theta: {est_theta}")
    print(f"Actual theta: {theta % 1}")

if __name__ == '__main__':
    main()