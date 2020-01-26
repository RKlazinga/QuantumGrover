from src.grover.run_grover import *
from quantuminspire.credentials import enable_account
from quantuminspire.api import QuantumInspireAPI
import time

start_login = time.time()
enable_account("58957ea5a48a801eb5af6adcae7776126c122c9d")
qi = QuantumInspireAPI()
print("Logged in to QI account ({} seconds)".format(str(time.time() - start_login)[:5]))\

backend = qi.get_backend_type_by_name('QX single-node simulator')

SHOT_COUNT = 500

# whether to apply optimization to our generated QASM
# performance improvement of ~20-50%
OPTIMIZE = True

# MODES:
#   - normal: use toffoli gates and ancillary qubits for max speed
#   - no toffoli: same as normal, but replace toffoli gates for 2-gate equivalent circuits. uses ancillary qubits.
#   - crot: no ancillary qubits or toffoli gates, but scales with 3^n gates for n bits
#   - fancy cnot: no ancillary qubits or toffoli gates, scales 2^n
MODE = "no toffoli"


# Search example

# SEARCH_TARGETS = [
#     "000100"[::-1],
#     "100111"[::-1],
# ]
#
# qasm, _, qubit_count, data_qubits = grover_search_qasm(SEARCH_TARGETS, MODE)
# print(qasm)
# execute_search_qasm(SEARCH_TARGETS, qi, qasm, SHOT_COUNT, backend, qubit_count, data_qubits, True)


# SAT example

BOOL_EXPR = "(a and b and c and d) or (a and b and not(c) and not(d))"
# BOOL_EXPR = generate_ksat_expression(4, 5, 5)
# BOOL_EXPR = "(c or not(d) or a or not(b) or not(e)) and (c or not(e) or not(a) or not(b) or d) and (a or e or b or not(d) or c) and (b or a or not(c) or e or d)"
# BOOL_EXPR = "(a and b and c and d) or (a and b and c and d)"
qasm, _, qubit_count, data_qubits = grover_sat_qasm(BOOL_EXPR, MODE, sat_mode="normal")
# write_file = open("qasms/latest_sat.qasm", "w")
# write_file.write(qasm)
# write_file.close()
execute_sat_qasm(qi, qasm, SHOT_COUNT, backend, qubit_count, data_qubits, True)
