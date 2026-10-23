// All 73 chats of the words study as a Word document, marking the 12 in the trading run and the 2 in the pilot
// (RD2, 16 Oct 2026). Input: the JSON from export_chats73.py.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  HeadingLevel, LevelFormat, BorderStyle, Footer, PageNumber, PageBreak,
} = require("docx");

const [, , IN, OUT] = process.argv;
const chats = JSON.parse(fs.readFileSync(IN, "utf8"));
const FONT = "Calibri";
const runs = (text, opts = {}) => {
  const out = [], re = /(\*\*[^*]+\*\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...opts }));
    out.push(new TextRun({ text: m[0].slice(2, -2), bold: true, ...opts }));
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...opts }));
  return out;
};
const P = (text, opts = {}) => new Paragraph({ children: runs(text), spacing: { after: 100 }, ...opts });
const H1 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 200, after: 100 } });
const B = (text) => new Paragraph({ children: runs(text), numbering: { reference: "bullets", level: 0 }, spacing: { after: 60 } });
const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(widths, header, rows, style = () => ({})) {
  const cell = (text, w, head, st) => new TableCell({
    width: { size: w, type: WidthType.DXA }, borders,
    shading: head ? { type: ShadingType.CLEAR, fill: "E8EEF4", color: "auto" } : st.fill ? { type: ShadingType.CLEAR, fill: st.fill, color: "auto" } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({ children: runs(String(text), head ? { bold: true, size: 19 } : { size: 19, ...(st.run || {}) }) })],
  });
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: header.map((h, i) => cell(h, widths[i], true, {})) }),
           ...rows.map(r => { const st = style(r); return new TableRow({ children: r.slice(0, widths.length).map((c, i) => cell(c, widths[i], false, st)) }); })],
  });
}
const day = (d) => d ? new Date(d + "T00:00:00Z").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }) : "no date";
const bank = (role) => role.split(" [")[0];
const flag = (c) => c.pilot ? "pilot + trading" : c.trading ? "trading" : "";

const nTrading = chats.filter(c => c.trading).length, nPilot = chats.filter(c => c.pilot).length;
const byBank = {};
chats.forEach(c => { byBank[bank(c.role)] = (byBank[bank(c.role)] || 0) + 1; });

const body = [
  new Paragraph({ children: [new TextRun({ text: "All 73 chats", bold: true, size: 40, font: FONT })], spacing: { after: 80 } }),
  new Paragraph({ children: [new TextRun({ text: "RD2 · the words study and the trading run · 16 October 2026", color: "555555", size: 22 })], spacing: { after: 200 } }),
  H1("What this is"),
  P("Every chat in the court record (the Third Amended Complaint) with a point where the agent can take one trader's seat and write the next message: 95 chats in the record, minus those with no such point and the two phone chats. Each chat is shown whole, in date order."),
  B(`**The words study** uses all 73: the agent reads the chat up to its turn and writes a reply.`),
  B(`**The trading run** uses ${nTrading} of them: the UBS chats on the five days of 2011 with minute-by-minute prices, where the agent also trades (marked **trading**).`),
  B(`**The pilot** uses ${nPilot}: 7 Jan and 12 Jan (marked **pilot + trading**).`),
  B("**Whose seat:** " + Object.entries(byBank).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(", ") + "."),
  P("In each chat: lines before the agent's turn are white (the agent sees them in the words study); its own bank's lines are in bold; the blue row is where it answers; the yellow lines are how the real chat went on, which it never sees."),
  H1("The 73 at a glance"),
  table([500, 1350, 2700, 1900, 1610, 1300], ["#", "Date", "Chat", "Agent plays", "Asked to", "Also in"],
    chats.map((c, i) => [String(i + 1), day(c.date), c.id, bank(c.role), c.kind, flag(c)]),
    r => r[5] ? { fill: r[5].startsWith("pilot") ? "FFE8CC" : "E2EFDA" } : {}),
];

chats.forEach((c, i) => {
  body.push(new Paragraph({ children: [new PageBreak()] }));
  body.push(H1(`${i + 1}. ${day(c.date)}: ${c.id}${c.trading ? (c.pilot ? "  (pilot + trading)" : "  (trading)") : ""}`));
  body.push(P(`**The agent plays:** ${c.role}. **Asked to:** ${c.kind}: ${c.decision}. **Scheme:** ${c.scheme || "not stated"}. ` +
    `**Complaint paragraph:** ${c.paragraph || "-"}${c.core ? ". One of the 24 core chats." : "."}`));
  body.push(table([2600, 6760], ["Who", "Line"], c.rows,
    r => r[3] === "marker" ? { fill: "DCE6F1", run: { bold: true, color: "1F3864" } }
      : r[2] === "after" ? { fill: "FFF8E1", run: { color: "5A4A00", bold: r[3] === "self" } }
      : r[3] === "gap" ? { run: { italics: true, color: "666666" } } : { run: { bold: r[3] === "self" } }));
  if (c.real_did) body.push(P(`**What the real trader did:** ${c.real_did}.`, { spacing: { before: 80, after: 60 } }));
  if (c.note) body.push(new Paragraph({ children: [new TextRun({ text: "Note: " + c.note, italics: true, color: "555555", size: 19 })], spacing: { after: 60 } }));
});

const doc = new Document({
  creator: "RD2", title: "All 73 chats",
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [{ id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 26, bold: true, font: FONT, color: "1F3864" }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 0 } }],
  },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1260, right: 1260, bottom: 1260, left: 1260 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: ["Page ", PageNumber.CURRENT], color: "777777", size: 18 })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log("written", OUT, buf.length); });
