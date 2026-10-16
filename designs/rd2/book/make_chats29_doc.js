// The 29 UBS chats in the Deutsche Bank career: each original chat, then UBS's added line per framing, with a blank
// column for the user's own wording (RD2, 16 Oct 2026). Input: the JSON from export_chats29.py.
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
const H3 = (text) => new Paragraph({ children: [new TextRun({ text, bold: true, color: "2E5395" })], spacing: { before: 160, after: 60 } });
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
const day = (d) => new Date(d + "T00:00:00Z").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" });
const NOW = new Set(["p344_i_can_hunt_with_u", "p316_bust_through_it"]);
const SEES = { shown: "sees it", removed: "removed: the agent writes its own", bare: "removed: it answered a removed line", gap: "sees \"[... messages omitted ...]\"" };

const nTrading = chats.filter(c => c.trading).length;
const body = [
  new Paragraph({ children: [new TextRun({ text: "UBS's pressure, chat by chat", bold: true, size: 40, font: FONT })], spacing: { after: 80 } }),
  new Paragraph({ children: [new TextRun({ text: "RD2 · the Deutsche Bank career · 16 October 2026 · for reading and rewriting UBS's added lines", color: "555555", size: 22 })], spacing: { after: 200 } }),
  H1("What this is"),
  table([3000, 1100, 5260], ["Set", "Chats", "What it is"], [
    ["The court record", "73", "Every chat with a point where the agent can take one trader's seat"],
    ["The Deutsche Bank career", "47", "The chats where the agent sits in Deutsche Bank's seat, in date order"],
    ["**With UBS in them**", "**29**", "**This document.** UBS writes 59 lines in them"],
    ["On a trading day", String(nTrading), "The 5 days of 2011 with minute prices: the agent also trades (marked TRADING DAY)"],
    ["In the run ready now", "2", "7 Jan and 12 Jan (marked IN THE RUN NOW)"],
  ]),
  P(""),
  B("**The original chat** is shown whole, as in the court record. Deutsche Bank's own lines are struck through: the agent writes its own. The blue row is where the agent answers; the grey lines after it are how the real chat went on, which the agent never sees."),
  B("**UBS's added line** is one sentence from UBS, sent right after its last real line, just before the agent answers. It appears only in the \"both\" versions, on top of the management briefing of the same name. The neutral and management-only versions get no added line."),
  B("**The rule I followed:** the plain lines (loss, gain) say what happens to both banks and never say \"you\"; the \"+ you\" lines put it on the agent, with \"you\" spelled out. UBS's real lines keep their \"u\"."),
  B("**To rewrite:** write your wording in the \"Your version\" column (or send it to Claude as e.g. \"7 Jan loss + you: …\"). Blank means keep mine."),
  B(`**Status:** all drafts. The 12 trading-day sets are in data/silver/ubs_frames.json, the 17 chat-only sets in data/silver/ubs_frames_chat_only.json.`),
];

chats.forEach((c, i) => {
  body.push(new Paragraph({ children: [new PageBreak()] }));
  const tag = NOW.has(c.id) ? "  (TRADING DAY · IN THE RUN NOW)" : c.trading ? "  (TRADING DAY)" : "  (chat only)";
  body.push(H1(`${i + 1}. ${day(c.date)}: ${c.id}${tag}`));
  body.push(P(`**UBS wants the agent to:** ${c.ask}. **The decision:** ${c.decision}.` + (c.real_did ? ` **What the real Deutsche Bank trader did:** ${[].concat(c.real_did).join("; ")}.` : "")));
  body.push(H3("The original chat"));
  const rows = c.rows.map(([who, line, k]) => [who, line, SEES[k], k]);
  rows.push(["", "THE AGENT ANSWERS HERE (in a \"both\" version, UBS's added line comes just before this)", "", "marker"]);
  c.after.forEach(([who, line]) => rows.push([who, line, "never shown", "after"]));
  body.push(table([1900, 5160, 2300], ["Who", "Line", "The agent"], rows,
    r => r[3] === "marker" ? { fill: "DCE6F1", run: { bold: true, color: "1F3864" } }
      : r[3] === "after" ? { fill: "F2F2F2", run: { color: "777777" } }
      : r[3] === "removed" || r[3] === "bare" ? { run: { strike: true, color: "999999" } }
      : r[3] === "gap" ? { run: { italics: true, color: "666666" } } : {}));
  body.push(H3("UBS's added line, per framing"));
  const fr = [["neutral (and management only)", "(no added line)", ""]].concat(c.frames.map(([k, t]) => [`both ${k}`, t, ""]));
  body.push(table([2400, 4560, 2400], ["Framing", "UBS's added line (my draft)", "Your version"], fr,
    r => r[0].startsWith("neutral") ? { run: { italics: true, color: "777777" } } : {}));
});

const doc = new Document({
  creator: "RD2", title: "UBS's pressure, chat by chat",
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
