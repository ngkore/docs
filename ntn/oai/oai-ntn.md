# OAI NTN: Inside the Source Code

**Author:** [Megha Koranga](https://www.linkedin.com/in/megha-koranga-7aa3a0203/)

**Published:** May 16, 2025

> *Part 2 of 2: OpenAirInterface (OAI) NTN Series*

Continuing the exploration of Non-Terrestrial Networks (NTN), this second part of the series delves into the technical implementation within the 5G network architecture. The discussion provides a deep dive into the code flow and all the necessary extensions made to the gNB and UE software to enable communication with satellites and other non-terrestrial platforms. This process covers how standard procedures are extended and modified to account for the unique characteristics of NTNs, such as increased delay, Doppler shift, and satellite-specific configuration requirements.

To provide a holistic understanding of the sequence and interplay between various layers and functional blocks, a stepwise flowchart is detailed. This flowchart captures how NTN support is integrated into the OAI stack, starting from gNB initialization, moving through timing adjustments and message scheduling, and concluding with the establishment and synchronization of the NTN link.

A more detailed and interactive version of the flowchart is accessible here:
[OAI NTN Codeflow](https://app.diagrams.net/#G1pdG863MVB1PmqTQG2HVdMAC9hXP82mJm#%7B%22pageId%22%3A%22KzjFfqPiEhOPBe0r8-R2%22%7D)

![alt text](./images/ntn_codeflow_oai.svg)

> Flowchart showing the step-by-step flow of how NTN support is integrated into the OAI stack --- from gNB initialization to timing adjustments and message scheduling.

## Step-by-Step Breakdown of the NTN Flowchart

### gNB

**Step 1:**  
*RCconfig_nr_macrlc(cfg) — MAC & RLC Layer Configuration Entry Point:*  
This is the first major configuration function called after basic system initialization. It sets up the gNB’s MAC and RLC layers by reading configuration from the config interface, serving as the foundation for further protocol stack setup.

**Step 2:**  
*nr_mac_config_scc() — Applying NTN Offsets in MAC:*  
This function takes the serving cell config (scc) and applies critical timing offset calculations for NTN environments. The function invokes `get_NTN_Koffset()` to derive delay-based offsets (e.g., GEO → 478, LEO → 40). These offsets are used to set scheduling delays for essential messages such as Msg2, Msg4, and HARQ, ensuring that the MAC scheduler is aware of NTN-specific timing characteristics.

`[NR_MAC] Candidates per PDCCH aggregation level on UESS: L1: 0, L2: 2, L4: 0, L8: 0, L16: 0`

This log message confirms that the MAC scheduler now initializes with the proper timing shifts required for NTN operation.

**Step 3:**  
*prepare_scc() — Finalizing Serving Cell Config (RRC Layer):*  
This function is a critical part of the early setup flow. Here, the gNB interprets its behavior regarding radio parameters such as frequency, bandwidth, and timing structure. This step constructs the `ServingCellConfigCommon` used in RRC to build SIBs (System Information Blocks), which are central to cell broadcast and UE configuration.  
- Checks the `scc->ext2->ntn_Config_r17` parameter, signaling if NTN mode is enabled.
- When enabled, the system activates additional timing parameters and satellite-specific features as per 3GPP Release 17 requirements.
- Allocates memory for extended SIBs, including the latest v1700 version for NTN.

**Step 4:**  
*get_SIB1_NR() — Populating NTN-Specific Fields in SIB1:*  
This function validates if the gNB is operating in an NTN band using `is_ntn_band(band)` (e.g., band=254 for NTN). If in NTN mode, SIB1 and SIB19 are filled with satellite and NTN-specific parameters.
- Allocates memory for the required SIB1 versions (v1610, v1630, v1700).
- Assigns NR_UE_Timers and constants appropriate for NTN: t300=t301=t310=t319=2000 ms, n310=10, n311=1, t311=3000 ms.
- Sets the `cellBarredNTN_r17` flag to notBarred, indicating that the cell is available for NTN UEs.

These steps ensure all satellite-related and delay-sensitive parameters (orbit type, timing advance, satellite positioning) are accessible to the UE during network entry.

`[NR_RRC] SIB1 freq: offsetToPointA 5`

A representative log confirming that SIB1’s frequency domain resource, specifically offsetToPointA, is set, which defines the starting point of the carrier grid.

**Step 5:**  
*Control Returns to RCconfig_nr_macrlc(cfg):*  
All NTN-specific configuration (SIB1/SIB19 values, timing adjustments, band identification) is now passed from the RRC to MAC. If the system is Standalone (SA mode) and `ntn_Config_r17` is present:
- Calls `nr_mac_configure_sib19()` to schedule SIB19, which includes key NTN information such as satellite position, velocity, timing advance, and Doppler compensation.

`[HW] No connected device, generating void samples...`

**Step 6:**  
*gNB_dlsch_ulsch_scheduler() — Main Downlink+Uplink Scheduling Function (every slot):*  
This function is repeatedly called each slot and manages downlink and uplink scheduling.
- Handles SIB1 and SIB19 scheduling.
- Schedules PRACH (Msg1) resource allocation using `NTN_Koffset`.
- Invokes `schedule_nr_sib19()` to broadcast satellite-related parameters.
- Maintains Msg1 timing alignment accounting for GEO/LEO propagation delays.

The function also continuously monitors if any UE has triggered random access, then initiates the appropriate action sequence for message handling.

`get_feasible_msg3_tda()`

Example scheduling logs indicate the activation of RA processes and the addition of new UE context.  
`[NR_MAC] 414.4 UE RA-RNTI 003d TC-RNTI d7f9: Activating RA process index 0 [NR_MAC] Adding new UE context with RNTI 0xd64f`.

**Step 7:**  
*Uplink Preprocessor — nr_ulsch_preprocessor():*  
With new UE context created, the uplink preprocessor manages the scheduling of uplink data.
- For NTN, applies an adjusted K2 value with `get_NTN_Koffset()` (e.g., GEO: K2=484, LEO: K2=46).
- K2 represents the delay between the downlink control indication (DCI) grant and uplink transmission (PUSCH).

As a result, the gNB is able to schedule Msg3 sufficiently in advance so it arrives on time, even considering significant GEO/LEO delays. Meanwhile, the system schedules related messages for other UEs.

`[NR_MAC]   UE f8de: Msg3 scheduled (415.3 TDA 0) [NR_MAC]  UE d7f9: 415.3 Generating RA-Msg2 DCI`

**Step 8:**  
*Msg3 Received and Msg4 Scheduling Begins:*  
Upon successful Msg3 reception, the logs confirm this event and the transition of the UE state.
`[NR_MAC]   507. 3 PUSCH with TC_RNTI 0xd64f received correctly [NR_MAC]   Activating scheduling Msg4 for TC_RNTI 0xd64f (state WAIT_Msg3) [NR_RRC]   Decoding CCCH: RNTI d64f, payload_size 6`

The system then prepares Msg4, while the RRC begins decoding the connection request from the UE.

**Step 9:**  
*Continuous Loop After Msg3 — Main Slot Scheduler:*  
Following Msg3, the main gNB scheduling function loops through each slot, handling Msg4 scheduling, uplink timing, and measurement reporting as required. This loop also triggers functions such as `nr_ulsch_preprocessor()` and `nr_csi_meas_reporting()` for ongoing slot-based processing.

`[NR_RRC] [DL] Send RRC Setup`

This log entry confirms that the Msg4 data for the UE is prepared and is ready for delivery through PDSCH as part of Msg4.

**Step 10:**  
*Msg4 Scheduling Phase:*  
Finally, `nr_generate_Msg4_MsgB()` is called to generate Msg4, and `nr_acknack_scheduling()` computes the expected ACK/NACK feedback timing using `NTN_gNB_Koffset()` to compensate for satellite-induced delays. The gNB logs reflect Msg4 transmission and the scheduling of the UE's feedback.

`[NR_MAC] UE dGenerate Msg4: feedback at  557. 2, payload 201 bytes,  next state nrRA_WAIT_Msg4_MsgB_ACK`

### UE

**Step 1:**  
*apply_ntn_config() Called from UE_thread() (Repeatedly):*  
Within the `UE_thread()` loop (in `nr-ue.c`), `apply_ntn_config()` is invoked repeatedly to apply satellite-related timing configurations for the UE. These include updating the orbit type, delay offsets, and all relevant NTN parameters depending on the current satellite environment (GEO or LEO).

`[NR_RRC]   Found SIB19`

**Step 2:**  
*SIB19 Decoding and NTN Configuration Transfer:*  
After successfully decoding SIB19, the UE triggers `process_msg_rcc_to_mac()` to transfer satellite-related configuration data (orbit type, timing advance adjustments) from RRC to MAC.

**Step 3:**  
*nr_rrc_mac_config_other_sib() — Applying SIB19 and Starting RA (NTN-Specific):*  
This function applies the new NTN configuration within the MAC layer:
- It updates the `ntn_Config_r17` parameter.
- Computes the necessary timing advance value using `configure_ntn_ta()`.
- Changes UE state to `UE_PERFORMING_RA`, which means it is now prepared to start the Random Access (RA) process with satellite-aware timing.

**Step 4:**  
*configure_ntn_ta() — Computing Total UE Timing Advance for NTN:*  
The UE calls `calculate_ue_sat_ta()` to determine the one-way signal delay based on satellite and UE 3D positions. For example, in GEO, this results in a value around 238.74 ms, which is incorporated as part of the UE's overall timing advance value. This ensures Msg3 transmission is appropriately scheduled to arrive at the gNB on time, even under extreme satellite delays.

**Step 5:**  
*schedule_ntn_config_command() — Delivering NTN Timing to PHY Layer:*  
After all timing values are computed and configured in MAC, this function prepares a dedicated FAPI PDU for the PHY layer, containing the total timing advance, drift, and Koffset values. The PHY layer then has full visibility of the timing implications and can schedule uplink transmissions, such as Msg3, with slot-level accuracy, even for high-delay environments.

**Step 6:**  
*nr_ue_scheduled_response_dl() and configure_ntn_params() — Final PHY Configuration:*  
At the final stage, the PHY layer processes the incoming configuration message (in `nr_ue_scheduled_response_dl()`).
- Upon recognizing `FAPI_NR_DL_NTN_CONFIG_PARAMS`, `configure_ntn_params()` loads all the necessary satellite timing values, including the total time advance (`ntn_total_time_advance_ms`) and any required drift correction, into the PHY.
- This step enables the UE to align uplink transmissions (Msg3 and PUCCH) precisely with gNB expectations even with the extensive and asymmetric delays of satellites.

**Step 7(a):**  
*UE Initiates 4-Step Random Access Procedure with NTN Adjustments:*  
The RA process is started in the MAC and PHY layer with applied satellite delay and Doppler compensation values:
`apply_ntn_config()` is invoked again from within the per-slot PHY processing loop, ensuring PRACH occasions and Msg1 events are properly scheduled for satellite-based communication.

`[MAC] Initialization of 4-Step CBRA procedure [NR_MAC] PRACH scheduler: Selected RO Frame x, Slot 9, Symbol 0, Fdm 0`

As Msg1 is sent, the UE prepares to receive Msg2 and apply the timing advance determined by the satellite environment.

**Step 7(b):**  
*Msg1 Sent, Msg2 Received, TA Applied (NTN Flow):*  
The UE returns to its processing loop, receives Msg2 (`[PHY] RAR-Msg2 decoded [NR MAC] [UE 0] Found RAR with the intended RAPID 56 [MAC] Received TA command 31`), and applies the relevant timing adjustment.  
- The timing for Msg3 is calculated using `GET_DURATION_RX_TO_TX()`.
- Continuous invocation of `apply_ntn_config()` maintains the most accurate PHY layer settings for LEO orbits.

**Step 7(c):**  
*Msg3 Transmission — NTN Timing Fully Applied:*  
Logs such as `[NR MAC] [RAPROC] [163.3] RA-Msg3 transmitted` confirm successful Msg3 transmission at the correct slot (and delay). The function `nr_Msg3_transmitted()` finalizes this process, noting the total delay applied for GEO/LEO conditions. The UE continues calling `apply_ntn_config()` to maintain alignment for Msg4 and subsequent feedback/ACK scheduling.

**Step 7(d):**  
*Msg4 Acknowledged — RA Procedure Successful:*  
gNB confirms acknowledgment:
`[NR_MAC]  UE : Received Ack of Msg4. CBRA procedure succeeded!`
UE logs:
`4-Step RA procedure succeeded. CBRA: Contention Resolution is successful.`

This marks the conclusion of the contention-based RA procedure, indicating successful handover and synchronization even with high satellite delays.

**Step 8:**  
*Post-RA: UE Begins RRC Setup Completion:*  
`[NR_RRC] [UE 0] [RAPROC] Logical Channel UL-DCCH (SRB1), Generating RRCSetupComplete (bytes32)`
At this point, the UE sends the RRCSetupComplete message via UL-DCCH (SRB1 channel), confirming its full RRC connection establishment with the gNB and its official admission into the network. The UE continues to invoke `apply_ntn_config()` every slot to retain timing precision for all subsequent communication over the satellite link.

## Data Exchange Between UE and gNB

![Alternative text](./images/gnb_GEO.png)

*gNB (for GEO)*

Example gNB log output demonstrates successful Msg4 acknowledgment, RRC setup, and ongoing uplink/downlink activity, evidencing all NTN timing offsets are correctly applied.

![Alternative text](./images/UE_GEO.png){width="800px"}

*UE (for GEO)*

This concludes Part II of the NTN blog series, with a comprehensive examination of the code flow empowering Non-Terrestrial Network (NTN) support in OpenAirInterface. By analyzing both gNB and UE perspectives, the stepwise walkthrough covers crucial aspects including SIB19 processing, NTN-specific timing advance calculation, and full synchronization across the 4-step Random Access Procedure.

The provided flowchart consolidates this complex interaction, showcasing the function calls and log traces instrumental to establishing NTN-aware connectivity in OAI.
