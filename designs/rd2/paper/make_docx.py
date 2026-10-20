"""Make an editable Word copy of the paper (RD2_paper.docx) from RD2_paper.tex.

Run after the PDF has been built (it reads the numbers of tables, figures and sections from RD2_paper.aux):
    cd designs/rd2/paper && python3 make_docx.py
Needs pandoc and pdflatex. The two figures are drawn by LaTeX and inserted as pictures; everything else (text, tables,
the equation, citations and references) stays editable in Word.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "docx_build")
TEXT_WIDTH_CM = 16.51  # 8.5in page with 1in margins


def read(name):
    return open(os.path.join(HERE, name), encoding="utf-8").read()


def labels_from_aux(aux):
    """{label: number} as LaTeX numbered them."""
    return dict(re.findall(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}", aux))


def balanced(s, i):
    """Index just past the brace group that opens at s[i] == '{'."""
    depth = 0
    for j in range(i, len(s)):
        depth += {"{": 1, "}": -1}.get(s[j], 0)
        if depth == 0:
            return j + 1
    raise ValueError("unbalanced braces")


def draw_figures(tex):
    """Draw each tikzpicture on its own with LaTeX and swap it for the picture."""
    preamble = ("\\documentclass[border=6pt]{standalone}\n\\usepackage[T1]{fontenc}\n\\usepackage{lmodern}\n"
                "\\usepackage{pgfplots}\n\\usetikzlibrary{positioning,arrows.meta}\n\\pgfplotsset{compat=1.17}\n")
    n = 0

    def swap(m):
        nonlocal n
        n += 1
        name = f"figure{n}"
        with open(os.path.join(BUILD, name + ".tex"), "w") as f:
            f.write(preamble + "\\begin{document}\n" + m.group(0) + "\n\\end{document}\n")
        subprocess.run(["pdflatex", "-interaction=nonstopmode", name + ".tex"], cwd=BUILD, check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run(["pdftoppm", "-r", "250", "-png", "-singlefile", name + ".pdf", name], cwd=BUILD, check=True)
        return f"\\includegraphics[width=0.95\\linewidth]{{{name}.png}}"

    return re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", swap, tex, flags=re.S)


def column_spec(spec):
    """[(kind, width in cm or None)] for a tabular(x) column spec; kind is l, c, r or X."""
    cols, i = [], 0
    while i < len(spec):
        ch = spec[i]
        if ch in "><@!" and i + 1 < len(spec) and spec[i + 1] == "{":
            i = balanced(spec, i + 1)
        elif ch in "pmb" and i + 1 < len(spec) and spec[i + 1] == "{":
            end = balanced(spec, i + 1)
            width = re.match(r"([\d.]+)cm", spec[i + 2:end - 1])
            # Word's table text is a little wider than LaTeX's footnote size, so narrow columns get some room.
            cols.append(("l", max(float(width.group(1)), 2.4) if width else None))
            i = end
        elif ch in "lcr":
            cols.append((ch, None)); i += 1
        elif ch in "XL":
            cols.append(("X", None)); i += 1
        elif ch == "C":
            cols.append(("C", None)); i += 1
        else:
            i += 1
    return cols


def plain_length(cell):
    cell = re.sub(r"\\(textbf|textit|emph|text)\{", "{", cell)
    cell = re.sub(r"\\[a-zA-Z]+\*?", "", cell)
    return len(re.sub(r"[{}$~\\]", "", cell).strip())


def tables_to_tabular(tex, aligns):
    """tabularx (which pandoc does not read) becomes tabular with every column's share of the page width, so Word lays
    the tables out as LaTeX did. The column alignments are kept in `aligns` for the filter."""
    out, pos = [], 0
    pat = re.compile(r"\\begin\{(tabularx|tabular)\}(\{\\linewidth\})?\{")
    while True:
        m = pat.search(tex, pos)
        if not m:
            out.append(tex[pos:]); break
        env = m.group(1)
        spec_end = balanced(tex, m.end() - 1)
        spec = tex[m.end():spec_end - 1]
        body_end = tex.index(f"\\end{{{env}}}", spec_end)
        body = tex[spec_end:body_end]
        cols = column_spec(spec)
        longest = [6] * len(cols)
        for row in re.split(r"\\\\", body):
            if "multicolumn" in row:
                continue
            cells = re.split(r"(?<!\\)&", re.sub(r"\\(toprule|midrule|bottomrule|hline)", "", row))
            if len(cells) == len(cols):
                for k, c in enumerate(cells):
                    longest[k] = max(longest[k], plain_length(c))
        fixed = sum(w / TEXT_WIDTH_CM for _, w in cols if w)
        weights = [0 if w else min(max(n, 6), 45) for (_, w), n in zip(cols, longest)]
        left = max(1.0 - fixed, 0.2)
        shares = [w / TEXT_WIDTH_CM if w else left * wt / sum(weights) for (_, w), wt in zip(cols, weights)]
        new_spec = "".join(f"p{{{s:.3f}\\linewidth}}" for s in shares)
        aligns.append("".join("C" if k in "cC" else "R" if k == "r" else "L" for k, _ in cols))
        out.append(tex[pos:m.start()] + f"\\begin{{tabular}}{{{new_spec}}}" + body + "\\end{tabular}")
        pos = body_end + len(f"\\end{{{env}}}")
    return "".join(out)


def number_captions(tex, labels):
    """Tables and figures are numbered in order, as LaTeX numbers them (the labels' numbers are checked against it)."""
    count = {"table": 0, "figure": 0}

    def fix(m):
        block, kind = m.group(0), m.group(1)
        if "\\caption{" not in block:
            return block
        count[kind] += 1
        lab = re.search(r"\\label\{([^}]*)\}", block)
        assert not lab or labels.get(lab.group(1)) == str(count[kind]), lab.group(1)
        word = "Table" if kind == "table" else "Figure"
        return block.replace("\\caption{", f"\\caption{{\\textbf{{{word} {count[kind]}:}} ", 1)
    return re.sub(r"\\begin\{(table|figure)\}.*?\\end\{\1\}", fix, tex, flags=re.S)


def number_sections(tex):
    """Write the section numbers into the headings (appendices lettered), as in the PDF."""
    sec = sub = 0
    appendix = False
    out, pos = [], 0
    for m in re.finditer(r"\\appendix\b|\\(section|subsection)\{", tex):
        if m.group(0).startswith("\\appendix"):
            out.append(tex[pos:m.start()]); pos = m.end()
            appendix, sec = True, 0
            continue
        end = balanced(tex, m.end() - 1)
        title = tex[m.end():end - 1]
        if m.group(1) == "section":
            sec, sub = sec + 1, 0
            num = f"Appendix {chr(64 + sec)}." if appendix else f"{sec}"
            head = f"\\section*{{{num}~{title}}}"
        else:
            sub += 1
            head = f"\\subsection*{{{sec}.{sub}~{title}}}"
        out.append(tex[pos:m.start()] + head); pos = end
    out.append(tex[pos:])
    return "".join(out)


def prepare(tex, labels, aligns):
    tex = re.sub(r"\\newcommand\{\\authornote\}.*\n",
                 "\\\\newcommand{\\\\authornote}[1]{\\\\textbf{[Note:} \\\\textit{#1}\\\\textbf{]}}\n", tex)
    tex = re.sub(r"\\title\{.*?\n\\date\{.*?\}\n",
                 "\\\\title{The Push Down the Mountain: Loss, Gain, Blame and Credit in an AI Trading Agent's "
                 "Decision to Collude}\n\\\\author{Harrison Margolin, Algoverse AI Research}\n"
                 "\\\\date{Working draft, October 20, 2026. Behavioral results final; interpretability results in "
                 "progress.}\n", tex, flags=re.S)
    tex = draw_figures(tex)
    tex = tables_to_tabular(tex, aligns)
    tex = number_captions(tex, labels)
    eq = re.search(r"\\begin\{equation\}(.*?)\\label\{([^}]*)\}\s*\\end\{equation\}", tex, flags=re.S)
    if eq:
        tex = tex.replace(eq.group(0), f"\\[{eq.group(1).strip()} \\qquad ({labels[eq.group(2)]})\\]")
    tex = re.sub(r"\\eqref\{([^}]*)\}", lambda m: f"({labels[m.group(1)]})", tex)
    tex = re.sub(r"\\ref\{([^}]*)\}", lambda m: labels[m.group(1)], tex)
    tex = re.sub(r"\\paragraph\{", r"\\textbf{", tex)
    tex = tex.replace("\\bibliographystyle{plainnat}\n\\bibliography{references}", "REFSMARKER")
    return number_sections(tex)


FILTER = r"""
local aligns = {}
for line in io.lines(os.getenv("ALIGNS")) do table.insert(aligns, line) end
local n = 0
function Table(t)
  n = n + 1
  local a = aligns[n]
  if a then
    for j, cs in ipairs(t.colspecs) do
      local ch = a:sub(j, j)
      local al = (ch == "C" and "AlignCenter") or (ch == "R" and "AlignRight") or "AlignLeft"
      t.colspecs[j] = {al, cs[2]}
    end
  end
  return t
end

-- Math becomes ordinary text (italic letters, real sub- and superscripts), which every viewer shows and is easy to edit.
local greek = {alpha = "α", beta = "β", gamma = "γ", delta = "δ", varepsilon = "ε", epsilon = "ε"}
local function group(s, i)
  local depth = 0
  for j = i, #s do
    local c = s:sub(j, j)
    if c == "{" then depth = depth + 1 elseif c == "}" then
      depth = depth - 1
      if depth == 0 then return s:sub(i + 1, j - 1), j + 1 end
    end
  end
  return s:sub(i + 1), #s + 1
end
local function as_text(s)
  local out, i = {}, 1
  local function push(x) table.insert(out, x) end
  while i <= #s do
    local c = s:sub(i, i)
    if c == "\\" then
      local name = s:match("^\\([a-zA-Z]+)", i)
      if name then
        i = i + 1 + #name
        if name == "text" or name == "mathrm" then
          local g; g, i = group(s, i); push(pandoc.Str(g))
        elseif greek[name] then push(pandoc.Emph{pandoc.Str(greek[name])})
        elseif name == "times" then push(pandoc.Str("×"))
        elseif name == "qquad" then push(pandoc.Str("\u{2003}\u{2003}"))
        elseif name == "cdot" then push(pandoc.Str("·"))
        else push(pandoc.Str(name)) end
      else
        local nx = s:sub(i + 1, i + 1)
        if nx == "%" or nx == "$" then push(pandoc.Str(nx))
        elseif nx == "," and #out > 0 and out[#out].t ~= "Space" then push(pandoc.Space()) end
        i = i + 2
      end
    elseif c == "^" or c == "_" then
      local inner
      if s:sub(i + 1, i + 1) == "{" then inner, i = group(s, i + 1) else inner, i = s:sub(i + 1, i + 1), i + 2 end
      push(c == "^" and pandoc.Superscript(as_text(inner)) or pandoc.Subscript(as_text(inner)))
    elseif c:match("%a") then push(pandoc.Emph{pandoc.Str(c)}); i = i + 1
    elseif c == "-" then push(pandoc.Str("−")); i = i + 1
    elseif c == "'" then push(pandoc.Str("′")); i = i + 1
    elseif c:match("%s") then
      if #out > 0 and out[#out].t ~= "Space" then push(pandoc.Space()) end
      i = i + 1
    else push(pandoc.Str(c)); i = i + 1 end
  end
  return out
end

function Para(p)
  if pandoc.utils.stringify(p) == "REFSMARKER" then
    return {pandoc.Header(1, "References", {class = "unnumbered"}), pandoc.Div({}, {id = "refs"})}
  end
  -- A displayed equation gets its own centred paragraph.
  local blocks, run = {}, {}
  local split = false
  for _, x in ipairs(p.content) do
    if x.t == "Math" and x.mathtype == "DisplayMath" then
      split = true
      if #run > 0 then table.insert(blocks, pandoc.Para(run)) end
      table.insert(blocks, pandoc.Div({pandoc.Para(as_text(x.text))}, {["custom-style"] = "Equation"}))
      run = {}
    elseif not (#run == 0 and (x.t == "Space" or x.t == "SoftBreak")) then
      table.insert(run, x)
    end
  end
  if split then
    if #run > 0 then table.insert(blocks, pandoc.Para(run)) end
    return blocks
  end
end

function Math(m)
  if m.mathtype == "InlineMath" then return as_text(m.text) end
end
"""


def make_reference(path):
    """Pandoc's own Word template with an academic look: Times New Roman, black headings, 11pt text, 9pt tables,
    US Letter with 1-inch margins, and a centred style for the equation."""
    import shutil, zipfile
    raw = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"], check=True,
                         capture_output=True).stdout
    tmp = path + ".tmp"
    open(tmp, "wb").write(raw)
    font = 'w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"'
    with zipfile.ZipFile(tmp) as z:
        files = {n: z.read(n) for n in z.namelist()}
    st = files["word/styles.xml"].decode()
    st = re.sub(r'<w:rFonts w:asciiTheme="[^"]*" w:eastAsiaTheme="[^"]*" w:hAnsiTheme="[^"]*" w:cstheme="[^"]*" />',
                f"<w:rFonts {font} />", st)
    st = re.sub(r'<w:color w:val="[0-9A-F]+" w:themeColor="accent1"[^/]*/>', "", st)
    st = st.replace('<w:sz w:val="24" />\n        <w:szCs w:val="24" />',
                    '<w:sz w:val="22" />\n        <w:szCs w:val="22" />', 1)
    st = st.replace('<w:spacing w:before="180" w:after="180" />', '<w:spacing w:before="0" w:after="140" />', 1)

    def restyle(sid, rpr):
        nonlocal st
        m = re.search(r'(<w:style [^>]*w:styleId="' + sid + r'".*?)(</w:style>)', st, re.S)
        body = re.sub(r"<w:sz w:val=\"\d+\" />\s*<w:szCs w:val=\"\d+\" />", "", m.group(1))
        if "<w:rPr>" in body:
            body = body.replace("<w:rPr>", "<w:rPr>" + rpr, 1)
        else:
            body += "<w:rPr>" + rpr + "</w:rPr>"
        st = st[:m.start()] + body + m.group(2) + st[m.end():]

    restyle("Title", '<w:sz w:val="32" /><w:szCs w:val="32" />')
    restyle("Heading1", '<w:sz w:val="28" /><w:szCs w:val="28" />')
    restyle("Heading2", '<w:sz w:val="24" /><w:szCs w:val="24" />')
    restyle("Compact", '<w:sz w:val="18" /><w:szCs w:val="18" />')
    restyle("Caption", '<w:sz w:val="20" /><w:szCs w:val="20" />')
    st = st.replace("</w:styles>",
                    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Equation"><w:name w:val="Equation" />'
                    '<w:basedOn w:val="BodyText" /><w:pPr><w:spacing w:before="120" w:after="120" />'
                    '<w:jc w:val="center" /></w:pPr></w:style></w:styles>')
    files["word/styles.xml"] = st.encode()
    doc = files["word/document.xml"].decode()
    doc = doc.replace("</w:body>", '<w:sectPr><w:pgSz w:w="12240" w:h="15840" /><w:pgMar w:top="1440" '
                      'w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0" />'
                      "</w:sectPr></w:body>")
    files["word/document.xml"] = doc.encode()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in files.items():
            z.writestr(n, b)
    os.remove(tmp)


def main():
    os.makedirs(BUILD, exist_ok=True)
    labels = labels_from_aux(read("RD2_paper.aux"))
    aligns = []
    tex = prepare(read("RD2_paper.tex"), labels, aligns)
    open(os.path.join(BUILD, "paper_for_word.tex"), "w").write(tex)
    open(os.path.join(BUILD, "aligns.txt"), "w").write("\n".join(aligns) + "\n")
    open(os.path.join(BUILD, "filter.lua"), "w").write(FILTER)
    make_reference(os.path.join(BUILD, "reference.docx"))
    cmd = ["pandoc", "paper_for_word.tex", "-f", "latex", "-o", os.path.join(HERE, "RD2_paper.docx"),
           "--lua-filter=filter.lua", "--citeproc", f"--bibliography={os.path.join(HERE, 'references.bib')}",
           "--resource-path=.", "--reference-doc=reference.docx"]
    subprocess.run(cmd, cwd=BUILD, check=True, env={**os.environ, "ALIGNS": "aligns.txt"})
    print("wrote", os.path.join(HERE, "RD2_paper.docx"))


if __name__ == "__main__":
    sys.exit(main())
