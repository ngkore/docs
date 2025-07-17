# Understanding Open-Source 5G Core Network Evolution in 2025

Nowadays, the open-source market is filled with open-source 5G cores. If we have to choose one, it's difficult because there are so many options. That's what we are going to discuss here.


## 1. List of Available open source 5G Cores in the market:
- Free5gc
- Open5GS
- Magma Core
- OAI
- Aether SD Core
- Canonical Charmed Aether SD Core
- Ella core
- QCore

Haah 😩, there are so many, aren't there!

Why are there so many cores? What specific areas do they excel in? What makes them different, and how should a user choose one?

There are many questions when we look at the list of 5G Packet Cores. Each core has its own specific use case and unique strengths.

First, let's take a brief look at each of them:

## 2. Detailed Comparison of Major Open-Source 5G Core Projects

### 2.1 Free5GC

**Overview and Background:**

Originating from National Yang Ming Chiao Tung University (Taiwan), Free5GC is hosted by the Linux Foundation and fully 3GPP-compliant. It has a vibrant academic and developer community, with active maintenance and recent releases focusing on Release 16/17 features. Licensed under Apache 2.0, it encourages open contributions. The project held its first World Forum in 2025, highlighting its growing ecosystem.

**Supported Components:**

Implements a full 5G SA core including AMF, SMF, UPF, NRF, PCF, AUSF, UDM, UDR, NSSF, BSF, and SCP.

**SA/NSA Support:**

Primarily supports 5G Standalone (SA) architecture.

**Cloud-Native Readiness:**

Supports Docker, Kubernetes, and Helm charts for flexible deployment.

**Integration with Simulators:**

Well integrated with UERANSIM and supports interoperability with srsRAN and OAI-RAN.

**Use Case Suitability:**

Academic research, PoC deployments, private networks, and experimental testbeds.

**Performance and Scalability:**

Moderate control plane latency and good scalability; known for low resource consumption.

**Community and Activity:**

Active GitHub repository, forum, regular releases, and growing community events.

### 2.2 Open5GS

**Overview and Background:**

Open5GS is a mature open-source project written in C, supporting both 4G EPC and 5G core functions. It has a large community and commercial support options. Licensed under an open-source license, it is widely adopted in academia and industry.

**Supported Components:**

Full 5G SA core including AMF, SMF, UPF, NRF, PCF, AUSF, UDM, UDR, NSSF, BSF, SEPP, and SCP.

**SA/NSA Support:**

Supports both 5G Standalone and Non-Standalone architectures, as well as 4G EPC.

**Cloud-Native Readiness:**

Docker and Kubernetes support with Helm charts; includes web UI for management.

**Integration with Simulators:**

Compatible with UERANSIM, srsRAN, and OAI-RAN.

**Use Case Suitability:**

Production-grade deployments, private networks, academic research, and migration scenarios.

**Performance and Scalability:**

Best-in-class control plane latency; stable with multiple UEs; moderate resource usage.

**Community and Activity:**

Large, active community with frequent updates and comprehensive documentation.

### 2.3 Magma Core

**Overview and Background:**

Originally developed by Meta and now under the Linux Foundation, Magma is designed for carrier-grade LTE and 5G core networks. It emphasizes automation, edge deployment, and scalability. Licensed open source, it has strong industry backing.

**Supported Components:**

Implements LTE EPC and evolving 5G core functions with support for AMF, SMF, UPF, and others.

**SA/NSA Support:**

Supports both 5G Standalone and Non-Standalone.

**Cloud-Native Readiness:**

Containerized, Kubernetes-ready with automation tools.

**Integration with Simulators:**

Compatible with various RAN simulators and hardware.

**Use Case Suitability:**

Telco-grade deployments, rural and edge networks, private 5G.

**Performance and Scalability:**

Demonstrated 550 Mbps downlink on Arm edge devices; optimized for low power and cost.

**Community and Activity:**

Growing community with commercial support and multiple industry partners.

### 2.4 OpenAirInterface (OAI) 5G Core

**Overview and Background:**

Developed by the OpenAirInterface Software Alliance, OAI provides a comprehensive 3GPP-compliant 5G SA core with a focus on research and professional validation. Licensed under OAI Public License, it has strong industry collaborations.

**Supported Components:**

Full SBA core including AMF, SMF, UPF, NRF, PCF, AUSF, UDM, UDR, NSSF, and NEF.

**SA/NSA Support:**

Supports 5G Standalone.

**Cloud-Native Readiness:**

Docker and Kubernetes support; Helm charts available.

**Integration with Simulators:**

Works with OAI-RAN and srsRAN; tested with commercial gNBs.

**Use Case Suitability:**

MEC, edge computing, research, and high-performance deployments.

**Performance and Scalability:**

Highest data plane throughput among open cores; resource intensive.

