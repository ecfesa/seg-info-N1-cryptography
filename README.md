# 🔐 SegInfo — Cryptography

Educational cryptography exercises developed for the **Information Security (SegInfo)** course.

The project demonstrates classical encryption, TCP communication, and Diffie–Hellman key exchange.

> ⚠️ **Educational project:** The cryptographic implementations are simplified and are not intended for production use.

## ✨ Features

* 🔤 **Caesar Cipher**

  * TCP client/server communication
  * Message encryption and decryption

* 🔑 **Diffie–Hellman**

  * Public/private key exchange
  * Shared secret generation
  * Encrypted TCP communication

* ⚔️ **Attack Simulation**

  * `--attack` mode simulates communication with an incorrect key
  * Demonstrates the effects of a key mismatch

* 🐍 **Python**

  * No external dependencies
  * Simple command-line execution

## 📁 Project Structure

```text
seg-info-N1-cryptography/
├── caesar_cipher/
│   ├── Simple_tcpClient.py
│   └── Simple_tcpServer.py
│
├── diffie_hellman/
│   ├── Simple_tcpClient.py
│   └── Simple_tcpServer.py
│
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ecfesa/seg-info-N1-cryptography.git
cd seg-info-N1-cryptography
```

### 2. Run an exercise

Start the server first:

```bash
cd caesar_cipher
python3 Simple_tcpServer.py
```

Then, in another terminal:

```bash
python3 Simple_tcpClient.py
```

The same process can be used for Diffie–Hellman:

```bash
cd diffie_hellman
python3 Simple_tcpServer.py
```

```bash
python3 Simple_tcpClient.py
```

### 3. Test the attack simulation

Inside `diffie_hellman/`:

```bash
python3 Simple_tcpClient.py --attack
```

This intentionally uses an incorrect key to demonstrate a key mismatch between the client and server. It is **not a real Man-in-the-Middle attack**.

## 📺 Video Demonstration

> 🎥 **Video coming soon**

A demonstration of the project, including both exercises and the attack simulation, will be added here.

<!-- Future video:
[![Project Demonstration](VIDEO_THUMBNAIL_URL)](VIDEO_URL)
-->

## 📚 Concepts

| Concept                | Implementation  |
| ---------------------- | --------------- |
| TCP communication      | Client / Server |
| Classical cryptography | Caesar Cipher   |
| Key exchange           | Diffie–Hellman  |
| Shared secrets         | Diffie–Hellman  |
| Key mismatch           | `--attack`      |

## ⚠️ Security Notice

This project is intended for **learning purposes only**. The Diffie–Hellman implementation uses intentionally small parameters, and the encryption mechanisms are simplified demonstrations rather than secure cryptographic protocols.

## 👥 Authors

Developed for the **Security Information (SegInfo)** course.

[GitHub Repository](https://github.com/ecfesa/seg-info-N1-cryptography)
