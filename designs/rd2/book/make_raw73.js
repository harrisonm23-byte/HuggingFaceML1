// The 73 chats exactly as quoted in the court record: no markings, no edits (RD2, 16 Oct 2026)
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Footer, PageNumber } = require("docx");
const [, , IN, OUT] = process.argv;
const chats = JSON.parse(fs.readFileSync(IN, "utf8"));
const day = (d) => d ? new Date(d + "T00:00:00Z").toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" }) : "No date";
const body = [
  new Paragraph({ children: [new TextRun({ text: "The 73 chats, unedited", bold: true, size: 36 })], spacing: { after: 120 } }),
  new Paragraph({ children: [new TextRun({ text: "As quoted in the Third Amended Complaint, In re London Silver Fixing, Ltd. Antitrust Litigation, No. 14-md-2573-VEC (S.D.N.Y.), Dkt. 258 and 258-1. In date order. \"[messages omitted in the court record]\" marks where the complaint leaves lines out.", color: "555555", size: 20 })], spacing: { after: 240 } }),
];
chats.forEach((c, i) => {
  body.push(new Paragraph({ text: `${i + 1}. ${day(c.date)}`, heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 40 } }));
  body.push(new Paragraph({ children: [new TextRun({ text: `${c.id} · complaint paragraph ${c.paragraph || "-"}${c.page ? `, page ${c.page}` : ""}`, color: "777777", size: 18 })], spacing: { after: 100 } }));
  c.messages.forEach(([who, text]) => body.push(new Paragraph({
    children: who === "***" ? [new TextRun({ text: "[messages omitted in the court record]", italics: true, color: "666666" })]
                            : [new TextRun({ text: who + ": ", bold: true }), new TextRun({ text })],
    spacing: { after: 40 } })));
});
const doc = new Document({
  creator: "RD2", title: "The 73 chats, unedited",
  styles: { default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [{ id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 24, bold: true, color: "1F3864" }, paragraph: { spacing: { before: 280, after: 40 }, outlineLevel: 1 } }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: ["Page ", PageNumber.CURRENT], color: "777777", size: 18 })] })] }) },
    children: body }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log("written", OUT, buf.length); });