**Community and Activity:**

Active alliance with commercial backing and professional support.

### 2.5 Aether 5GC (Canonical Charmed SD-Core)

**Overview and Background:**

Part of the Open Networking Foundation’s Aether project, Canonical maintains the Charmed Aether SD-Core, focusing on cloud-native private 5G deployments. It is open source with strong automation and observability.

**Supported Components:**

Implements modular 5G core functions suitable for private networks.

**SA/NSA Support:**
Supports 5G SA.

**Cloud-Native Readiness:**

Fully Kubernetes-native with Juju operator framework.

**Integration with Simulators:**

Integrates with common RAN simulators and testbeds.

**Use Case Suitability:**

Enterprise private 5G, testbeds, and edge deployments.

**Performance and Scalability:**

Optimized for reliability and ease of deployment rather than raw throughput.

**Community and Activity:**

Supported by Canonical and ONF with active documentation.

### 2.6 Canonical Charmed Aether SD Core
**Overview and Background:**

Canonical Charmed Aether SD Core is the enterprise-focused, open-source 5G core developed by Canonical in partnership with the Open Networking Foundation (ONF) as part of the Aether project. It targets private, campus, and industrial 5G deployments, emphasizing automation and ease of use. Actively maintained, it is licensed as open source and integrated into Canonical’s Ubuntu ecosystem.

**Supported Components:**

Implements key 5G core functions (AMF, SMF, UPF, NRF, AUSF, UDM, PCF, etc.) with a modular, microservices-based architecture.

**SA/NSA Support:**

Supports 5G Standalone (SA) deployments.

**Cloud-Native Readiness:**

Fully Kubernetes-native, leveraging Canonical’s Juju operator framework for automated deployment and lifecycle management.

**Integration with Simulators:**

Integrates with UERANSIM, srsRAN, and other common RAN simulators; supports testbed and real-world RAN integrations.

**Use Case Suitability:**

Designed for private enterprise networks, industrial IoT, campus networks, and managed edge deployments.

**Performance and Scalability:**

Optimized for reliability, automation, and observability rather than raw throughput. Scales well for enterprise needs.

**Community and Activity:**

Backed by Canonical and ONF, with active documentation, community support, and regular releases.

2.7 Ella Core
**Overview and Background:**

Ella Core is a lightweight, open-source 5G core purpose-built for private, industrial, and remote deployments. It is designed for simplicity, high performance, and minimal resource usage. The project is actively maintained and welcomes community contributions.

**Supported Components:**

Implements essential 5G SA core functions (AMF, SMF, UPF, NRF, AUSF, UDM, PCF) in a single binary with an embedded database.

**SA/NSA Support:**

Supports 5G Standalone (SA) architecture.

**Cloud-Native Readiness:**

Runs as a single binary on Linux; can be containerized for Docker/Kubernetes deployments.

**Integration with Simulators:**

Integrates with UERANSIM, srsRAN, and other open-source RAN simulators.

**Use Case Suitability:**

Ideal for private 5G in factories, farms, ships, and rapid-deployment scenarios; suitable for SMEs and remote/edge use.

**Performance and Scalability:**

Extremely lightweight—runs on as little as 2 CPU cores and 2GB RAM; supports >3.5 Gbps throughput and <2 ms latency.

**Community and Activity:**

Growing open-source community, active documentation, and responsive support channels.

### 2.8 QCore

**Overview and Background:**

QCore is an experimental, ultra-minimal open-source 5G core written in Rust, targeting highly constrained environments like drones, backpacks, or space. It is in early development and invites collaboration. Licensed under AGPL (main code) and GPL (eBPF), with commercial licenses available.

**Supported Components:**

Implements a monolithic 5G SA core with basic AMF, SMF, UPF functionality; lacks full SBA decomposition and advanced features.

**SA/NSA Support:**

Supports 5G Standalone (SA) only.

**Cloud-Native Readiness:**

Runs as a single process on Linux; can be containerized, but not microservices-based.

**Integration with Simulators:**

Interoperates with OpenAirInterface and srsRAN gNB/UE simulators; quickstart scripts for integration.

**Use Case Suitability:**

Best for research, experimentation, and ultra-lightweight deployments in constrained environments (e.g., drones, edge, space).

**Performance and Scalability:**

Prioritizes minimal resource usage over throughput or scalability; supports a single UE context.

**Community and Activity:**

Small, early-stage project; active GitHub, seeking contributors, and provides test harnesses and documentation.

## 3. Comparative Summary

Here is a comparative matrix of major open-source 5G core network projects as of 2025, based on the most current technical literature, project documentation, and deployment reports:


