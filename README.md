# seg-info-N1-cryptography

Exercises for the **Security Information** (SegInfo) course, covering classic cryptography and secure key exchange protocols.

## Contents

### Caesar Cipher
TCP client/server implementing the Caesar cipher for encrypted communication over a network.

### Diffie-Hellman
TCP client/server implementing the Diffie-Hellman key exchange to establish a shared secret over an insecure channel, followed by encrypted communication.

Run the client with `--attack` to simulate a peer encrypting with a **wrong key**:

```bash
python3 Simple_tcpClient.py          # normal exchange
python3 Simple_tcpClient.py --attack # client uses shared_secret + 50 as key
```

#### Notes on the `--attack` flag

This is **not** a real attack on Diffie-Hellman. It simulates a key mismatch:
the client encrypts with `shared_secret + 50`, so the honest server cannot decrypt
the message and reports `Decryption failed` instead of crashing. No third party
intercepts anything. Real attacks against plain DH would be:

- **Man-in-the-middle**: an attacker replaces `A`/`B` during the exchange and
  ends up sharing a secret with each side, since plain DH has no authentication.
- **Discrete log brute force**: an eavesdropper recovers the private key from the
  public values `(p, g, A)`. Trivial here because the prime is only 8 bits;
  infeasible with properly sized primes (2048+ bits).

#### Why the response comes back almost intact

With a wrong key, only the *first* leg is broken (server receives garbage). On
the return trip the damage cancels out instead of stacking, because each side
reuses its own key consistently and XOR is self-inverse (`X ⊕ K ⊕ K = X`):

```
P ──⊕Kw──> C1 ──⊕Kr──> garbage ──upper()──> G' ──⊕Kr──> C2 ──⊕Kw──> ≈ P
```

Every key application undoes itself across the round trip; only genuine data
mutation mid-flight (the server's `.upper()`) leaves permanent damage. In
practice the corrupted bytes often become NUL characters (`\x00`), which are
invisible in the terminal — print with `repr()` to see them. This self-canceling
behavior is specific to raw XOR (malleable ciphers); with a block cipher like
AES the response really would come back unrecoverable.

## How to Run

Each directory contains a `Simple_tcpServer.py` and a `Simple_tcpClient.py`. Start the server first, then run the client in a separate terminal.
