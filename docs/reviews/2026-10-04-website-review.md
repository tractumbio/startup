# Tractum Bio: website review and improvement plan

Prepared for Adrian Cioanca · 4 October 2026

## 1. Executive assessment

Tractum Bio has a credible specialist proposition: combine retinal science, translational judgement and analytical implementation to help biotech companies make development decisions and CROs build useful capabilities. The website should make that combination concrete.

The current site promises more breadth than it demonstrates. Strong credentials are present, but the buyer cannot easily inspect past work, understand the first paid deliverable, or distinguish personal delivery from work coordinated through specialists. Speculative valuation graphics make that problem worse.

The recommended direction is a focused, evidence-led specialist practice with two clear service routes. Fix the mobile contact defect, define the initial engagement, replace ambiguous statistics, and add project evidence before investing heavily in decoration.

### Review scope and evidence labels

Reviewed the supplied `index.html`, `asset.html`, `capability.html`, `styles.css` and `site.js`. Checked internal link destinations and anchors, inspected responsive rules, and calculated selected colour contrasts. External research is linked below.

- **Confirmed:** directly supported by the supplied source code or an identified external source.
- **Recommendation:** editorial, commercial or implementation judgement; not a measured conversion result.
- **Owner evidence required:** cannot responsibly be established from general market research.
- **Proposed offer:** a service design suggestion, not a commitment already made by Tractum Bio.

This was not a browser-rendered usability audit. Actual line wrapping, screenshots, page performance, screen-reader behaviour and mobile interactions still need testing. No website files were changed or deployed. This document contains the complete review and research; external source documents are linked rather than bundled.

## 2. Prioritised backlog

| Priority | Change | Why it matters | Completion criterion |
|---|---|---|---|
| P0 | Repair phone CTA labels | Both labels are hidden at small widths | A visible, meaningful label at 320–420px |
| P0 | Replace misleading statistical presentation | Scientific buyers scrutinise evidence | Each retained figure has a scope, date, currency where relevant, and source |
| P0 | Remove unsupported valuation uplift | An illustrative number is not evidence of client impact | No uplift claim without a transparent worked model |
| P0 | Match booking labels to actual behaviour | Current booking buttons open email | Scheduling works, or wording explicitly says email |
| P1 | Define the first paid engagement | Buyers need to understand the purchase | Inputs, outputs, timing, boundaries and price basis stated |
| P1 | Add two substantiated case studies | Credentials do not demonstrate every offered service | Role, deliverable and evidence clearly attributed |
| P1 | Restore mobile navigation | Main links disappear below 900px | Both service routes remain reachable in the header |
| P1 | Narrow absolute CRO promises | Broad assurances invite scepticism | Supported scope and acceptance criteria described |
| P1 | Fix HTML structure and contrast | Reliability and readability | One document shell; required colour pairs pass checks |
| P2 | Shorten biography and add portrait | Improve trust and scanning | Short homepage bio, fuller About content |
| P2 | Improve metadata and measure enquiries | Better sharing and informed iteration | Accurate previews; defined conversion events |

## 3. Positioning and homepage

### Replace the opening line

Current: “The eye, judged by someone who has worked every side of it.”

Problems: it does not clearly identify the service, “judged” sounds unnatural here, and “every side” implies a breadth of experience that the page does not substantiate.

**Recommended balanced homepage copy:**

> Ophthalmic development decisions. Practical capability for the labs behind them.
>
> Tractum Bio helps biotechs assess ophthalmic opportunities and helps CROs build the studies, analytics and workflows to support them.

If biotech assessment is the main commercial priority, use the more direct headline on the homepage as well as the biotech page:

> Assess your candidate’s potential in ophthalmology before committing to development.

Use two explicit routes underneath:

| Audience | Card heading | Supporting message | Action |
|---|---|---|---|
| Biotech | Assess an ophthalmic opportunity | Evaluate indication fit, development barriers and the evidence needed for the next decision | Explore asset assessment |
| CRO | Build ophthalmic and analytical capabilities | Develop workflows on your infrastructure and transfer them to your team | Explore capability builds |

Avoid allowing general automation to overwhelm the ophthalmic specialism. Keep cross-therapeutic analytics as a defined service on the CRO page rather than making the homepage resemble a general technology consultancy.

### Recommended homepage order

1. Specific proposition and two service routes.
2. Compact, verifiable founder credentials.
3. One evidence-backed example for each audience.
4. What the initial engagement delivers.
5. Optional, concise market context.
6. Short founder introduction and portrait.
7. Contact action with a clear next step.

