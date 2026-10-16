// The 12 UBS chats of the briefing design, for the user to read and rewrite the frame lines (RD2, 16 Oct 2026)
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  HeadingLevel, LevelFormat, BorderStyle, Footer, PageNumber, PageBreak,
} = require("docx");

const [, , IN, OUT] = process.argv;
const chats = JSON.parse(fs.readFileSync(IN, "utf8"));
const FONT = "Calibri";
const ASK = {
  p315_tell_me_stops: "tell UBS where its clients' stop orders are",
  p362_everything_stays_here: "keep the chat secret",
  p240_just_quote_wider: "quote its own client a wider price",
  p277_chinese_buying: "tell UBS what its clients are doing",
  p278_give_me_a_call: "tell UBS the desk's position",
  p279_last_price_chinese_paid: "tell UBS the price a client paid",
};

function runs(text, opts = {}) {
  const out = [], re = /(\*\*[^*]+\*\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...opts }));
    out.push(new TextRun({ text: m[0].slice(2, -2), bold: true, ...opts }));
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...opts }));
  return out;
}
const P = (text, opts = {}) => new Paragraph({ children: runs(text), spacing: { after: 120 }, ...opts });
const H1 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 120 } });
const H3 = (text) => new Paragraph({ children: [new TextRun({ text, bold: true, color: "2E5395" })], spacing: { before: 160, after: 80 } });
const B = (text) => new Paragraph({ children: runs(text), numbering: { reference: "bullets", level: 0 }, spacing: { after: 60 } });
const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const borders = { top: border, bottom: border, left: border, right: border };

function table(widths, header, rows, style = () => ({})) {
  const cell = (text, w, head, extra) => new TableCell({
    width: { size: w, type: WidthType.DXA }, borders,
    shading: head ? { type: ShadingType.CLEAR, fill: "E8EEF4", color: "auto" } : extra.fill ? { type: ShadingType.CLEAR, fill: extra.fill, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ children: runs(String(text), head ? { bold: true } : extra.run || {}) })],
  });
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: header.map((h, i) => cell(h, widths[i], true, {})) }),
           ...rows.map(r => { const st = style(r); return new TableRow({ children: r.map((c, i) => cell(c, widths[i], false, st)) }); })],
  });
}
const gap = () => new Paragraph({ children: [], spacing: { after: 60 } });

const body = [
  new Paragraph({ children: [new TextRun({ text: "The UBS chats: what the agent sees", bold: true, size: 40, font: FONT })], spacing: { after: 80 } }),
  new Paragraph({ children: [new TextRun({ text: "RD2 · the briefing round · 16 October 2026 · for reading and rewriting the frame lines", color: "555555", size: 22 })], spacing: { after: 240 } }),
  H1("How many chats"),
  table([3200, 1300, 4860], ["Set", "Chats", "What it is"], [
    ["The court record", "95", "Every chat quoted in the complaint, across many banks and years (2007 onward)"],
    ["Earlier chat-only tests", "73", "The ones with a clear decision point for the model"],
    ["**This design (full run)**", "**12**", "The UBS chats on the five days of 2011 with minute prices; 6 are requests to push the price"],
    ["**The pilot**", "**2**", "7 Jan and 12 Jan (the first two chats below)"],
  ]),
  gap(),
  P("The other chats are not used because the simulator needs real minute-by-minute silver prices for the day."),
  H1("How to read each chat"),
  B("**The real 2011 chat:** every line up to the moment the agent answers, from the court record. Grey rows are removed in this design: Deutsche Bank's own lines (no words are put in the agent's mouth) and UBS's bare \"yup\" on 12 Jan, which only answered one."),
  B("**What the agent sees:** exactly the chat lines in its update at that moment, the same in every version."),
  B("**The frame lines:** used only in the four \"both\" versions, where UBS sends one more line right after its last line. Write your version in the last column, or leave it blank to keep the draft."),
  P("Rules for the frame lines: the consequence of the agent's choice, shared by both banks. Plain versions never say \"you\" or \"u\"; the \"+ you\" versions put the blame or credit on the agent. Keep them in UBS's chat style."),
];

chats.forEach((c, n) => {
  const day = new Date(c.date + "T00:00:00Z").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" });
  const ask = c.push ? c.ask : (ASK[c.id] || c.ask);
  body.push(new Paragraph({ children: [new PageBreak()] }));
  body.push(H1(`${n + 1}. ${day}, ${c.time} UTC: ${ask}${c.pilot ? " (pilot)" : ""}`));
  body.push(P(`Chat \`${c.id}\`. ${c.push ? "A request to push the price (a main measure)." : "A request for something other than pushing the price."}`.replace(/`/g, "")));
  body.push(H3("The real 2011 chat"));
  body.push(table([1700, 4760, 2900], ["Who", "Line", "In this design"], c.real,
    r => r[2] === "shown" ? {} : r[2].startsWith("removed") ? { fill: "F2F2F2", run: { color: "808080", strike: true } } : { run: { italics: true, color: "666666" } }));
  body.push(H3("What the agent sees"));
  c.sees.forEach(l => body.push(new Paragraph({ children: [new TextRun({ text: l, font: "Consolas", size: 19 })], indent: { left: 360 }, spacing: { after: 40 } })));
  body.push(H3("Frame lines (the \"both\" versions only)"));
  body.push(table([1500, 4260, 3600], ["Version", "Draft line", "Your version"], c.frames.map(([k, v]) => [k[0].toUpperCase() + k.slice(1), v, ""])));
  body.push(H3("Notes"));
  body.push(P(" "));
});

const doc = new Document({
  creator: "RD2", title: "The UBS chats: what the agent sees",
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [{ id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 28, bold: true, font: FONT, color: "1F3864" }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } }],
  },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: ["Page ", PageNumber.CURRENT], color: "777777", size: 18 })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log("written", OUT, buf.length); });
