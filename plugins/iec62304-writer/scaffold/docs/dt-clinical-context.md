<!--
  Narrative sections inlined into the deliverables by the exporters.
  Each `## <anchor>` below is a section the exporters look up by its slug;
  any other H2 is ignored. Everything in this file is EXPORTED: present
  tense, no dates, no `[TODO`/`[DRAFT`/`[GAP-` markers, no commit hashes,
  no competitor names. A remark you want to keep goes in an HTML comment
  like this one — the exporters strip it.

  The six sections below are REQUIRED by the SDD export (store lint SL-6).
  The architecture-writer fills the first three and drafts the four
  security views from the code; the security-analyst completes the views;
  a human reviews all six. Leave a section empty rather than invent.

  Other anchors the exporters recognise (optional, add them as `## <slug>`
  when the product needs them): document-overview, abbreviations,
  glossary, intended-use, warnings-and-precautions, connected-devices,
  personnel-and-training, packaging, end-users,
  characteristics-affecting-safety, hardware-and-software-requirements,
  processing-workflow, application-workflow, class-diagram, cots-control,
  test-environment-overview, tests-identification-strategy, tests-schedule,
  qualification, test-preparation-data, test-preparation-environment,
  test-preparation-tools, automated-tests-platform, local-tests-platforms.
  A section may also be supplied from a QMS-managed file through
  `dt-config.yaml: external_resources`.
-->

<!-- REQUIRED (SDD). The component diagram (Mermaid) and one paragraph per component: what it does, what it talks to. -->
## general-system-architecture

<!-- REQUIRED (SDD). The state machine of the software — idle, receiving, processing, exporting, error, maintenance — with entry and exit conditions and what is observable in each state. -->
## run-states

<!-- REQUIRED (SDD). Why the architecture is what it is. The module-level `## Design notes` roll up here; alternatives discarded; no dates. -->
## architecture-rationale

<!-- REQUIRED (SDD; FDA premarket cybersecurity guidance, global system view). One diagram with every network interface, port and protocol, every trust boundary and authentication point, each data store with its protection at rest and in transit, where secrets live. One paragraph per boundary. -->
## security-global-view

<!-- REQUIRED (SDD; multi-patient harm view). How one patient's data and results are isolated from another's on the same instance: session scope, identifiers, storage separation, cleanup, what a cross-patient failure would look like. -->
## security-multi-patient-view

<!-- REQUIRED (SDD; updateability / patchability view). How software and OTS updates are delivered, authenticated (signature), applied and rolled back; who can trigger one; device behaviour during an update; OTS end-of-life handling. -->
## security-updateability-view

<!-- REQUIRED (SDD; security use-case views). One diagram per security-relevant use case — ingest, export, administer, update, support access — showing the actors, the data crossing each boundary and the control that protects the crossing. -->
## security-use-case-views
