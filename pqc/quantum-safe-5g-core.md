# Quantum Safe 5G Core
### PQTN Compliant 5G Core
**Author:** [Aditya Koranga](https://www.linkedin.com/in/aditya-koranga/) & [Shubham Kumar](https://www.linkedin.com/in/chmodshubham/)

**Published:** August 08, 2025

## Network Function PQC Migration

### AMF (Access and Mobility Management Function)
| Network Function | Interface / Properties | Protocol | Current Algorithms | PQTN Specified Algorithms | Status |
|---|---|---|---|---|---|
| AMF | N2 | NGAP over SCTP | IPSec (Classical) | <span style="color: #0066cc; font-weight: bold;">IPSec with ML-KEM-768</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| AMF | SBI (Namf): N8, N12, N22, etc. | HTTP/2 + mTLS 1.3 | Classical: ECDHE + ECDSA, RSA, etc. | <span style="color: #0066cc; font-weight: bold;">ML-KEM-768 + ML-DSA-65 or Hybrid PQC</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| AMF | SBI (Authorization) | OAuth2.0 | RS256 or ES256 | <span style="color: #0066cc; font-weight: bold;">ML-DSA or Hybrid ML-DSA</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |

### SMF (Session Management Function)
| Network Function | Interface / Properties | Protocol | Current Algorithms | PQTN Specified Algorithms | Status |
|---|---|---|---|---|---|
| SMF | N4 | PFCP over UDP | IPSec (Classical) | <span style="color: #0066cc; font-weight: bold;">IPSec with ML-KEM-768</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| SMF | SBI (Nsmf): N7, N10, N11, etc. | HTTP/2 + mTLS 1.3 | Classical: ECDHE + ECDSA, RSA, etc. | <span style="color: #0066cc; font-weight: bold;">ML-KEM-768 + ML-DSA-65 or Hybrid PQC</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| SMF | SBI (Authorization) | OAuth2.0 | RS256 or ES256 | <span style="color: #0066cc; font-weight: bold;">ML-DSA or Hybrid ML-DSA</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |

### UDM (Unified Data Management)
| Network Function | Interface / Properties | Protocol | Current Algorithms | PQTN Specified Algorithms | Status |
|---|---|---|---|---|---|
| UDM | SIDF Function | ECIES | ECC: X25519 & secp256 | <span style="color: #0066cc; font-weight: bold;">ML-KEM-768 or X25519MLKEM768 with AES-256</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| UDM | SBI (Nudm): N8, N10, N13, etc. | HTTP/2 + mTLS 1.3 | Classical: ECDHE + ECDSA, RSA, etc. | <span style="color: #0066cc; font-weight: bold;">ML-KEM-768 + ML-DSA-65 or Hybrid PQC</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| UDM | SBI (Authorization) | OAuth2.0 | RS256 or ES256 | <span style="color: #0066cc; font-weight: bold;">ML-DSA or Hybrid ML-DSA</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |

### NRF (Network Repository Function)
| Network Function | Interface / Properties | Protocol | Current Algorithms | PQTN Specified Algorithms | Status |
|---|---|---|---|---|---|
| NRF | SBI (Nnrf) | HTTP/2 + mTLS 1.3 | Classical: ECDHE + ECDSA, RSA, etc. | <span style="color: #0066cc; font-weight: bold;">ML-KEM-768 + ML-DSA-65 or Hybrid PQC</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| NRF | OAuth (Authorization Server) | JWT/JWS | RS256 or ES256 | <span style="color: #0066cc; font-weight: bold;">ML-DSA or Hybrid ML-DSA</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |

### UPF (User Plane Function)
| Network Function | Interface / Properties | Protocol | Current Algorithms | PQTN Specified Algorithms | Status |
|---|---|---|---|---|---|
| UPF | N3 | GTP-U over UDP | IPSec (Classical) | <span style="color: #0066cc; font-weight: bold;">IPSec with ML-KEM-768</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| UPF | N4 | PFCP over UDP | IPSec (Classical) | <span style="color: #0066cc; font-weight: bold;">IPSec with ML-KEM-768</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| UPF | N6 | Various | Depends on deployment | <span style="color: #0066cc; font-weight: bold;">IPSec with ML-KEM-768</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |

### AUSF (Authentication Server Function)
| Network Function | Interface / Properties | Protocol | Current Algorithms | PQTN Specified Algorithms | Status |
|---|---|---|---|---|---|
| AUSF | SBI (Nausf): N12, N13, etc. | HTTP/2 + mTLS 1.3 | Classical: ECDHE + ECDSA, RSA, etc. | <span style="color: #0066cc; font-weight: bold;">ML-KEM-768 + ML-DSA-65 or Hybrid PQC</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| AUSF | SBI (Authorization) | OAuth2.0 | RS256 or ES256 | <span style="color: #0066cc; font-weight: bold;">ML-DSA or Hybrid ML-DSA</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |

### PCF (Policy Control Function)
| Network Function | Interface / Properties | Protocol | Current Algorithms | PQTN Specified Algorithms | Status |
|---|---|---|---|---|---|
| PCF | SBI (Npcf): N5, N7, N15, etc. | HTTP/2 + mTLS 1.3 | Classical: ECDHE + ECDSA, RSA, etc. | <span style="color: #0066cc; font-weight: bold;">ML-KEM-768 + ML-DSA-65 or Hybrid PQC</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| PCF | SBI (Authorization) | OAuth2.0 | RS256 or ES256 | <span style="color: #0066cc; font-weight: bold;">ML-DSA or Hybrid ML-DSA</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |

### NSSF (Network Slice Selection Function)
| Network Function | Interface / Properties | Protocol | Current Algorithms | PQTN Specified Algorithms | Status |
|---|---|---|---|---|---|
| NSSF | SBI (Nnssf): N22 | HTTP/2 + mTLS 1.3 | Classical: ECDHE + ECDSA, RSA, etc. | <span style="color: #0066cc; font-weight: bold;">ML-KEM-768 + ML-DSA-65 or Hybrid PQC</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| NSSF | SBI (Authorization) | OAuth2.0 | RS256 or ES256 | <span style="color: #0066cc; font-weight: bold;">ML-DSA or Hybrid ML-DSA</span> | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |

## Inter-PLMN and Roaming Interfaces
| Interface | Function | Protocol | Current Crypto | PQTN Specified Algorithms | Status |
|---|---|---|---|---|---|
| N32-c (Control Plane) | SEPP–SEPP | TLS 1.3 | Classical: ECDHE + ECDSA, RSA, etc. | <span style="color: #0066cc; font-weight: bold;">ML-KEM-768 + ML-DSA-65 or Hybrid PQC</span> | <span style="background-color: #fff3cd; color: #856404; padding: 2px 6px; border-radius: 3px;">🔄 Ongoing</span> |
| N32-f (Forwarding) | SEPP–SEPP | HTTP/2 TLS 1.3 | Classical: ECDHE + ECDSA, RSA, etc. | <span style="color: #0066cc; font-weight: bold;">ML-KEM-768 + ML-DSA-65 or Hybrid PQC</span> | <span style="background-color: #fff3cd; color: #856404; padding: 2px 6px; border-radius: 3px;">🔄 Ongoing</span> |

## Management and Support Interfaces
| System | Interface | Protocol | Current Crypto | PQTN Specified Algorithms | Notes | Status |
|---|---|---|---|---|---|---|
| Element Management | HTTPS | TLS 1.2/1.3 | RSA/ECDSA | <span style="color: #0066cc; font-weight: bold;">ML-DSA or Hybrid ML-DSA</span> | Admin access security | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |
| SSH Management | SSH | SSH 2.0 | RSA/ECDSA | <span style="color: #0066cc; font-weight: bold;">ML-DSA or Hybrid ML-DSA</span> | Remote shell access | <span style="background-color: #d4edda; color: #155724; padding: 2px 6px; border-radius: 3px;">✅ Completed</span> |

## Database and Storage Migration
| Component | Interface | Current Protection | PQTN Specified Protection | Data Sensitivity |
|---|---|---|---|---|
| UDM Database | Internal API | AES-128 + RSA key wrap | <span style="color: #0066cc; font-weight: bold;">AES-256 + ML-KEM-768 key wrap</span> | <span style="color: #dc3545; font-weight: bold;">Subscriber data, SUPI</span> |
| Configuration DB | Internal API | AES-128 + RSA | <span style="color: #0066cc; font-weight: bold;">AES-256 + ML-DSA-65</span> | <span style="color: #fd7e14; font-weight: bold;">Network configuration</span> |

## Certificate and Key Management
| PKI Component | Current Algorithm | PQTN Specified Algorithms | Transition Method | Dependencies |
|---|---|---|---|---|
| <span style="color: #6f42c1; font-weight: bold;">Root CA</span> | RSA-4096 | <span style="color: #0066cc; font-weight: bold;">ML-DSA-87</span> | New root deployment | HSM upgrade |
| <span style="color: #6f42c1; font-weight: bold;">Intermediate CA</span> | RSA-2048 | <span style="color: #0066cc; font-weight: bold;">ML-DSA-65</span> | Cross-signed transition | Root CA ready |
| <span style="color: #6f42c1; font-weight: bold;">NF Certificates</span> | ECDSA P-256 | <span style="color: #0066cc; font-weight: bold;">ML-DSA-65</span> | Parallel issuance | Intermediate CA |
| <span style="color: #6f42c1; font-weight: bold;">TLS Server Certs</span> | ECDSA P-256 | <span style="color: #0066cc; font-weight: bold;">ML-DSA-65</span> | Rolling replacement | Per NF schedule |
| <span style="color: #6f42c1; font-weight: bold;">Client Certificates</span> | ECDSA P-256 | <span style="color: #0066cc; font-weight: bold;">ML-DSA-44</span> | On-demand issuance | Service requests |
