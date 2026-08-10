# 5G Core NF APIs Across 3GPP Releases 15–18

**Author:** [Khushi Chhillar](https://www.linkedin.com/in/kcl17/)

**Published:** April 8, 2025

> **Note:** All service definitions link to [jdegre/5GC_APIs](https://github.com/jdegre/5GC_APIs), a community-maintained mirror of the 3GPP-defined OpenAPI YAML specifications for the 5G Core Service-Based Interfaces (SBIs).

The tables below track how the Service-Based Interfaces (SBIs) exposed by each 5G Core network function (NF) have grown across 3GPP Releases 15 through 18. Services <mark>highlighted</mark> in a release column were newly introduced in that release relative to the previous one. Each NF has its own table so the release-over-release additions stay easy to scan.

> **Note:** These tables are wide. For a better view, zoom out your browser to about 50% (<kbd>Ctrl</kbd> + <kbd>-</kbd>) before reading them.

## AMF

```{table}
:class: dec-font-size

| REL 15 | REL 16 | REL 17 | REL 18 |
| --- | --- | --- | --- |
| • [Communication](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_Communication.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_EventExposure.yaml)<br>• [Location](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_Location.yaml)<br>• [MT](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_MT.yaml) | • [Communication](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_Communication.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_EventExposure.yaml)<br>• [Location](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_Location.yaml)<br>• [MT](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_MT.yaml) | • [Communication](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_Communication.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_EventExposure.yaml)<br>• [Location](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_Location.yaml)<br>• [MT](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_MT.yaml)<br>• <mark>[MBS Communication](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_MBSCommunication.yaml)</mark><br>• <mark>[MBS Broadcast](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_MBSBroadcast.yaml)</mark> | • [Communication](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_Communication.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_EventExposure.yaml)<br>• [Location](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_Location.yaml)<br>• [MT](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_MT.yaml)<br>• [MBS Communication](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_MBSCommunication.yaml)<br>• [MBS Broadcast](https://jdegre.github.io/loader.html?yaml=TS29518_Namf_MBSBroadcast.yaml) |
```

## SMF

```{table}
:class: dec-font-size

| REL 15 | REL 16 | REL 17 | REL 18 |
| --- | --- | --- | --- |
| • [PDU Session](https://jdegre.github.io/loader.html?yaml=TS29502_Nsmf_PDUSession.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29508_Nsmf_EventExposure.yaml) | • [PDU Session](https://jdegre.github.io/loader.html?yaml=TS29502_Nsmf_PDUSession.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29508_Nsmf_EventExposure.yaml)<br>• <mark>[NIDD (Non-IP Data Delivery)](https://jdegre.github.io/loader.html?yaml=TS29542_Nsmf_NIDD.yaml)</mark> | • [PDU Session](https://jdegre.github.io/loader.html?yaml=TS29502_Nsmf_PDUSession.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29508_Nsmf_EventExposure.yaml)<br>• [NIDD (Non-IP Data Delivery)](https://jdegre.github.io/loader.html?yaml=TS29542_Nsmf_NIDD.yaml) | • [PDU Session](https://jdegre.github.io/loader.html?yaml=TS29502_Nsmf_PDUSession.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29508_Nsmf_EventExposure.yaml)<br>• [NIDD (Non-IP Data Delivery)](https://jdegre.github.io/loader.html?yaml=TS29542_Nsmf_NIDD.yaml) |
```

## PCF

```{table}
:class: dec-font-size

| REL 15 | REL 16 | REL 17 | REL 18 |
| --- | --- | --- | --- |
| • [Policy Authorization](https://jdegre.github.io/loader.html?yaml=TS29514_Npcf_PolicyAuthorization.yaml)<br>• [Access and Mobility (AM) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29507_Npcf_AMPolicyControl.yaml)<br>• [Session Management (SM) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29512_Npcf_SMPolicyControl.yaml)<br>• [Background Data Transfer (BDT) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29554_Npcf_BDTPolicyControl.yaml)<br>• [Policy Control Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29523_Npcf_EventExposure.yaml)<br>• [UE Policy Control](https://jdegre.github.io/loader.html?yaml=TS29525_Npcf_UEPolicyControl.yaml) | • [Policy Authorization](https://jdegre.github.io/loader.html?yaml=TS29514_Npcf_PolicyAuthorization.yaml)<br>• [Access and Mobility (AM) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29507_Npcf_AMPolicyControl.yaml)<br>• [Session Management (SM) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29512_Npcf_SMPolicyControl.yaml)<br>• [Background Data Transfer (BDT) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29554_Npcf_BDTPolicyControl.yaml)<br>• [Policy Control Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29523_Npcf_EventExposure.yaml)<br>• [UE Policy Control](https://jdegre.github.io/loader.html?yaml=TS29525_Npcf_UEPolicyControl.yaml) | • [Policy Authorization](https://jdegre.github.io/loader.html?yaml=TS29514_Npcf_PolicyAuthorization.yaml)<br>• <mark>[Access and Mobility (AM) Policy Authorization](https://jdegre.github.io/loader.html?yaml=TS29534_Npcf_AMPolicyAuthorization.yaml)</mark><br>• [Access and Mobility (AM) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29507_Npcf_AMPolicyControl.yaml)<br>• [Session Management (SM) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29512_Npcf_SMPolicyControl.yaml)<br>• [Background Data Transfer (BDT) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29554_Npcf_BDTPolicyControl.yaml)<br>• [Policy Control Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29523_Npcf_EventExposure.yaml)<br>• [UE Policy Control](https://jdegre.github.io/loader.html?yaml=TS29525_Npcf_UEPolicyControl.yaml)<br>• <mark>[Multicast/Broadcast Policy Control](https://jdegre.github.io/loader.html?yaml=TS29537_Npcf_MBSPolicyControl.yaml)</mark><br>• <mark>[Multicast/Broadcast Policy Authorization](https://jdegre.github.io/loader.html?yaml=TS29537_Npcf_MBSPolicyAuthorization.yaml)</mark> | • [Policy Authorization](https://jdegre.github.io/loader.html?yaml=TS29514_Npcf_PolicyAuthorization.yaml)<br>• [Access and Mobility (AM) Policy Authorization](https://jdegre.github.io/loader.html?yaml=TS29534_Npcf_AMPolicyAuthorization.yaml)<br>• [Access and Mobility (AM) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29507_Npcf_AMPolicyControl.yaml)<br>• [Session Management (SM) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29512_Npcf_SMPolicyControl.yaml)<br>• [Background Data Transfer (BDT) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29554_Npcf_BDTPolicyControl.yaml)<br>• [Policy Control Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29523_Npcf_EventExposure.yaml)<br>• [UE Policy Control](https://jdegre.github.io/loader.html?yaml=TS29525_Npcf_UEPolicyControl.yaml)<br>• [Multicast/Broadcast Policy Control](https://jdegre.github.io/loader.html?yaml=TS29537_Npcf_MBSPolicyControl.yaml)<br>• [Multicast/Broadcast Policy Authorization](https://jdegre.github.io/loader.html?yaml=TS29537_Npcf_MBSPolicyAuthorization.yaml)<br>• <mark>[Planned Data Transfer with QoS (PDTQ) Policy Control](https://jdegre.github.io/loader.html?yaml=TS29543_Npcf_PDTQPolicyControl.yaml)</mark> |
```

## UDM

```{table}
:class: dec-font-size

| REL 15 | REL 16 | REL 17 | REL 18 |
| --- | --- | --- | --- |
| • [Subscriber Data Management](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_SDM.yaml)<br>• [UE Context Management](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_UECM.yaml)<br>• [UE Authentication](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_UEAU.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_EE.yaml)<br>• [Parameter Provisioning](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_PP.yaml) | • [Subscriber Data Management](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_SDM.yaml)<br>• [UE Context Management](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_UECM.yaml)<br>• [UE Authentication](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_UEAU.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_EE.yaml)<br>• [Parameter Provisioning](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_PP.yaml)<br>• <mark>[NIDD Authorization](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_NIDDAU.yaml)</mark><br>• <mark>[MT](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_MT.yaml)</mark> | • [Subscriber Data Management](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_SDM.yaml)<br>• [UE Context Management](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_UECM.yaml)<br>• [UE Authentication](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_UEAU.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_EE.yaml)<br>• [Parameter Provisioning](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_PP.yaml)<br>• [NIDD Authorization](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_NIDDAU.yaml)<br>• [MT](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_MT.yaml)<br>• <mark>[Service-Specific Authorization](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_SSAU.yaml)</mark><br>• <mark>[RSDS (Report SM Delivery Status)](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_RSDS.yaml)</mark><br>• <mark>[UEID (UE Identifier)](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_UEID.yaml)</mark> | • [Subscriber Data Management](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_SDM.yaml)<br>• [UE Context Management](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_UECM.yaml)<br>• [UE Authentication](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_UEAU.yaml)<br>• [Event Exposure](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_EE.yaml)<br>• [Parameter Provisioning](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_PP.yaml)<br>• [NIDD Authorization](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_NIDDAU.yaml)<br>• [MT](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_MT.yaml)<br>• [Service-Specific Authorization](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_SSAU.yaml)<br>• [RSDS (Report SM Delivery Status)](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_RSDS.yaml)<br>• [UEID (UE Identifier)](https://jdegre.github.io/loader.html?yaml=TS29503_Nudm_UEID.yaml) |
```

## UDR

```{table}
:class: dec-font-size

| REL 15 | REL 16 | REL 17 | REL 18 |
| --- | --- | --- | --- |
| • [Data Repository](https://jdegre.github.io/loader.html?yaml=TS29504_Nudr_DR.yaml)<br>• [Subscription Data](https://jdegre.github.io/loader.html?yaml=TS29505_Subscription_Data.yaml)<br>• [Policy Data](https://jdegre.github.io/loader.html?yaml=TS29519_Policy_Data.yaml)<br>• [Exposure Data](https://jdegre.github.io/loader.html?yaml=TS29519_Exposure_Data.yaml)<br>• [Application Data](https://jdegre.github.io/loader.html?yaml=TS29519_Application_Data.yaml) | • [Data Repository](https://jdegre.github.io/loader.html?yaml=TS29504_Nudr_DR.yaml)<br>• [Subscription Data](https://jdegre.github.io/loader.html?yaml=TS29505_Subscription_Data.yaml)<br>• [Policy Data](https://jdegre.github.io/loader.html?yaml=TS29519_Policy_Data.yaml)<br>• [Exposure Data](https://jdegre.github.io/loader.html?yaml=TS29519_Exposure_Data.yaml)<br>• [Application Data](https://jdegre.github.io/loader.html?yaml=TS29519_Application_Data.yaml)<br>• <mark>[Group ID Map](https://jdegre.github.io/loader.html?yaml=TS29504_Nudr_GroupIDmap.yaml)</mark> | • [Data Repository](https://jdegre.github.io/loader.html?yaml=TS29504_Nudr_DR.yaml)<br>• [Subscription Data](https://jdegre.github.io/loader.html?yaml=TS29505_Subscription_Data.yaml)<br>• [Policy Data](https://jdegre.github.io/loader.html?yaml=TS29519_Policy_Data.yaml)<br>• [Exposure Data](https://jdegre.github.io/loader.html?yaml=TS29519_Exposure_Data.yaml)<br>• [Application Data](https://jdegre.github.io/loader.html?yaml=TS29519_Application_Data.yaml)<br>• [Group ID Map](https://jdegre.github.io/loader.html?yaml=TS29504_Nudr_GroupIDmap.yaml) | • [Data Repository](https://jdegre.github.io/loader.html?yaml=TS29504_Nudr_DR.yaml)<br>• [Subscription Data](https://jdegre.github.io/loader.html?yaml=TS29505_Subscription_Data.yaml)<br>• [Policy Data](https://jdegre.github.io/loader.html?yaml=TS29519_Policy_Data.yaml)<br>• [Exposure Data](https://jdegre.github.io/loader.html?yaml=TS29519_Exposure_Data.yaml)<br>• [Application Data](https://jdegre.github.io/loader.html?yaml=TS29519_Application_Data.yaml)<br>• [Group ID Map](https://jdegre.github.io/loader.html?yaml=TS29504_Nudr_GroupIDmap.yaml) |
```

## AUSF

```{table}
:class: dec-font-size

| REL 15 | REL 16 | REL 17 | REL 18 |
| --- | --- | --- | --- |
| • [UE Authentication](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_UEAuthentication.yaml)<br>• [SoR (Steering of Roaming) Protection](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_SoRProtection.yaml)<br>• [UPU (UE Parameter Update) Protection](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_UPUProtection.yaml) | • [UE Authentication](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_UEAuthentication.yaml)<br>• [SoR (Steering of Roaming) Protection](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_SoRProtection.yaml)<br>• [UPU (UE Parameter Update) Protection](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_UPUProtection.yaml) | • [UE Authentication](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_UEAuthentication.yaml)<br>• [SoR (Steering of Roaming) Protection](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_SoRProtection.yaml)<br>• [UPU (UE Parameter Update) Protection](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_UPUProtection.yaml) | • [UE Authentication](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_UEAuthentication.yaml)<br>• [SoR (Steering of Roaming) Protection](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_SoRProtection.yaml)<br>• [UPU (UE Parameter Update) Protection](https://jdegre.github.io/loader.html?yaml=TS29509_Nausf_UPUProtection.yaml) |
```

## NSSF

```{table}
:class: dec-font-size

| REL 15 | REL 16 | REL 17 | REL 18 |
| --- | --- | --- | --- |
| • [NSSAI Availability](https://jdegre.github.io/loader.html?yaml=TS29531_Nnssf_NSSAIAvailability.yaml)<br>• [NS Selection](https://jdegre.github.io/loader.html?yaml=TS29531_Nnssf_NSSelection.yaml) | • [NSSAI Availability](https://jdegre.github.io/loader.html?yaml=TS29531_Nnssf_NSSAIAvailability.yaml)<br>• [NS Selection](https://jdegre.github.io/loader.html?yaml=TS29531_Nnssf_NSSelection.yaml) | • [NSSAI Availability](https://jdegre.github.io/loader.html?yaml=TS29531_Nnssf_NSSAIAvailability.yaml)<br>• [NS Selection](https://jdegre.github.io/loader.html?yaml=TS29531_Nnssf_NSSelection.yaml) | • [NSSAI Availability](https://jdegre.github.io/loader.html?yaml=TS29531_Nnssf_NSSAIAvailability.yaml)<br>• [NS Selection](https://jdegre.github.io/loader.html?yaml=TS29531_Nnssf_NSSelection.yaml) |
```

## NRF

```{table}
:class: dec-font-size

| REL 15 | REL 16 | REL 17 | REL 18 |
| --- | --- | --- | --- |
| • [NF Management](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_NFManagement.yaml)<br>• [NF Discovery](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_NFDiscovery.yaml)<br>• [Access Token (OAuth2)](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_AccessToken.yaml) | • [NF Management](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_NFManagement.yaml)<br>• [NF Discovery](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_NFDiscovery.yaml)<br>• [Access Token (OAuth2)](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_AccessToken.yaml)<br>• <mark>[Bootstrapping](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_Bootstrapping.yaml)</mark> | • [NF Management](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_NFManagement.yaml)<br>• [NF Discovery](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_NFDiscovery.yaml)<br>• [Access Token (OAuth2)](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_AccessToken.yaml)<br>• [Bootstrapping](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_Bootstrapping.yaml) | • [NF Management](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_NFManagement.yaml)<br>• [NF Discovery](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_NFDiscovery.yaml)<br>• [Access Token (OAuth2)](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_AccessToken.yaml)<br>• [Bootstrapping](https://jdegre.github.io/loader.html?yaml=TS29510_Nnrf_Bootstrapping.yaml) |
```
