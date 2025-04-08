# PKE-MET: Implementation of Public-Key Encryption with Multi-Ciphertext Equality Test

This repository contains an implementation of the Public-Key Encryption with Multi-Ciphertext Equality Test (PKE-MET) scheme, as presented in the paper [PKE-MET: Public-Key Encryption With Multi-Ciphertext Equality Test in Cloud Computing](https://ieeexplore.ieee.org/document/9078833/). The PKE-MET scheme allows a cloud server to determine whether multiple ciphertexts, encrypted under different public keys, correspond to the same plaintext without revealing the plaintext itself.

## Overview

The PKE-MET scheme enhances traditional Public-Key Encryption with Equality Test (PKEET) by enabling equality tests among more than two ciphertexts. This is particularly useful in cloud computing scenarios where efficient and secure data deduplication and search functionalities are required.

## Features

- **Multi-Ciphertext Equality Test**: Allows testing the equivalence of multiple ciphertexts encrypted under different public keys.
- **Security**: Provides security proofs under the defined security models, including OW-CPA and IND-CPA.
- **Flexibility**: Extends to Public-Key Encryption with Flexible Multi-Ciphertext Equality Test (PKE-FMET), enabling equality tests on any number of ciphertexts as long as certain conditions are met.

## Repository Structure

- `cyclic_group.py`: Contains implementations related to cyclic groups used in the scheme.
- `finite_field.py`: Provides functionalities for operations over finite fields.
- `pke_met.py`: Core implementation of the PKE-MET scheme.
- `utils.py`: Utility functions supporting the implementation.
- `main.py`: Demonstrates the usage of the PKE-MET implementation with example scenarios.

## Requirements

- Python 3.x
- Pycryptodome

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/sasank-pankam/pke-met.git
   ```

2. Navigate to the project directory:

   ```bash
   cd pke-met
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the demonstration script:

   ```bash
   python demo.py
   ```

   This will execute example scenarios demonstrating the PKE-MET scheme's functionalities.

## References

- Susilo, W., Guo, F., Zhao, Z., & Wu, G. (2020). PKE-MET: Public-Key Encryption With Multi-Ciphertext Equality Test in Cloud Computing. _IEEE Transactions on Cloud Computing_, 10(2), 1476-1488. [https://doi.org/10.1109/TCC.2020.2990201](https://doi.org/10.1109/TCC.2020.2990201)

## Acknowledgements

This implementation is based on the work by Susilo et al. and aims to provide a practical demonstration of the PKE-MET scheme for educational and research purposes.