Market size is context, not proof that a visitor should hire Tractum Bio. Put actual work and deliverables ahead of the market narrative.

## 4. Research-backed replacements for numerical claims

### 4.1 Clinical development success: correct the comparison

**Verified:** BIO/Informa/QLS’s February 2021 report, using 2011–2020 data, reports Phase I-to-FDA-approval likelihood of **11.9% for ophthalmology**, compared with **7.9% across indications**. Figures 5a–5b, printed pages 10–11, support the comparison. [S1]

The current homepage identifies 7.9% as an overall baseline, while the asset page places it beside “odds favour the eye.” Replace that ambiguity with both values and the historical period.

**Proposed website copy:**

> 11.9% vs 7.9% — historical approval likelihood from Phase I: ophthalmology versus all indications, 2011–2020.

**Nearby qualification:**

> Historical industry comparison, not a forecast for an individual candidate.

Do not present this as a 2026 success rate, a preclinical probability, or evidence that repurposing itself improves approval chances. The report estimates likelihood by compounding phase-transition rates; its tabulated n values are transitions, not a simple cohort of unique drugs followed to approval. Prefer “above the overall average” to a vague ranking claim.

### 4.2 Ophthalmic drug market: replace the unexplained range

**Verified publisher estimate:** Mordor Intelligence’s public report gives **US$37.49 billion for 2025** and **US$40.58 billion for 2026**, for the global ophthalmic drugs market. The page identifies its proprietary estimation framework and a January 2026 data update. [S2]

**Recommended short card:**

> US$37.5B — estimated global ophthalmic drugs market in 2025. Source: Mordor Intelligence.

Alternatively use the 2026 estimate, explicitly labelled as such. Do not combine forecasts from different publishers into the current US$20–40B range. Remove the unexplained “retina-weighted” description. This market includes more than retinal therapeutics and is not Tractum Bio’s consulting addressable market.

This is a commercial research estimate, not audited industry revenue. The public page was reviewed; its underlying paid model was not independently validated. The original MarketsandMarkets attribution was not tied to a specific matching report in this review and should be removed unless that report is supplied.

### 4.3 EyeBio transaction: separate cash from milestones

**Verified:** Merck’s 29 May 2024 announcement specified **US$1.3 billion upfront** and **up to US$1.7 billion in contingent milestone payments**, for a maximum potential **US$3 billion**. A separate Merck release confirms completion of the acquisition. [S3, S4]

**Proposed website copy:**

> Merck acquired EyeBio in 2024 under terms including US$1.3B upfront and up to US$1.7B in milestones.

Use this as a labelled transaction example. Do not describe the maximum as cash already paid, imply that it values a typical early-stage asset, or imply Tractum Bio participated.

Replace “pharma is buying ophthalmic assets, not building them” with a narrower editorial statement: “Strategic acquisitions are one route through which pharmaceutical companies expand their ophthalmic pipelines.”

### 4.4 Remove the unsupported +76% valuation graphic

The arithmetic from US$85M to US$150M is approximately 76.5%. That does not establish either valuation or connect the uplift to Tractum Bio’s work.

**Action:** remove “+76%”, “$85M→$150M” and the +30/+76/+140% range from the sales page. External research cannot validate hypothetical client-specific values without the actual model.

If a demonstration is later added, label it prominently as hypothetical and show indication, modality, stage, geography, commercial assumptions, costs, timing, probabilities, discounting and sensitivities. Explain what is enterprise value versus asset value. Keep this separate from realised client outcomes.

Replace the entire outcome panel with tangible outputs: decision memo, prioritised evidence gaps, study plan and assumptions register. Also remove “5→1” unless the five questions are explicitly defined.

## 5. Make the biotech engagement purchasable

The current tracks list activities but leave the buyer uncertain about deliverables, timing and decisions. Rename and structure them around outputs.

### Proposed initial offer: ophthalmic opportunity assessment

| Component | Proposed scope |
|---|---|
| Intended client | A biotech with a defined candidate or mechanism considering an ophthalmic indication |
| Inputs | Non-confidential summary initially; agreed access to relevant scientific data after confidentiality arrangements |
| Work | Mechanism-to-indication mapping, literature assessment, delivery and exposure questions, differentiation and development-gap review |
| Deliverables | Indication shortlist, evidence matrix, risk register, recommendation memo and readout meeting |
| Decision | Proceed, pause pending specified evidence, or stop |
| Commercial basis | Fixed scope and fee agreed before starting |
| Timing | Publish an achievable range only after checking effort, availability and data dependencies |
| Boundaries | No experimental results, formal patent opinion or guaranteed regulatory outcome implied |

