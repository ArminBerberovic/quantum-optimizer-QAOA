namespace QuantumLibrary {
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Measurement;
  open Microsoft.Quantum.Canon;
 
  operation runQAOA(gamma: Double, beta : Double) : Result[] {

    use qubits = Qubit[6];
    ApplyToEach(H, qubits);

      CNOT(qubits[0],qubits[1]);
      Rz(gamma,qubits[1]);
      CNOT(qubits[0],qubits[1]);

      CNOT(qubits[0],qubits[5]);
      Rz(gamma,qubits[5]);
      CNOT(qubits[0],qubits[5]);

      CNOT(qubits[1],qubits[2]);
      Rz(gamma,qubits[2]);
      CNOT(qubits[1],qubits[2]);

      CNOT(qubits[1],qubits[5]);
      Rz(gamma,qubits[5]);
      CNOT(qubits[1],qubits[5]);

      CNOT(qubits[2],qubits[3]);
      Rz(gamma,qubits[3]);
      CNOT(qubits[2],qubits[3]);

      CNOT(qubits[2],qubits[4]);
      Rz(gamma,qubits[4]);
      CNOT(qubits[2],qubits[4]);

      CNOT(qubits[3],qubits[4]);
      Rz(gamma,qubits[4]);
      CNOT(qubits[3],qubits[4]);

      CNOT(qubits[4],qubits[5]);
      Rz(gamma,qubits[5]);
      CNOT(qubits[4],qubits[5]);

      Rx(beta,qubits[0]);
      Rx(beta,qubits[1]);
      Rx(beta,qubits[2]);
      Rx(beta,qubits[3]);
      Rx(beta,qubits[4]);
      Rx(beta,qubits[5]);
 
    let results = MeasureEachZ(qubits);
    ResetAll(qubits);

	  return results;
  }
}