| Project                        | 3GPP Release Support | Core Components (AMF/SMF/UPF/NRF/etc.) | SA/NSA Support | Cloud-Native (Docker/K8s) | RAN/Simulator Integration        | Performance & Scalability                | Community & Docs        | Use Case Suitability                  | License/Openness         |
|---------------------------------|---------------------|----------------------------------------|---------------|---------------------------|----------------------------------|-----------------------------------------|-------------------------|---------------------------------------|-------------------------|
| **Free5GC**                    | R15+                | Full SBA: AMF, SMF, UPF, NRF, PCF, AUSF, UDM, UDR, NSSF, BSF, SCP | SA (primary), NSA (partial) | Yes (Docker, K8s, Helm)          | UERANSIM, srsRAN, OAI-RAN               | Low resource use, moderate latency      | Active, academic, Linux Fdn | Academic, PoC, private, research      | Apache License 2.0         |
| **Open5GS**                    | R17                 | Full SBA: AMF, SMF, UPF, NRF, PCF, AUSF, UDM, UDR, NSSF, BSF, SCP, SEPP | SA & NSA, 4G EPC           | Yes (Docker, K8s, Helm, WebUI)   | UERANSIM, srsRAN, OAI-RAN, commercial   | Best control plane latency, stable      | Large, active, commercial | Production, private, research         | AGPL-3.0              |
| **Magma Core**                 | Evolving (LTE/5G)   | EPC+5G: AMF, SMF, UPF, others           | SA & NSA, LTE               | Yes (K8s, Docker, automation)     | Various RANs, testbeds                   | 550 Mbps on Arm, telco-grade            | Linux Fdn, industry      | Telco, rural, edge, enterprise         | BSD-style open source license             |
| **OpenAirInterface (OAI) 5GC** | R16                 | Full SBA: AMF, SMF, UPF, NRF, PCF, AUSF, UDM, UDR, NSSF, NEF | SA                        | Yes (Docker, K8s, Helm)          | OAI-RAN, srsRAN, UERANSIM, commercial   | Highest data plane throughput           | Industry, academic         | MEC, edge, research, enterprise        | OAI Public License V1.1      |
| **Aether SD Core**             | R15+                | Modular: AMF, SMF, UPF, NRF, AUSF, UDM, PCF | SA                        | Yes (K8s, Juju, Helm)            | UERANSIM, srsRAN, OAI, testbeds         | Reliable, automated, scalable           | ONF, Canonical, docs        | Private, campus, edge, enterprise      | Apache License 2.0              |
| **Canonical Charmed Aether SD Core** | R15+        | Modular: AMF, SMF, UPF, NRF, AUSF, UDM, PCF | SA                        | Yes (K8s, Juju, Helm)            | UERANSIM, srsRAN, OAI, testbeds         | Reliable, automated, enterprise-ready   | Canonical, ONF, docs           | Private, campus, edge, industrial      | Apache License 2.0              |
| **Ella Core**                  | R15+                | Essential: AMF, SMF, UPF, NRF, AUSF, UDM, PCF | SA                        | Single binary, Docker/K8s option | UERANSIM, srsRAN, OAI                   | >3.5Gbps, <2ms, ultra-lightweight       | Growing, docs, support           | Private, SME, rapid/remote, industrial | Apache License 2.0              |
| **QCore**                      | R15+ (minimal)      | Minimal: AMF, SMF, UPF (monolithic)         | SA                        | Single process, Docker option    | OAI, srsRAN, UERANSIM                    | Ultra-lightweight, single UE, research  | Small, early, docs                | Research, drones, space, constrained   | GNU Affero General Public License |

**Legend:**  
- **SA**: Standalone 5G Core  
- **NSA**: Non-Standalone (with LTE/EPC)  
- **SBA**: Service-Based Architecture  
- **K8s**: Kubernetes  
- **PoC**: Proof of Concept  
- **SME**: Small/Medium Enterprise

### Notes:
- **Academic Research/Testbeds:**
    <br>Free5GC, OpenAirInterface, Open5GS (for dual-mode)

- **PoC/Experimental Networks:**
    <br>Free5GC, Ella Core, Charmed Aether SD-Core, QCore (for constrained/novel use)

- **Enterprise Private 5G:**
    <br>Open5GS, Ella Core, Charmed Aether SD-Core, Magma Core

- **Telco-Grade Deployments:**
    <br>Magma Core, OpenAirInterface (with pro support)

- **Integration with RAN Simulators:**
    <br>Free5GC, Open5GS, QCore (for srsRAN/OAI), srsRAN (RAN side)

- **Ultra-Constrained/Novel Environments:**
    <br>QCore (drones, space), Ella Core (lightweight, rapid deploy)

### Key Differentiators:
- **Ella Core**: eBPF datapath technology, minimalist approach

- **Canonical** Charmed Aether SD Core: Operator-based deployment with good dashboards

- **Aether** SD-Core: Enterprise-grade with comprehensive monitoring and cloud-native architecture

