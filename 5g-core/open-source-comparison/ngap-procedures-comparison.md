# NGAP Procedures Comparison (Class 1 EPs)

**Author:**
**Published:**

> **Note:** This comparison reflects the projects as of April 17, 2025. New features or procedures may not be included.

## Introduction

The NG Application Protocol (NGAP) defines the signaling procedures exchanged over the N2 interface between the gNB (RAN) and the AMF in a 5G Standalone (SA) network. NGAP procedures are grouped into **Class 1** (request/response, with an explicit success or failure outcome) and **Class 2** (no response expected) Elementary Procedures (EPs).

This document tracks which **Class 1 NGAP procedures** are implemented across four widely used open-source 5G Core / RAN-facing projects:

- **Free5GC/SDCore**
- **OAI** (OpenAirInterface)
- **Open5GS**
- **Magma**

The comparison is based on the presence of each NGAP message (request, response/acknowledge, and failure variants) in the respective codebases. A `—` indicates the message was not evaluated / no data is available for that project.

## 1. Summary

| Platform | Class 1 Messages Implemented (of 82 tracked) |
| --- | :---: |
| Free5GC/SDCore | 44 |
| OAI | 20 |
| Open5GS | 32 |
| Magma | 16 |

Free5GC/SDCore has the broadest Class 1 NGAP coverage among the four projects, including full support for AMF/RAN configuration update, handover, and PWS-related procedures. OAI and Open5GS focus primarily on core mobility procedures (handover, initial context setup, PDU session management), while Magma implements only the baseline procedures required for NG setup, initial context setup, and PDU session resource management — it does not implement handover, configuration update, or broadcast/multicast (MBS) related procedures.

None of the four projects currently implement the newer Release 17/18 procedures: UE Context Suspend/Resume, UE Radio Capability ID Mapping, Broadcast/Distribution Session Setup/Modification/Release, Multicast Session Activation/Deactivation/Update, Timing Synchronisation Status, MT Communication Handling, or Broadcast Session Transport.

## 2. Procedure-by-Procedure Comparison

### AMF Configuration Update

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| AMF CONFIGURATION UPDATE | YES | NO | — | NO |
| AMF CONFIGURATION UPDATE ACKNOWLEDGE | YES | NO | — | NO |
| AMF CONFIGURATION UPDATE FAILURE | YES | NO | — | NO |

### RAN Configuration Update

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| RAN CONFIGURATION UPDATE | YES | NO | YES | NO |
| RAN CONFIGURATION UPDATE ACKNOWLEDGE | YES | NO | YES | NO |
| RAN CONFIGURATION UPDATE FAILURE | YES | NO | YES | NO |

### Handover Cancellation

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| HANDOVER CANCEL | YES | NO | YES | NO |
| HANDOVER CANCEL ACKNOWLEDGE | YES | NO | YES | NO |

### Handover Preparation

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| HANDOVER REQUIRED | YES | YES | YES | NO |
| HANDOVER COMMAND | YES | YES | YES | NO |
| HANDOVER PREPARATION FAILURE | YES | YES | YES | NO |

### Handover Resource Allocation

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| HANDOVER REQUEST | YES | YES | YES | NO |
| HANDOVER REQUEST ACKNOWLEDGE | YES | YES | YES | NO |
| HANDOVER FAILURE | YES | NO | YES | NO |

### Initial Context Setup

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| INITIAL CONTEXT SETUP REQUEST | YES | YES | YES | YES |
| INITIAL CONTEXT SETUP RESPONSE | YES | YES | YES | YES |
| INITIAL CONTEXT SETUP FAILURE | YES | NO | YES | YES |

### NG Reset

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| NG RESET | YES | YES | YES | YES |
| NG RESET ACKNOWLEDGE | YES | YES | YES | YES |

### NG Setup

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| NG SETUP REQUEST | YES | YES | YES | YES |
| NG SETUP RESPONSE | YES | YES | YES | YES |
| NG SETUP FAILURE | YES | YES | YES | YES |

### Path Switch Request

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| PATH SWITCH REQUEST | YES | NO | YES | NO |
| PATH SWITCH REQUEST ACKNOWLEDGE | YES | NO | YES | NO |
| PATH SWITCH REQUEST FAILURE | YES | NO | — | NO |

### PDU Session Resource Modify

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| PDU SESSION RESOURCE MODIFY REQUEST | YES | YES | YES | YES |
| PDU SESSION RESOURCE MODIFY RESPONSE | YES | YES | YES | YES |

### PDU Session Resource Modify Indication

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| PDU SESSION RESOURCE MODIFY INDICATION | YES | NO | — | NO |
| PDU SESSION RESOURCE MODIFY CONFIRM | YES | NO | — | NO |

### PDU Session Resource Release

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| PDU SESSION RESOURCE RELEASE COMMAND | YES | YES | YES | YES |
| PDU SESSION RESOURCE RELEASE RESPONSE | YES | YES | YES | YES |

### PDU Session Resource Setup

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| PDU SESSION RESOURCE SETUP REQUEST | YES | YES | YES | YES |
| PDU SESSION RESOURCE SETUP RESPONSE | YES | YES | YES | YES |

