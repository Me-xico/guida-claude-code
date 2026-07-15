"""Genera slides.html: la guida paginata, un h2 per schermata.

Uso:  uv run --with markdown python build-slides.py
Rigenerare dopo ogni modifica ai capitoli md (come mkdocs per il sito).
"""
import re
from pathlib import Path

import markdown

HERE = Path(__file__).parent
OUT = HERE / "slides.html"

BLOCKS = [
    ("Base", ["01-installazione.md", "02-setup-e-config.md",
              "03-uso-quotidiano.md", "04-claude-md-e-rules.md"]),
    ("Metodo", ["11-verifica.md", "12-prompt-engineering.md",
                "13-errori-comuni.md"]),
    ("Potenza", ["05-skills-e-slash-commands.md", "06-agenti.md",
                 "07-hooks.md", "08-mcp.md", "09-plugins.md",
                 "10-workflow-frontend.md"]),
    ("Riferimento", ["14-must-have-e-costi.md", "15-risparmiare-token.md"]),
]

MD = markdown.Markdown(extensions=["fenced_code", "tables"])


def md_to_pages(path: Path):
    """Spezza un capitolo in pagine: intro (h1 + testo fino al primo h2),
    poi una pagina per ogni sezione h2."""
    text = path.read_text()
    title = re.match(r"#\s+(.+)", text).group(1)
    parts = re.split(r"(?m)^## ", text)
    pages = [(title, None, parts[0])]
    for part in parts[1:]:
        h2, _, body = part.partition("\n")
        pages.append((title, h2.strip(), "## " + part))
    return pages


sections_html, toc_entries = [], []
n = 0

for block, files in BLOCKS:
    n += 1
    sections_html.append(
        f'<section class="slide divider"><div class="divider-inner">'
        f"<h1>{block}</h1></div></section>"
    )
    toc_entries.append((n, f"— {block} —", True))
    for f in files:
        for chap, sect, body in md_to_pages(HERE / f):
            n += 1
            MD.reset()
            html_body = MD.convert(body)
            crumb = chap if not sect else f"{chap.split('—')[0].strip()} · {sect}"
            sections_html.append(
                f'<section class="slide"><div class="crumb">{crumb}</div>'
                f'<div class="content">{html_body}</div></section>'
            )
            toc_entries.append((n, sect or chap, False))

toc_html = "".join(
    f'<div class="toc-item{" toc-block" if is_block else ""}" data-n="{i}">{label}</div>'
    for i, label, is_block in toc_entries
)

page = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guida a Claude Code — sfogliabile</title>
<style>
:root {{ --bg:#1a1c1f; --fg:#e8e6e3; --dim:#9a978f; --accent:#e8845c;
         --code-bg:#26292e; --border:#3a3d42; }}
html[data-theme=light] {{ --bg:#faf9f6; --fg:#1f2328; --dim:#6a6e74;
         --accent:#c2542a; --code-bg:#f0efec; --border:#d8d6d0; }}
* {{ box-sizing:border-box; margin:0; }}
body {{ background:var(--bg); color:var(--fg); font:22px/1.55 system-ui,sans-serif; }}
.slide {{ display:none; min-height:100vh; padding:3.2rem 8vw 4.5rem; }}
.slide.active {{ display:block; }}
.crumb {{ color:var(--accent); font-size:.75em; text-transform:uppercase;
          letter-spacing:.06em; margin-bottom:1.2rem; }}
.content h1 {{ font-size:2.1em; margin-bottom:1rem; }}
.content h2 {{ font-size:1.6em; margin-bottom:1rem; color:var(--accent); }}
.content h3 {{ font-size:1.15em; margin:1.2rem 0 .5rem; }}
.content p, .content ul, .content ol, .content table, .content blockquote,
.content pre {{ margin-bottom:.9rem; }}
.content li {{ margin:.3rem 0 .3rem 1.2rem; }}
.content code {{ background:var(--code-bg); padding:.12em .35em;
                 border-radius:4px; font-size:.85em; }}
.content pre {{ background:var(--code-bg); padding:1rem; border-radius:8px;
                overflow-x:auto; }}
.content pre code {{ background:none; padding:0; font-size:.8em; }}
.content blockquote {{ border-left:4px solid var(--accent); padding:.4rem 1rem;
                       color:var(--dim); }}
.content table {{ border-collapse:collapse; width:100%; font-size:.9em; }}
.content th, .content td {{ border:1px solid var(--border); padding:.45rem .7rem;
                            text-align:left; }}
.content img {{ max-width:100%; max-height:62vh; display:block;
                margin:1rem auto; border-radius:8px; }}
.content a {{ color:var(--accent); }}
.divider {{ display:none; }} .divider.active {{ display:flex;
            align-items:center; justify-content:center; }}
.divider h1 {{ font-size:4em; color:var(--accent); }}
#bar {{ position:fixed; bottom:0; left:0; right:0; display:flex;
        justify-content:space-between; padding:.5rem 1.2rem;
        background:var(--bg); border-top:1px solid var(--border);
        font-size:.7em; color:var(--dim); }}
#toc {{ position:fixed; inset:0; background:var(--bg); overflow-y:auto;
        padding:3rem 10vw; display:none; z-index:10; }}