This is a proposed service specification. Confirm it before publication. Do not invent a standard fee or promise a two-week turnaround just to fill a gap.

### Make the decision gate explicit

Use: **Assess → decision gate → design evidence programme → optional execution support.**

At the gate, consider mechanism relevance, ocular exposure feasibility, safety uncertainty, meaningful differentiation and whether the key uncertainty can be tested within the sponsor’s budget. Set candidate-specific thresholds in the engagement; do not pretend a universal score makes the decision objective.

Describe later-stage outputs separately: prioritised studies, endpoints, acceptance criteria, CRO brief, dependencies, budget assumptions and decision milestones. Clarify whether Tractum Bio designs, coordinates, executes or reviews each component.

### Clarify specialist responsibilities

- Replace “FTO scan” with “preliminary patent landscape review; formal freedom-to-operate assessment through a qualified patent adviser,” if that reflects the delivery model.
- Explain what “IP strategy + filing support” includes and who handles specialist advice and filings.
- Replace broad “IND-ready” wording with the exact evidence-planning or coordination scope you can deliver. Do not imply a complete submission package if that is not the service.
- Replace “most assets should stop at the gate” with “an early no-go can be a valuable result.” The former asserts an unsupported proportion.

## 6. Strengthen the CRO proposition

Keep the useful promise: work on the client’s infrastructure, then transfer usable capability to its team. Separate scientific capability builds from analytical workflow builds so the buyer can purchase either.

| Current claim | Concern | Recommended wording or action |
|---|---|---|
| Any instrument, assay or image format | Implies universal integration | Supported instruments and formats agreed during scoping |
| No new hire | Staffing needs vary | Reduce reliance on permanent specialist hiring |
| Systems are untouched | Integration may require changes | Build around existing systems, with changes agreed upfront |
| Fully auditable | Undefined assurance | Describe records, versions, lineage and approvals retained |
| Deterministic | Not every analytical workflow is inherently deterministic | Specify versions, seeds and reproducibility controls where applicable |
| Validated against your QMS | Validation scope is unspecified | Define the client-agreed qualification or validation activities and sign-off |
| I will never compete for a sponsor | Too broad, particularly alongside biotech advisory | Explain sponsor ownership, confidentiality and conflict handling |
| Most analytics vendors have only sat at the computer | Unsupported competitor claim | Explain your bench, analytical and sponsor-facing experience directly |

For each listed disease area, distinguish hands-on experience, transferable expertise and delivery through partners. A retinal background does not automatically substantiate glaucoma, dry-eye and every ocular-safety capability.

### Proposed delivery and handover package

- Agreed workflow and supported input specification.
- Pilot using representative client data or an agreed study.
- Documented methods, software versions and configuration.
- Defined QC checks and scientist approval points.
- Acceptance results against the agreed test cases.
- SOPs, training and operating responsibilities.
- Ownership or licence terms for code and methods.
- Support period, maintenance needs and change process.

Sell the resulting operational capability. Avoid unsupported claims about increased sales or turnaround until measured.

## 7. Evidence the owner must supply

General web research can supply industry context. It cannot establish confidential delivery results, permission to name clients, or the founder’s precise role in a project.

| Claim or asset | Evidence needed | Publication treatment |
|---|---|---|
| Publication count, citations, h-index | Dated profile and counting basis | Link the profile; date dynamic metrics or omit them |
| Awards | Official award record | Use the exact award name and scope |
| Patents | Publication numbers, status, inventorship | Distinguish applications, grants and patent families |
| Capital raised | Accurate currency, funding type and attributable role | Separate grants from investment; avoid implying personal sole responsibility |
| Global pharma model work | Project records and disclosure permission | Identify personal contribution; anonymise if necessary |
| Automation performance | Comparable before/after timings and quality checks | State workload and denominator |
| Testimonials | Genuine statements and consent | Never manufacture endorsements |
| Founder portrait | Suitable original photo and usage rights | Prefer a real portrait to the oversized logo |

### Case study template

Use this twice: once for an ophthalmic capability, once for analytics or workflow automation.

1. **Context:** client type and problem, with permitted detail.
2. **Starting point:** existing capabilities and constraints.
3. **Your role:** precisely what you personally owned.
4. **Work delivered:** model, analysis, code, method, SOP or training.
5. **Evidence:** approved output or substantiated result.
6. **Limitations:** project scope and anything not established.