- **Magma**: Production-grade with flexible deployment options

- **OAI**: Comprehensive NF support with own RAN solution

- **Free5GC**: Developer-friendly with strong community and resources

- **Open5GS**: Most comprehensive feature set including IMS, SMS, and roaming support

- **QCore**: The world's most lightweight 5G Core (probably)



## 4. Conclusion
Open-source 5G cores are pivotal for innovation, education, and democratizing mobile network technology. With diverse projects addressing different needs—from lightweight research platforms to carrier-grade deployments—developers and researchers have a rich ecosystem to explore. Getting involved is as easy as contributing to GitHub repos, participating in forums (e.g., free5GC forum, Open5GS community), or joining project-specific events.

The future of 5G and beyond will be shaped by these collaborative efforts, accelerating the deployment of next-generation networks worldwide.

### References and Resources:

This article reflects the state of open-source 5G core networks as of mid-2025, consolidating community insights, academic research, and industry deployments.

- https://free5gc.org/forum/

- https://thesis.unipd.it/retrieve/9c877408-954d-488d-ab86-4e8bdfb4131c/Hosseinishamoushaki_Seyedali.pdf

- https://open5gs.org/open5gs/docs/guide/01-quickstart/

- https://www.computerweekly.com/news/366621701/SRS-deploys-srsRAN-enterprise-5G-at-innovation-hub

- https://www.prweb.com/releases/connect-5g-and-xtreme5g-collaborate-on-industry-first-edge-5g-stand-alone-magma-evolved-packet-core-built-on-arm-816545442.html

- https://arxiv.org/html/2505.14501v1

- https://researchspace.csir.co.za/server/api/core/bitstreams/09c11bd7-3e9e-45f8-bbf3-07b181bfd0e0/content

- https://magma.github.io/magma/docs/howtos/5g_nsa_support

- https://intelliot.eu/wp-content/uploads/2022/09/Deliverable-D4.2-5G-Network-Functionalities-1.pdf

- https://lf-aether.atlassian.net/wiki/spaces/HOME/pages/6160406/Research

- https://www.themoonlight.io/en/review/open-source-5g-core-platforms-a-low-cost-solution-and-performance-evaluation

- https://arxiv.org/html/2412.21162v1

- https://www.startus-insights.com/innovators-guide/5g-trends/

- https://www.open6gcore.org

- https://www.businesswire.com/news/home/20250610766552/en/PAWR-Platform-ARA-Debuts-Open-Source-5G-Core-Integrated-With-Commercial-RAN

- https://free5gc.org

- https://openairinterface.org/oai-5g-core-network-project/

- https://www.nist.gov/programs-projects/5g-core-networks-testbed

- https://arxiv.org/pdf/2412.21162.pdf

- https://github.com/free5gc/free5gc

- https://free5gc.org/blog/

- https://www.linuxfoundation.org/press/worlds-leading-open-source-mobile-packet-core-free5gc-moves-under-linux-foundation-to-provide-open-source-alternatives-across-5g-deployments

- https://arxiv.org/html/2502.02842v1

- https://www.fbcinc.com/e/nlit/agenda.aspx

- https://www.mdpi.com/2076-3417/14/16/7018

- https://www.linuxfoundation.org/blog/blog/how-open-source-communities-are-driving-5gs-future-even-within-a-large-government-like-the-us

- https://www.ns2project.com/5g-open-source-project/

- https://github.com/calee0219/awesome-5g/blob/main/README.md

- https://www.youtube.com/watch?v=Km4U81O3AIs

- https://www.snstelecom.com/private5g

- https://gomomentum.com/7-trends-that-will-define-telecommunications-in-2025/

- https://www.capgemini.com/insights/expert-perspectives/whats-next-for-telecoms-7-key-trends-and-takeaways-from-mwc-2025/

- https://www.startus-insights.com/innovators-guide/5g-market/

- https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/Open-Air-Interface-Roadmaps/diff?version_id=085cfcfd13cbca12f44a3ae2e959bf5aa0b7df61

- https://opennetworking.org/news-and-events/blog/aether-refactored-for-scalable-customizable-private-5g-deployments/

- https://www.opencompute.org/events/past-events/2024-ocp-global-summit

- https://www.ericsson.com/en/core-network/5g-core

- https://www.redhat.com/en/blog/5g-core-observability-edge

- https://www.cse.iitb.ac.in/~mythili/research/papers/2025-5gcore-k8s.pdf

- https://www.ieeetoronto.ca/2024/12/04/impact-of-open-source-5g-projects/

- https://github.com/zanattabruno/5G_OAI-Free5GC

- https://www.thebusinessresearchcompany.com/report/5g-core-global-market-report

- https://www.linkedin.com/pulse/5g-technology-market-outlook-2025-key-growth-drivers-nowcf