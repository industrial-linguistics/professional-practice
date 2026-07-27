# KDP Publication Pack

Status: **local release candidate; do not publish until the external gates below are closed**

Last checked against KDP documentation: 27 July 2026.

## Files to upload

### Paperback

- Interior: `textbook/main-amazon.pdf`
- Cover: `textbook/kdp/paperback-cover.pdf`
- Format: paperback
- Ink and paper: black ink on white paper
- Trim: 6 x 9 inches
- Bleed: no interior bleed
- Cover finish: matte
- Reading direction: left to right

The full-wrap cover is generated from the final interior page count. Rebuild
the complete release after any pagination change; do not reuse an older cover.
Leave KDP's automatic barcode enabled because the cover already reserves a
clear white barcode area.

### Kindle

- Manuscript: `textbook/it-professional-practice.epub`
- Marketing cover: `textbook/kdp/ebook-cover.jpg`
- Format: reflowable EPUB 3
- Language: English (Australia)

Do not upload the print PDF as the Kindle manuscript. The EPUB has reflowable
text, navigation, linked citations and text alternatives for its figures.

## Canonical metadata

- Title: **IT Professional Practice**
- Subtitle: **How Digital Services Are Operated, Improved, Bought and Governed**
- Author: **Greg Baker**
- Edition: **First edition**
- Publisher/imprint: **Industrial Linguistics**
- Publication year: **2026**
- Primary marketplace: **Amazon.com.au**
- Rights: **Worldwide rights**, provided the author confirms ownership of every
  included source image and the final review records
- Adult content: **No**
- Low-content book: **No**
- Large print: **No**

The title, subtitle, author and imprint must remain identical in the KDP form,
cover, interior and ISBN record. Rebuild after changing any of them.

## Product description

Code is only one part of a dependable digital service.

IT Professional Practice connects the work technical people are expected to
understand but are rarely taught together: service management, delivery
performance, incident learning, technology sales, vendor control,
small-organisation IT, open source and data authority.

Through workplace cases, practical artefacts and decision exercises, readers
learn how to:

- turn user promises into measurable service commitments;
- connect tickets, changes, releases and continual improvement;
- use DORA and reliability evidence without gaming the numbers;
- run incident reviews that lead to owned corrective action;
- test commercial promises against operational reality;
- choose proportionate controls for small and growing organisations;
- reason about open licensing, Indigenous data sovereignty and authority; and
- defend a service design under technical, commercial and governance
  questions.

Written for students and early-career practitioners, the book explains how the
parts of a digital service fit together and gives readers concrete ways to
participate in the decisions around them.

## Search terms

Use one phrase in each of KDP's seven keyword fields:

1. IT professional practice
2. IT service management
3. DevOps and DORA metrics
4. incident response postmortems
5. technology vendor management
6. small business IT strategy
7. Indigenous data sovereignty

Select up to three accurate categories available for the Australian primary
marketplace. Prefer the closest current equivalents of:

1. information technology or IT service management;
2. software development, DevOps or project management; and
3. business information management.

Do not select an unrelated low-competition category. KDP's category names can
change, so the live category chooser is authoritative.

## ISBN decision

The Kindle edition does not need an ISBN. The paperback does.

Preferred option: obtain an Australian ISBN for the paperback, register the
metadata exactly as written above and use **Industrial Linguistics** as the
imprint. This preserves the publisher identity and allows the same ISBN to be
used for the same paperback edition outside KDP.

Fast option: use KDP's free paperback ISBN. It can only be used through KDP and
the imprint will appear as **Independently published**, not Industrial
Linguistics. If this option is chosen, remove the publisher name from places
where it would misleadingly imply that it is the registered ISBN imprint.

Never insert an ISBN placeholder. Enter the assigned ISBN in
`content/textbook-metadata.json` and rebuild the release so the copyright page,
PDF metadata and KDP form agree.

## Pricing recommendation

Initial list prices:

| Edition | Australia | United States |
| --- | ---: | ---: |
| Paperback | A$39.99 | US$24.99 |
| Kindle | A$14.99 | US$9.99 |

At 378 pages, the current KDP black-ink regular-trim formula gives an estimated
printing cost of A$10.74 in Australia and US$5.54 in the United States. At the
recommended paperback prices, the estimated Amazon-marketplace royalties are
about A$13.26 and US$9.46 per copy before any applicable withholding or other
adjustments.

The Kindle build is kept below 3 MB to reduce delivery charges under the 70%
royalty option. Select 70% where eligible. The recommended eBook price remains
at least 20% below the corresponding print price. Verify every currency and
royalty in KDP's live pricing screen before publishing.

Do not enrol the eBook in KDP Select initially. Select requires digital
exclusivity and would prevent selling or distributing the EPUB through other
stores during the enrolment period. Reconsider it only as a deliberate
Amazon-exclusive marketing decision.

## AI-content disclosure

KDP requires disclosure of AI-generated text, images or translations even
after substantial human editing. For this edition, disclose:

- AI-generated text: **Yes**
- AI-generated images: **Yes**
- AI-generated translations: **No**

Use the most accurate scope options offered by the live KDP form. This is an
account disclosure, not wording to add to the copyright page. The author
remains responsible for rights, factual checks and reader experience.

## Release gates

The local files are not authority to press Publish. Close these gates in order:

1. Complete the two reviews in
   `docs/indigenous-content-publication-review.md`, record the reviewers and
   dispositions, and apply any required manuscript changes.
2. Confirm rights for all four interior images and the cover design.
3. Choose and assign the paperback ISBN, then run
   `python3 scripts/build_textbook_release.py`.
4. Open the final EPUB in Kindle Previewer. Check phone, tablet and e-reader
   modes; the table of contents; all four figures at large text; citations;
   chapter breaks; and the final references.
5. Create linked Kindle and paperback drafts in KDP using the identical
   metadata above. Upload the final release files and complete the AI
   disclosure.
6. Pass KDP Print Previewer with no unresolved errors. Inspect the trim,
   margins, spine, barcode area, fine lines and every illustrated page.
7. Approve the print preview and order a physical proof. Check cover colour and
   centring, spine position, text size, gutter comfort, image legibility,
   references and index. Record corrections and rebuild if necessary.
8. Have a human proofreader perform a final typo pass on the proof or final
   rendered files.
9. Recheck live prices and territories, then publish the linked editions.

## Local release command

From the repository root:

```bash
python3 scripts/build_textbook_release.py
```

The final automated result is written to
`textbook/audit/release-checks.txt`. A passing local report does not close the
external review, ISBN, Kindle Previewer, KDP Previewer, proof-copy or
account-disclosure gates.

## KDP sources

- [Paperback printing costs](https://kdp.amazon.com/en_US/help/topic/G201834340)
- [Paperback royalties](https://kdp.amazon.com/en_US/help/topic/G201834330)
- [Digital book pricing and delivery costs](https://kdp.amazon.com/en_US/help/topic/G200634500)
- [eBook list-price requirements](https://kdp.amazon.com/en_US/help/topic/G200634560)
- [ISBN and imprint options](https://kdp.amazon.com/en_US/help/topic/G201834170)
- [eBook cover specifications](https://kdp.amazon.com/en_US/help/topic/G200645690)
- [KDP AI-content guidelines](https://kdp.amazon.com/en_US/help/topic/G200672390)
- [Upload and preview book content](https://kdp.amazon.com/en_US/help/topic/G200641240)
- [Order a proof copy](https://kdp.amazon.com/en_US/help/topic/GVEG4YA9G2T7N6DR)