A useful case study can be qualitative. Do not fabricate percentages to make it appear commercial. Label independent worked examples as demonstrations, and label work completed in prior roles accordingly.

## 8. Biography, design and page structure

The founder biography is repeated on the homepage and biotech page. Shorten the homepage version to roughly 80–120 words with three or four relevant credentials. Keep the fuller story on an About page or expanded section.

Prioritise retinal research, translational work, the biotech founder role, and relevant analytics delivery. Teaching cohort sizes and outreach attendance are secondary to the buyer’s purchasing decision. Replace “the science is rarely the bottleneck” with a defensible point about framing development questions and sequencing evidence.

Use a real portrait beside the short biography. Retain the logo in navigation and footer. Add a sample deliverable or approved project image before adding decorative imagery. Do not use generic laboratory photographs to imply ownership of facilities.

Keep terminology consistent: “For biotech” and “For CROs” in global navigation; page-specific anchors underneath if needed. Move detailed evidence to accessible expandable sections or supporting pages without hiding critical qualifications.

In mobile testing, pay particular attention to the lens diagram and the ownership-stack diagram. SVG text shrinks with the whole graphic; larger internal font sizes do not automatically make it legible. Consider an HTML list on narrow screens.

## 9. Technical fixes

### 9.1 Confirmed mobile CTA cascade defect

In `styles.css`, the small-screen rule sets `.nav-cta .cta-short` to `display:inline`, but a later equal-specificity rule sets it to `display:none`. At widths at or below 420px, the long label is also hidden.

Move the default before the override:

```css
.nav-cta .cta-short { display: none; }

@media (max-width: 420px) {
  .nav-cta .cta-long { display: none; }
  .nav-cta .cta-short { display: inline; }
}
```

Delete the conflicting later rule. Check both visual text and the link’s accessible name.

### 9.2 Mobile navigation

`nav.links` disappears below 900px without a replacement. Add an accessible menu button and panel, or retain a compact always-visible service navigation. If using a toggle, implement `aria-expanded`, a labelled controlled region, sensible focus behaviour and Escape-to-close. Ensure navigation remains available if JavaScript fails.

### 9.3 Document structure

`index.html` contains an outer document wrapper surrounding another complete HTML document. Retain one doctype, one `html lang="en"`, one head and one body. Preserve needed safe-area behaviour without retaining the redundant wrapper or conflicting theme declaration.

### 9.4 Contrast

Calculated from the CSS hex values against white text:

| Button background | Approximate contrast | Assessment for normal-size text |
|---|---:|---|
| Light-theme blue `#2463A7` | 6.14:1 | Passes 4.5:1 target |
| Light-theme teal `#2B8C86` | 4.04:1 | Below target |
| Dark-theme blue `#5E9BDD` | 2.91:1 | Below target |
| Dark-theme teal `#4FB3AC` | 2.51:1 | Below target |

WCAG 2.2 SC 1.4.3 specifies 4.5:1 for normal text, with a 3:1 threshold for qualifying large text. The relevant button labels are normal-size text. [S5]

Separate filled-button colour tokens from link colours. A brighter link on a dark background can work while the same colour behind white button text fails. Check hover, focus and disabled states as well. This is a targeted contrast finding, not a full accessibility certification.

### 9.5 Contact and anchors

All booking calls to action currently use `mailto:`. Either add a working scheduling flow or change the label to “Email to arrange an intro call.” Keep a visible, selectable email address near every main contact action. State the meeting length and what to send initially, without requesting confidential datasets by default.

Allow for the sticky header:

```css
main section[id] { scroll-margin-top: 6rem; }
```

Adjust the offset after checking actual header height. Internal link and anchor checks found no missing targets in the supplied files.

### 9.6 Animation resilience

The script adds the `js` class, and `.js .reveal` hides content until observed. Existing fallbacks handle missing IntersectionObserver and an initial reduced-motion preference. Make essential content visible by default or ensure initialization failures cannot leave it hidden. Check tall sections, in-page anchor jumps and keyboard focus with reveal animations enabled.

### 9.7 Metadata and maintenance

Add a favicon, page-specific Open Graph metadata, a suitable sharing image, and canonical URLs once the production domain is confirmed. Retain accurate titles and descriptions. Add a sitemap once public routes are final. Use structured data only for factual organisation and person details; do not invent ratings or reviews.

