# Cryptography TLS Projects

This repository contains a collection of cryptography and TLS-based projects implemented using Python and web technologies. The purpose of this repository is to demonstrate secure communication techniques using symmetric encryption, asymmetric encryption, and hybrid cryptographic approaches combined with TLS (Transport Layer Security).

These projects are primarily intended for learning, academic demonstration, and experimentation with cryptographic concepts rather than production deployment.

---

## Project Overview

The repository includes multiple independent projects that showcase different encryption models and how TLS can be used to secure data transmission between a client and a server.

The implementations focus on:
- Data confidentiality using encryption
- Secure key exchange mechanisms
- TLS-enabled communication
- Backend and frontend integration for cryptographic workflows

---

## Projects Included

### 1. Asymmetric Encryption with TLS (`asymm - tls`)
This project demonstrates the use of RSA (asymmetric encryption) along with TLS for secure communication. The backend generates RSA key pairs and uses them to encrypt and decrypt messages exchanged over an HTTPS connection.

### 2. Hybrid Encryption with TLS (`hybrid tls`)
This project implements a hybrid cryptography model where:
- AES (symmetric encryption) is used for encrypting message data
- RSA (asymmetric encryption) is used for encrypting AES keys
- TLS ensures secure transport between client and server

This approach reflects real-world secure communication systems.

### 3. Symmetric Encryption with TLS (`symm - tls`)
This project focuses on symmetric encryption using AES combined with TLS. It demonstrates password-based key derivation, encrypted message exchange, and secure HTTPS communication.

### 4. Symmetric and Asymmetric Combined (`symm-asymm`)
This project shows how symmetric and asymmetric encryption techniques can be combined in a single workflow for secure data handling and verification.

### 5. Logs (`LOGS`)
This folder contains sample log files generated during encryption and decryption operations for analysis and debugging purposes.

---

## Repository Structure