#toc.open {{ display:block; }}
.toc-item {{ padding:.3rem .6rem; cursor:pointer; border-radius:6px; }}
.toc-item:hover {{ background:var(--code-bg); }}
.toc-block {{ color:var(--accent); font-weight:700; margin-top:1rem;
              pointer-events:none; }}
.edge {{ position:fixed; top:0; bottom:2.5rem; width:11vw; cursor:pointer;
         z-index:5; }} #prev {{ left:0; }} #next {{ right:0; }}
</style></head><body>
<section class="slide divider"><div class="divider-inner">
<h1 style="font-size:3em">Guida a Claude Code</h1>
<p style="color:var(--dim);margin-top:1rem">Da zero a produttivo · verificato
luglio 2026 (v2.1.210) · ← → per sfogliare · <b>i</b> = indice · <b>t</b> = tema</p>
</div></section>
{"".join(sections_html)}
<div id="toc">{toc_html}</div>
<div class="edge" id="prev"></div><div class="edge" id="next"></div>
<div id="bar"><span id="where"></span><span><b>i</b> indice · <b>t</b> tema ·
<span id="count"></span></span></div>
<script>
const S=[...document.querySelectorAll('.slide')];let cur=0;
function go(n){{S[cur].classList.remove('active');cur=Math.max(0,Math.min(S.length-1,n));
S[cur].classList.add('active');location.hash=cur;window.scrollTo(0,0);
document.getElementById('count').textContent=(cur+1)+' / '+S.length;
const c=S[cur].querySelector('.crumb');
document.getElementById('where').textContent=c?c.textContent:'Guida a Claude Code';}}
addEventListener('keydown',e=>{{
if(e.key==='ArrowRight'||e.key==='PageDown'||(e.key===' '&&!e.shiftKey))go(cur+1);
else if(e.key==='ArrowLeft'||e.key==='PageUp'||(e.key===' '&&e.shiftKey))go(cur-1);
else if(e.key==='Home')go(0);else if(e.key==='End')go(S.length-1);
else if(e.key==='i'||e.key==='o')document.getElementById('toc').classList.toggle('open');
else if(e.key==='Escape')document.getElementById('toc').classList.remove('open');
else if(e.key==='t'){{const h=document.documentElement;
h.dataset.theme=h.dataset.theme==='light'?'':'light';}}else return;e.preventDefault();}});
document.getElementById('prev').onclick=()=>go(cur-1);
document.getElementById('next').onclick=()=>go(cur+1);
document.querySelectorAll('.toc-item:not(.toc-block)').forEach(el=>el.onclick=()=>{{
document.getElementById('toc').classList.remove('open');go(+el.dataset.n);}});
go(+location.hash.slice(1)||0);
</script></body></html>"""

OUT.write_text(page)
print(f"slides.html: {len(sections_html)+1} pagine, {OUT.stat().st_size//1024} KB")