The CRO footer currently carries market and valuation references that are not central to that page. Use page-specific references and concise scope language. Remove the claim that valuation inputs are visible if no model is provided.

## 10. Conversion and measurement

Use one primary next step per page. The homepage routes visitors; the service pages explain a purchase; contact completes the journey.

If collecting enquiries through a form, start with company, service interest, development stage or capability gap, and preferred contact. Explain the initial conversation and offer confidentiality arrangements before detailed data exchange. Any tracking should avoid confidential asset details in URLs or event properties.

Measure distinct stages rather than treating clicks as revenue:

| Stage | Suggested measure |
|---|---|
| Audience selection | Visits to each service route |
| Contact intent | Email or scheduling action clicks |
| Enquiry | Completed contact or booking |
| Qualification | Enquiries that match the intended service |
| Commercial result | Scopes proposed and engagements agreed |

These are proposed measures; the supplied site has no demonstrated conversion baseline. Establish a baseline before setting improvement targets. A mailto click is not proof that an email was sent.

## 11. Implementation sequence and acceptance checklist

### First pass: accuracy and usability

- [ ] Fix the mobile CTA rule order.
- [ ] Provide mobile navigation.
- [ ] Remove duplicate homepage document wrappers.
- [ ] Correct the clinical-success comparison and add dated sources.
- [ ] Replace the market range with one attributed estimate.
- [ ] Distinguish upfront transaction value from milestones.
- [ ] Remove unsupported valuation uplift and unexplained outcome numbers.
- [ ] Align booking labels with actual behaviour.
- [ ] Fix button contrast and sticky-header anchor offsets.

### Second pass: offer and proof

- [ ] Confirm the first paid offer, deliverables and exclusions.
- [ ] Set an achievable timeframe and fee basis.
- [ ] State personal versus partner responsibilities.
- [ ] Add two approved case studies or clearly labelled demonstrations.
- [ ] Add selected publication, patent and professional-profile links.
- [ ] Replace the oversized founder logo with an appropriate portrait.
- [ ] Shorten the biography and tighten absolute claims.

### Third pass: launch verification

- [ ] Check 320, 375, 390, 420, 768, 900 and 1440px layouts.
- [ ] Check light and dark themes, keyboard operation, reduced motion and 200% zoom.
- [ ] Confirm no horizontal overflow or unreadable diagram labels.
- [ ] Verify visible focus, heading hierarchy and accessible menu names.
- [ ] Test every CTA on a phone and desktop.
- [ ] Confirm contact delivery and response ownership.
- [ ] Test representative pages with JavaScript disabled.
- [ ] Confirm metadata and social previews against the real domain.
- [ ] Record the evidence owner and review date for every quantitative claim.

## 12. Source register

Sources accessed 4 October 2026. Dollar figures in the external market and transaction sources are US dollars. Links may be updated by their publishers; retain the period and scope in any website citation.

| ID | Source | Use in this review |
|---|---|---|
| S1 | BIO, Informa Pharma Intelligence and QLS Advisors, *Clinical Development Success Rates and Contributing Factors 2011–2020*, February 2021. [Official PDF](https://go.bio.org/rs/490-EHZ-999/images/ClinicalDevelopmentSuccessRates2011_2020.pdf). [Publisher landing page](https://www.bio.org/clinical-development-success-rates-and-contributing-factors-2011-2020). | Historical approval comparison; Figures 5a–5b |
| S2 | Mordor Intelligence, *Ophthalmic Drugs Market Size and Share*, public 2026–2031 report page. [Report page](https://www.mordorintelligence.com/industry-reports/global-opthalmic-drugs-market). | Attributed commercial market estimates |
| S3 | Merck, *Merck to Acquire EyeBio*, 29 May 2024. [Announcement](https://www.merck.com/news/merck-to-acquire-eyebio/). | Announced upfront and contingent consideration |
| S4 | Merck, *Merck Completes Acquisition of EyeBio*. [Completion announcement](https://www.merck.com/news/merck-completes-acquisition-of-eyebio/). | Confirmation that the transaction completed |
| S5 | W3C WAI, *Understanding Success Criterion 1.4.3: Contrast (Minimum)*. [Guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). | Text contrast thresholds |

### Evidence still unresolved

No external source establishes Tractum Bio’s valuation uplift, client revenue impact, standard fees, delivery speed, current bibliometrics, or specific project results. Those require owner records or should be omitted. The historical success dataset was verified because it is the report cited by the site; it is not represented here as the latest available industry study. Market estimates and large transactions support context, not a promise of commercial or scientific success.
