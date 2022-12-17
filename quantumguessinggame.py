#!/usr/bin/env python
# coding: utf-8

import qiskit
from qiskit import IBMQ
from qiskit import *
from qiskit.tools.visualization import plot_bloch_multivector
from qiskit.tools.visualization import plot_histogram

from qiskit.tools.monitor import job_monitor #monitors how the job is doing, lets us see when the job is done
IBMQ.save_account('6ec82be171e1a107797861de7f50e09ce8aecbd05920c72e62c1bf6d45e3a49b975b6cac286d734e2bb86450b08aec9bda5abe9d316444bcb6d7983f3e6d048a')
IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
qcomp = provider.get_backend('ibmq_quito') #actual quantum computer
job = execute(circuit,backend = qcomp) #executes the circuit on the backend

 

job_monitor(job) 
result = job.result()


get_ipython().run_line_magic('matplotlib', 'inline')

from qiskit import *
%matplotlib inline
from qiskit.tools.visualization import plot_histogram

# Quantum Guessing Game:

# A secret string is inputted by the user, and the Quantum Computer can guess it in one try
# without knowing the string in any capactity.
print("Let's play a guessing game. Think of a number between 1 and 99,999,999,999,999 and I will guess it.")
print("I will be using the Bernstein-Vazirani algorithm to predict your number much faster than a classic computer could.")
def isValid(number):
    if not number.isdigit():
        print("All characters must be integers, please try again.")
        return False
    if len(number) > 14 or len(number) < 1:
        print("Length of string must be greater than 0 and less than 14, please try again.")
        return False
    else:
        return True

number = input("Enter a number of length n where n is less than 14 and greater than 0: ")


while(not(isValid(number))):
    number = input("Enter a number of length n where n is less than 14 and greater than 0: ")

number = int(number)
secretnumber = bin(number) #decimal to binary

circuit = QuantumCircuit(len(secretnumber)+1,len(secretnumber))

#creating a hadamard gate, used to convert qubit from clustering state to superposed state
circuit.h(range(len(secretnumber))) #range length of secret number 

circuit.x(len(secretnumber)) #last qubit (if 100101, 6) #x gate on the last qubit 
circuit.h(len(secretnumber))#last qubit (if 100101, 6)

circuit.barrier()

for ii, yesno in enumerate(reversed(secretnumber)): #for [i , i
    if yesno == '1':
        circuit.cx(ii, len(secretnumber))
                           

#101001
# circuit.cx(5,6) controlled not gate, being used when bit has a 1 in it. For example above
# circuit.cx(3,6) between 5 and 6, there is a 1, between 3 and 6, there is a 1, and between 
# circuit.cx(0,6) 0 and 6, there is a 1



circuit.barrier()

circuit.h(range((len(secretnumber))))
#apply another set of hadamard gates to finish the circuit 

circuit.barrier()

circuit.measure(range(len(secretnumber)),range(len(secretnumber))) #([qubits], [classicalbits])



circuit.draw(output='mpl') #dotted lines have 1s, the rest have 0s 101001, starting from q5. 
#q6 exists as an attachment point for entanglement

simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit,backend = simulator, shots = 1).result()
count =result.get_counts()
computerAnswer = next(iter(count)) #gets the first key in the count dictionary, or the correct answer back from the quantum computer

backToDecimal = int(computerAnswer, 2) #binary to decimal 
finale = (("Was this your number: %i?")%backToDecimal)
print(finale) #The correct answer guessed by the quantum computer
print(computerAnswer)

circuit.draw(output='mpl') #dotted lines have 1s, the rest have 0s 101001, starting from q5. 
#q6 exists as an attachment point for entanglement