### UE Context Modification

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| UE CONTEXT MODIFICATION REQUEST | YES | NO | YES | NO |
| UE CONTEXT MODIFICATION RESPONSE | YES | NO | YES | NO |
| UE CONTEXT MODIFICATION FAILURE | YES | NO | YES | NO |

### UE Context Release

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| UE CONTEXT RELEASE COMMAND | YES | YES | YES | YES |
| UE CONTEXT RELEASE COMPLETE | YES | YES | YES | YES |

### Write-Replace Warning

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| WRITE-REPLACE WARNING REQUEST | YES | NO | — | NO |
| WRITE-REPLACE WARNING RESPONSE | YES | NO | — | NO |

### PWS Cancel

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| PWS CANCEL REQUEST | YES | NO | — | NO |
| PWS CANCEL RESPONSE | YES | NO | — | NO |

### UE Radio Capability Check

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| UE RADIO CAPABILITY CHECK REQUEST | YES | NO | — | NO |
| UE RADIO CAPABILITY CHECK RESPONSE | YES | NO | — | NO |

### UE Context Suspend

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| UE CONTEXT SUSPEND REQUEST | NO | — | — | NO |
| UE CONTEXT SUSPEND RESPONSE | NO | — | — | NO |
| UE CONTEXT SUSPEND FAILURE | NO | — | — | NO |

### UE Context Resume

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| UE CONTEXT RESUME REQUEST | NO | — | — | NO |
| UE CONTEXT RESUME RESPONSE | NO | — | — | NO |
| UE CONTEXT RESUME FAILURE | NO | — | — | NO |

### UE Radio Capability ID Mapping

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| UE RADIO CAPABILITY ID MAPPING REQUEST | NO | — | — | NO |
| UE RADIO CAPABILITY ID MAPPING RESPONSE | NO | — | — | NO |

### Broadcast Session Setup

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| BROADCAST SESSION SETUP REQUEST | NO | — | — | NO |
| BROADCAST SESSION SETUP RESPONSE | NO | — | — | NO |
| BROADCAST SESSION SETUP FAILURE | NO | — | — | NO |

### Broadcast Session Modification

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| BROADCAST SESSION MODIFICATION REQUEST | NO | — | — | NO |
| BROADCAST SESSION MODIFICATION RESPONSE | NO | — | — | NO |
| BROADCAST SESSION MODIFICATION FAILURE | NO | — | — | NO |

### Broadcast Session Release

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| BROADCAST SESSION RELEASE REQUEST | NO | — | — | NO |
| BROADCAST SESSION RELEASE RESPONSE | NO | — | — | NO |

### Distribution Setup

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| DISTRIBUTION SETUP REQUEST | NO | — | — | NO |
| DISTRIBUTION SETUP RESPONSE | NO | — | — | NO |
| DISTRIBUTION SETUP FAILURE | NO | — | — | NO |

### Distribution Release

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| DISTRIBUTION RELEASE REQUEST | NO | — | — | NO |
| DISTRIBUTION RELEASE RESPONSE | NO | — | — | NO |

### Multicast Session Activation

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| MULTICAST SESSION ACTIVATION REQUEST | NO | — | — | NO |
| MULTICAST SESSION ACTIVATION RESPONSE | NO | — | — | NO |
| MULTICAST SESSION ACTIVATION FAILURE | NO | — | — | NO |

### Multicast Session Deactivation

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| MULTICAST SESSION DEACTIVATION REQUEST | NO | — | — | NO |
| MULTICAST SESSION DEACTIVATION RESPONSE | NO | — | — | NO |

### Multicast Session Update

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| MULTICAST SESSION UPDATE REQUEST | NO | — | — | NO |
| MULTICAST SESSION UPDATE RESPONSE | NO | — | — | NO |
| MULTICAST SESSION UPDATE FAILURE | NO | — | — | NO |

### Timing Synchronisation Status

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| TIMING SYNCHRONISATION STATUS REQUEST | NO | — | — | NO |
| TIMING SYNCHRONISATION STATUS RESPONSE | NO | — | — | NO |
| TIMING SYNCHRONISATION STATUS FAILURE | NO | — | — | NO |

### MT Communication Handling

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| MT COMMUNICATION HANDLING REQUEST | NO | — | — | NO |
| MT COMMUNICATION HANDLING RESPONSE | NO | — | — | NO |
| MT COMMUNICATION HANDLING FAILURE | NO | — | — | NO |

### Broadcast Session Transport

| Procedure (NGAP Message) | Free5GC/SDCore | OAI | Open5GS | Magma |
|---|:---:|:---:|:---:|:---:|
| BROADCAST SESSION TRANSPORT REQUEST | NO | — | — | NO |
| BROADCAST SESSION TRANSPORT RESPONSE | NO | — | — | NO |
| BROADCAST SESSION TRANSPORT FAILURE | NO | — | — | NO |

## 3. Legend

- **YES** — the procedure is implemented in the project's codebase.
- **NO** — the procedure is not implemented.
- **—** — not evaluated / no data available for that project and procedure.
