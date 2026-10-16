// The 29 UBS chats side by side, one column per framing (RD2, 16 Oct 2026). Landscape. Input: export_chats29.py's JSON.
// First an overview (one row per chat, UBS's added line in each framing), then each chat as the agent reads it in
// each framing: read down a column to see exactly what the agent gets.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  HeadingLevel, BorderStyle, Footer, PageNumber, PageBreak, PageOrientation,
} = require("docx");

const [, , IN, OUT] = process.argv;
const chats = JSON.parse(fs.readFileSync(IN, "utf8"));
const FONT = "Calibri";
const FR = ["loss", "gain", "loss + you", "gain + you"];
const NOW = new Set(["p344_i_can_hunt_with_u", "p316_bust_through_it"]);
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
const P = (text, opts = {}) => new Paragraph({ children: runs(text), spacing: { after: 80 }, ...opts });
const H1 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 120, after: 80 } });
const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const borders = { top: border, bottom: border, left: border, right: border };
// cells: either a string or {text, fill, run}
function table(widths, header, rows) {
  const cell = (c, w, head) => {
    const o = typeof c === "object" && c !== null ? c : { text: c };
    return new TableCell({
      width: { size: w, type: WidthType.DXA }, borders,
      shading: head ? { type: ShadingType.CLEAR, fill: "E8EEF4", color: "auto" } : o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: "auto" } : undefined,
      margins: { top: 40, bottom: 40, left: 70, right: 70 },
      children: [new Paragraph({ children: runs(String(o.text ?? ""), head ? { bold: true, size: 17 } : { size: 17, ...(o.run || {}) }) })],
    });
  };
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: header.map((h, i) => cell(h, widths[i], true)) }),
           ...rows.map(r => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, widths[i], false)) }))],
  });
}
const day = (d) => new Date(d + "T00:00:00Z").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" });
const tag = (c) => NOW.has(c.id) ? "trading day · in the run now" : c.trading ? "trading day" : "chat only";
const ADDED = "FFF2CC";   // the added line, in every framing column

const body = [
  new Paragraph({ children: [new TextRun({ text: "UBS's pressure, framing by framing", bold: true, size: 36, font: FONT })], spacing: { after: 60 } }),
  new Paragraph({ children: [new TextRun({ text: "RD2 · the 29 UBS chats in the Deutsche Bank career · 16 October 2026 · one column per framing", color: "555555", size: 20 })], spacing: { after: 160 } }),
  P("**Part 1, the overview:** one row per chat: UBS's last real line before the agent answers, then the line UBS adds in each framing. **Part 2, chat by chat:** the original chat in the first column (Deutsche Bank's lines struck through: the agent writes its own), then the chat exactly as the agent reads it in each framing. The added line is shaded yellow. Neutral and management-only versions read like the Original column without the struck lines, and with no added line."),
  H1("Part 1. The overview"),
  table([400, 1150, 2650, 2550, 2550, 2550, 2550], ["#", "Chat", "UBS's last real line", "both loss", "both gain", "both loss + you", "both gain + you"],
    chats.map((c, i) => {
      const last = [...c.rows].reverse().find(r => r[2] === "shown" && r[0] === "UBS");
      const f = Object.fromEntries(c.frames);
      const fill = NOW.has(c.id) ? "FFE8CC" : c.trading ? "E2EFDA" : undefined;
      return [{ text: String(i + 1), fill }, { text: `${day(c.date)}\n${c.id.split("_")[0]} · ${tag(c)}`, fill },
              { text: last ? last[1] : "", fill }, ...FR.map(k => ({ text: f[k], fill }))];
    })),
  P("Orange: in the run now (7 and 12 Jan). Green: the other trading days. White: chat only.", { spacing: { before: 80 } }),
];

chats.forEach((c, i) => {
  body.push(new Paragraph({ children: [new PageBreak()] }));
  body.push(H1(`${i + 1}. ${day(c.date)}: ${c.id} (${tag(c)})`));
  body.push(P(`**UBS wants the agent to:** ${c.ask}. **The decision:** ${c.decision}.` + (c.real_did ? ` **What the real Deutsche Bank trader did:** ${[].concat(c.real_did).join("; ")}.` : "")));
  const f = Object.fromEntries(c.frames);
  const rows = c.rows.map(([who, line, k]) => {
    const orig = k === "removed" || k === "bare" ? { text: line, run: { strike: true, color: "999999" } }
      : k === "gap" ? { text: line, run: { italics: true, color: "666666" } } : line;
    const seen = k === "shown" ? line : k === "gap" ? { text: "[... messages omitted ...]", run: { italics: true, color: "666666" } } : "";
    return [who, orig, ...FR.map(() => seen)];
  });
  rows.push(["UBS (added)", { text: "(none in the record)", run: { italics: true, color: "777777" } },
             ...FR.map(k => ({ text: f[k], fill: ADDED, run: { bold: true } }))]);
  rows.push([{ text: "", fill: "DCE6F1" }, ...Array(5).fill({ text: "THE AGENT ANSWERS HERE", fill: "DCE6F1", run: { bold: true, color: "1F3864", size: 15 } })]);
  body.push(table([1150, 2650, 2650, 2650, 2650, 2650], ["Who", "Original (court record)", "both loss", "both gain", "both loss + you", "both gain + you"], rows));
});

const doc = new Document({
  creator: "RD2", title: "UBS's pressure, framing by framing",
  styles: {
    default: { document: { run: { font: FONT, size: 19 } } },
    paragraphStyles: [{ id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 24, bold: true, font: FONT, color: "1F3864" }, paragraph: { spacing: { before: 120, after: 80 }, outlineLevel: 0 } }],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
                          margin: { top: 720, right: 720, bottom: 720, left: 720 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: ["Page ", PageNumber.CURRENT], color: "777777", size: 16 })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log("written", OUT, buf.length); });
