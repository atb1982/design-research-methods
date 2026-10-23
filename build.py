import json
_d = json.load(open('data.json', encoding='utf-8'))
_ov = json.load(open('overview_links.json', encoding='utf-8'))
_ids = {m['id']: m for m in _d['methods']}
for _k, _v in _ov.items():
    assert _k in _ids and _ids[_k]['kind'] == 'brief', _k
    for _l in _v:
        assert _l['url'].startswith('https://') and _l['title'] and _l['publisher'], _l
    _ids[_k]['overview'] = _v
_tp = json.load(open('templates.json', encoding='utf-8'))
for _k, _v in _tp.items():
    assert _k in _ids, _k
    for _l in _v:
        assert _l['url'].startswith('https://') and _l['title'] and _l['publisher'] and _l['format'] and _l['access'], _l
    _ids[_k]['templates'] = _v
import os
_own = json.load(open('templates_own.json', encoding='utf-8'))
for _t in _own:
    assert os.path.isfile(_t['file']), _t['file']
    assert _t['title'] and _t['format'] and _t['desc'] and _t['step'] in ('Plan','Consent','Collect','Analyze'), _t
    for _k in _t['methods']:
        assert _k in _ids, _k
for _k in _ids:
    _mine = [{'title': _t['title'], 'publisher': 'Design Research Methods', 'url': _t['file'], 'format': _t['format'],
              'access': 'Free download, no sign-in.', 'own': True}
             for _t in _own if _k in _t['methods']]
    if _mine:
        _ids[_k]['templates'] = _mine + _ids[_k].get('templates', [])
_d['ownTemplates'] = [{k: _t[k] for k in ('file','title','format','kind','desc','step','methods')} for _t in _own]
_pr = json.load(open('pairs.json', encoding='utf-8'))
assert set(_pr) == set(_ids), set(_ids) ^ set(_pr)
for _k, _v in _pr.items():
    assert 2 <= len(_v) <= 4, _k
    for _o, _why in _v:
        assert _o in _ids and _o != _k and _why, (_k, _o)
    _ids[_k]['pairs'] = [{'id': _o, 'why': _why} for _o, _why in _v]
_fm = json.load(open('families.json', encoding='utf-8'))
assert set(_fm) == set(_ids), set(_ids) ^ set(_fm)
_FAMS = [
 {'id':'read','name':'Read','evidence':'Artifacts, texts, images, and records','asks':'What exists, what was made, or how something came to be'},
 {'id':'ask','name':'Ask','evidence':'People\u2019s own accounts','asks':'What people say, believe, remember, value, or prefer'},
 {'id':'watch','name':'Watch','evidence':'Observed behavior','asks':'What people actually do, and in what setting'},
 {'id':'test','name':'Test','evidence':'A controlled comparison or a measurement','asks':'Whether one version works better than another, and by how much'},
 {'id':'make','name':'Make','evidence':'Something you or participants made, and the reactions to it','asks':'What is possible, or how people respond to something that does not exist yet'},
 {'id':'analyze','name':'Analyze','evidence':'Data you already have, from any family','asks':'What patterns, structure, or priorities a body of data holds'},
]
_FAMLINES = {
 'read':   ('What already exists, patterns across texts, images, and artifacts, and how a design came to be.', 'How audiences receive something, what people do now, or what causes what.'),
 'ask':    ('Experiences, beliefs, attitudes, and stated reasons and preferences.', 'What people actually do, or the effect of a change.'),
 'watch':  ('How activity unfolds in a real setting, including practice that people cannot describe.', 'Intentions and reasons, unless you also ask, or anything about people you did not watch.'),
 'test':   ('Whether a change moves an outcome, and by how much.', 'Why the effect happens, or whether it holds outside your test.'),
 'make':   ('What is possible, how people respond to something new, and knowledge built into an artifact.', 'A general claim, or an evaluation that is independent of you as the maker.'),
 'analyze':('Patterns, structure, and priorities in data you already collected.', 'Anything the data does not contain. The findings are only as strong as the data.'),
}
for _f in _FAMS:
    _f['show'], _f['limit'] = _FAMLINES[_f['id']]
_MODES = [
 {'id':'into','name':'Into design','gives':'An account of design itself: a history, a pattern across artifacts, or an interpretation.',
  'handIn':'An argument supported by evidence about existing designs.','leans':'Read first, then ask and watch.',
  'drift':'You end with guidelines or a toolkit for designers. That is research for design.',
  'pairs':[
   {'first':{'ids':['artifact-analysis','content-inventory-audit']},'second':{'ids':['interviews'],'note':'with practitioners or experts'},
    'adds':'The artifacts show what was made. The interviews show why, and catch readings you projected onto the work.'},
   {'first':{'ids':['literature-reviews','secondary-research']},'second':{'ids':['artifact-analysis'],'note':'of primary material'},
    'adds':'Published accounts show the received story. The primary artifacts let you check it.'}]},
 {'id':'through','name':'Through design','gives':'Knowledge produced by the act of making.',
  'handIn':'A made artifact plus a documented account of what making it taught you.','leans':'Make, best paired with watch or ask.',
  'drift':'Your research came first and the making only applies it. That is research for design. In research through design, the making is what produced the knowledge.',
  'pairs':[
   {'first':{'lead':'A prototype or probe, such as','ids':['cultural-probes']},'second':{'ids':['observation'],'note':'of people using it'},
    'adds':'Your own account of making is one perspective. Watching use tests it against behavior.'},
   {'first':{'lead':'A co-design or making session, such as','ids':['co-creation-session','design-workshops']},'second':{'ids':['interviews'],'note':'with participants afterward'},
    'adds':'The session produces artifacts. The interviews explain the choices behind them.'}]},
 {'id':'for','name':'For design','gives':'Research that informs a design solution you will produce. The knowledge serves the design.',
  'handIn':'A design solution with the research behind it, or the guidelines, tools, and processes that support making it.','leans':'Read and ask, with testing of materials, tools, or existing solutions.',
  'drift':'You never make anything, and the account of existing work is the end point. That is research into design.',
  'pairs':[
   {'first':{'ids':['interviews']},'second':{'ids':['observation','contextual-inquiry']},
    'adds':'This pair catches the gap between what people say they do and what they do.'},
   {'first':{'ids':['questionnaires-surveys']},'second':{'ids':['interviews','focus-groups']},
    'adds':'The survey shows the spread. The interviews explain the pattern.'},
   {'first':{'ids':['competitive-testing','experiments']},'second':{'ids':['interviews']},
    'adds':'The test shows whether something works. The interviews suggest why.'}]},
]
for _m in _MODES:
    for _p in _m['pairs']:
        for _side in ('first','second'):
            for _i in _p[_side]['ids']:
                assert _i in _ids, _i
_d['modes'] = _MODES
for _k, _v in _fm.items():
    assert _v['family'] in {f['id'] for f in _FAMS} and _v['show'] and _v['limit'], _k
    _ids[_k].update(_v)
_d['families'] = _FAMS
data_json = json.dumps(_d, ensure_ascii=False, indent=1)
assert '</script' not in data_json.lower()

CSS = """
:root{
 --red:#CC0000;--red-dk:#990000;--black:#000;--white:#fff;
 --g50:#fafafa;--g100:#f2f2f2;--g200:#e3e3e3;--g300:#cfcfcf;--g400:#a6a6a6;
 --g600:#636363;--g700:#4a4a4a;--g800:#2e2e2e;--text:#1a1a1a;--gtxt:#5c5c5c;--red-lt:#ff6b6b;
 --research:#fdc907;--rd:#6b5500;--rt:#1a1a1a;
 --insights:#eb5b54;--id:#a8322c;--it:#1a1a1a;
 --ideation:#83bc2c;--idd:#436d00;--idt:#1a1a1a;
 --proto:#4a8ecb;--pd:#15568f;--pt:#1a1a1a;
 --maxw:1360px;
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:Roboto,Helvetica,Arial,sans-serif;color:var(--text);background:#fff;line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
main{flex:1}
main:focus,#d-title:focus{outline:none}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap}
.skip{position:fixed;top:8px;left:8px;z-index:1000;background:#fff;color:#000;font-weight:700;font-size:14px;padding:12px 18px;border-radius:3px;transform:translateY(-300%)}
.skip:focus{transform:none;outline:3px solid var(--red);outline-offset:2px}
ul,ol{list-style:none}
button{font:inherit;color:inherit;background:none;border:none;cursor:pointer}
img{max-width:100%;display:block}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
header.site :focus-visible,.hero :focus-visible,.contrib :focus-visible,footer.site :focus-visible{outline-color:#fff}
.page{display:none;flex-direction:column;min-height:100vh}
.page.on{display:flex}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 32px}

/* HEADER */
header.site{background:var(--black);position:sticky;top:0;z-index:300;box-shadow:0 1px 0 rgba(255,255,255,.08)}
.hbar{height:4px;background:var(--red)}
.hin{max-width:var(--maxw);margin:0 auto;padding:0 32px;height:66px;display:flex;align-items:center;gap:18px}
.logo{display:flex;align-items:center;gap:13px;flex-shrink:0}
.logo img{height:36px;width:auto}
.logo .div{width:1px;height:30px;background:rgba(255,255,255,.22)}
.logo.nologo .div{display:none}
.logo .txt{font-size:12px;color:rgba(255,255,255,.62);line-height:1.35}
.logo .txt b{display:block;color:#fff;font-weight:500;font-size:13px;letter-spacing:.1px}
.srch{flex:1;max-width:340px;position:relative;margin-left:4px}
.srch input{width:100%;padding:9px 32px 9px 35px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.16);
 border-radius:3px;color:#fff;font-size:13.5px;transition:background .15s,border-color .15s}
.srch input::-webkit-search-cancel-button,.srch input::-webkit-search-decoration{-webkit-appearance:none;appearance:none;display:none}
.srch input::placeholder{color:rgba(255,255,255,.68)}
.srch input:focus{background:rgba(255,255,255,.15);border-color:rgba(255,255,255,.7)}
.srch input:focus-visible{outline:3px solid #fff;outline-offset:2px}
.srch svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:rgba(255,255,255,.68);pointer-events:none}
.srch .clr{position:absolute;right:3px;top:50%;transform:translateY(-50%);color:rgba(255,255,255,.78);font-size:20px;line-height:1;width:30px;height:30px;display:none}
.srch .clr:hover{color:#fff}
nav.top{display:flex;align-items:center;margin-left:auto;flex-shrink:0}
nav.top button{font-size:12.5px;font-weight:700;color:rgba(255,255,255,.62);padding:9px 14px;
 border-bottom:3px solid transparent;transition:color .15s}
nav.top button:hover{color:#fff}
nav.top .r{border-bottom-color:var(--research)}
nav.top .i{border-bottom-color:var(--insights)}
nav.top .d{border-bottom-color:var(--ideation)}
nav.top .p{border-bottom-color:var(--proto)}
nav.top .r,nav.top .i,nav.top .d,nav.top .p{color:rgba(255,255,255,.85)}
nav.top .plain:hover{border-bottom-color:rgba(255,255,255,.3)}

/* HERO */
.hero{background:var(--black);color:#fff;padding:76px 0 64px;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;inset:0;pointer-events:none;
 background:radial-gradient(ellipse 50% 70% at 82% 46%,rgba(204,0,0,.085),transparent 72%)}
.hero .wrap{position:relative}
.kicker{font-family:'Roboto Condensed',Roboto,sans-serif;font-size:12px;font-weight:700;letter-spacing:2.2px;
 text-transform:uppercase;color:var(--red);margin-bottom:18px}
.hero h1{font-family:'Roboto Slab',Georgia,serif;font-size:clamp(36px,5.4vw,62px);font-weight:700;line-height:1.05;letter-spacing:-.5px;margin-bottom:22px}
.hero h1 em{font-style:normal;color:var(--red)}
.hero .kicker,.contrib .kicker{color:var(--red-lt)}
.hero p.lede{font-size:16.5px;line-height:1.72;color:rgba(255,255,255,.62);max-width:56ch;margin-bottom:38px}
.chips{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:42px}
.chip{font-family:'Roboto Condensed',sans-serif;font-size:12px;font-weight:700;letter-spacing:1.2px;
 text-transform:uppercase;padding:6px 13px;border-radius:2px;transition:transform .12s}
.chip:hover{transform:translateY(-2px)}
.chip.research{background:var(--research);color:var(--rt)}
.chip.insights{background:var(--insights);color:var(--it)}
.chip.ideation{background:var(--ideation);color:var(--idt)}
.chip.proto{background:var(--proto);color:var(--pt)}
.stats{display:flex;gap:46px;flex-wrap:wrap;border-top:1px solid rgba(255,255,255,.13);padding-top:28px}
.stat b{font-family:'Roboto Condensed',sans-serif;font-size:38px;font-weight:700;line-height:1;display:block}
.stat span{font-size:12px;color:rgba(255,255,255,.7);text-transform:uppercase;letter-spacing:1.1px;margin-top:6px;display:block}

/* FILTER */
.filters{background:#fff;border-bottom:1px solid var(--g200);position:sticky;top:70px;z-index:200}
.filters .in{max-width:var(--maxw);margin:0 auto;padding:0 32px;height:52px;display:flex;align-items:center;gap:8px;overflow-x:auto}
.filters .in.fr{height:46px;border-top:1px solid var(--g100);background:var(--g50);max-width:none;padding:0 max(32px,calc((100vw - var(--maxw))/2 + 32px))}
.flab{font-size:12.5px;font-weight:500;color:var(--g700);white-space:nowrap;flex-shrink:0;margin-right:2px}
.ff{font-size:13px;font-weight:500;padding:5px 13px;border:1px solid var(--g300);border-radius:40px;color:var(--g700);background:#fff;white-space:nowrap;flex-shrink:0;min-height:30px}
.ff:hover{border-color:var(--g600);color:var(--text)}
.ff.on{background:#1a1a1a;color:#fff;border-color:#1a1a1a}
.ff .n{font-size:11.5px;opacity:.8;margin-left:5px}
.fhelp{margin-left:auto;font-size:12.5px;font-weight:500;color:var(--red-dk);text-decoration:underline;text-underline-offset:3px;white-space:nowrap;flex-shrink:0;padding:4px 2px;min-height:28px}
.fpanel{display:none;background:#fff;border-bottom:1px solid var(--g200)}
.fpanel.on{display:block}
.fpanel .in{max-width:var(--maxw);margin:0 auto;padding:18px 32px 22px}
.fpanel p.lead{font-size:14px;color:var(--g700);max-width:78ch;line-height:1.65;margin-bottom:14px}
.fdefs{display:grid;grid-template-columns:repeat(3,1fr);gap:10px 28px}
.fdefs div{font-size:13px;line-height:1.55;color:var(--g700)}
.fdefs b{display:block;font-size:14px;color:var(--text);font-weight:700}
.fnote{background:#eef4fb;border-bottom:1px solid #c9dcf0;padding:10px 0;display:none}
.fnote.on{display:block}
.fnote .in{max-width:var(--maxw);margin:0 auto;padding:0 32px;display:flex;align-items:center;justify-content:space-between;gap:16px;font-size:13.5px;color:var(--g800)}
.fnote button{min-height:28px;padding:0 4px;font-size:12.5px;font-weight:700;color:var(--red-dk);text-decoration:underline;text-underline-offset:3px;white-space:nowrap}
.fb{font-family:'Roboto Condensed',sans-serif;font-size:12.5px;font-weight:700;letter-spacing:.6px;
 text-transform:uppercase;padding:6px 14px;border:1px solid var(--g200);border-radius:40px;color:var(--g600);
 white-space:nowrap;flex-shrink:0;transition:all .14s}
.fb:hover{border-color:var(--g400);color:var(--text)}
.fb.on{color:#fff;border-color:transparent}
.fb.on.all{background:var(--black)}
.fb.on.research{background:var(--research);color:var(--rt)}
.fb.on.insights{background:var(--insights);color:var(--it)}
.fb.on.ideation{background:var(--ideation);color:var(--idt)}
.fb.on.proto{background:var(--proto);color:var(--pt)}
.fcount{margin-left:auto;font-family:'Roboto Condensed',sans-serif;font-size:12px;color:var(--gtxt);white-space:nowrap;flex-shrink:0}
.sbanner{background:#fffbe9;border-bottom:1px solid #f0dc92;padding:11px 0;display:none}
.sbanner.on{display:block}
.sbanner .in{max-width:var(--maxw);margin:0 auto;padding:0 32px;display:flex;align-items:center;justify-content:space-between;gap:16px;font-size:13.5px;color:var(--g700)}
.sbanner button{min-height:28px;padding:0 4px;font-family:'Roboto Condensed',sans-serif;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--red)}
.sbanner button:hover{text-decoration:underline}
mark{background:#ffe9a8;color:inherit;border-radius:2px;padding:0 1px}

/* DOUBLE DIAMOND */
.dd{background:#f4f4f4;padding:84px 0;border-bottom:1px solid var(--g200)}
.dd h2{font-family:'Roboto Slab',Georgia,serif;font-size:clamp(24px,3.1vw,36px);font-weight:700;margin-bottom:16px;letter-spacing:-.3px}
.dd p.intro{font-size:15.5px;line-height:1.78;color:#555;margin-bottom:40px;max-width:76ch}
.dd img.diagram{width:100%;max-width:85%;margin:0 auto 42px;border-radius:8px}
.ddgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--g300);border-radius:6px;overflow:hidden}
.ddc{background:#fff;padding:26px 22px}
.ddc .step{font-family:'Roboto Condensed',sans-serif;font-size:12px;font-weight:700;letter-spacing:1.3px;
 text-transform:uppercase;color:var(--gtxt);margin-bottom:7px}
.ddc .ph{font-family:'Roboto Condensed',sans-serif;font-size:12px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;margin-bottom:5px}
.ddc.research .ph{color:var(--rd)}
.ddc.insights .ph{color:var(--id)}
.ddc.ideation .ph{color:var(--idd)}
.ddc.proto .ph{color:var(--pd)}
.ddc h3{font-family:'Roboto Slab',Georgia,serif;font-size:19px;font-weight:700;margin-bottom:11px}
.ddc p{font-size:13.5px;line-height:1.68;color:#666;margin-bottom:14px}
.ddc .n{font-family:'Roboto Condensed',sans-serif;font-size:12px;color:var(--gtxt)}

/* PHASE SECTIONS */
.phase{padding:64px 0}
.phase+.phase{border-top:1px solid var(--g200)}
.phase.hide,.phase.nomatch{display:none}
#sec-dd,#sec-research,#sec-insights,#sec-ideation,#sec-proto,#sec-sources,#sec-contributors{scroll-margin-top:172px}
/* while searching, results sit directly under the header: no hero, no framework section */
.searching .hero,.searching .dd{display:none}
.searching .phase{padding:30px 0}
.searching .phead{margin-bottom:18px}
.phead{display:flex;align-items:flex-start;justify-content:space-between;gap:26px;margin-bottom:30px;flex-wrap:wrap}
.pleft{display:flex;align-items:center;gap:15px}
.badge{font-family:'Roboto Condensed',sans-serif;font-size:11.5px;font-weight:700;letter-spacing:1.3px;
 text-transform:uppercase;padding:6px 13px;border-radius:2px}
.badge.research{background:var(--research);color:var(--rt)}
.badge.insights{background:var(--insights);color:var(--it)}
.badge.ideation{background:var(--ideation);color:var(--idt)}
.badge.proto{background:var(--proto);color:var(--pt)}
.phead h2{font-family:'Roboto Slab',Georgia,serif;font-size:22px;font-weight:700}
.phead p{font-size:13.5px;color:var(--g600);max-width:46ch;text-align:right;line-height:1.6}

/* CARDS */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:16px;align-items:start}
.card{position:relative;border:1px solid var(--g200);border-radius:5px;overflow:hidden;background:#fff;cursor:pointer;
 display:flex;flex-direction:column;transition:box-shadow .18s,transform .18s,border-color .18s}
.card:hover{box-shadow:0 7px 22px rgba(0,0,0,.1);transform:translateY(-2px);border-color:var(--g300)}
.card .bar{height:4px;flex-shrink:0}
.card .bar.research{background:var(--research)}
.card .bar.insights{background:var(--insights)}
.card .bar.ideation{background:var(--ideation)}
.card .bar.proto{background:var(--proto)}
.card .thumb{aspect-ratio:16/10;background:var(--g100);overflow:hidden}
.card .thumb img{width:100%;height:100%;object-fit:cover}
.card .body{padding:14px 16px;flex:1}
.card .tags{display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap}
.card .ph{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.3px;
 text-transform:uppercase;display:block}
.fam{font-size:11.5px;line-height:1;font-weight:500;color:var(--g700);border:1px solid var(--g300);border-radius:10px;padding:3px 8px;background:#fff;white-space:nowrap}
.card.brief .fam{background:var(--g50)}
.card .ph.research{color:var(--rd)}
.card .ph.insights{color:var(--id)}
.card .ph.ideation{color:var(--idd)}
.card .ph.proto{color:var(--pd)}
.card h3{font-family:'Roboto Slab',Georgia,serif;font-size:15.5px;font-weight:700;line-height:1.24;margin-bottom:7px}
.card p{font-size:12.5px;line-height:1.56;color:var(--g600)}
.card p b{font-weight:500;color:var(--text)}
.card h3 a{color:inherit}
.card h3 a::after{content:"";position:absolute;inset:0;z-index:1}
.card h3 a:focus-visible{outline:none}
.card h3 a:focus-visible::after{outline:3px solid var(--red);outline-offset:-3px;border-radius:5px}
.card .foot{padding:9px 16px;background:var(--g50);border-top:1px solid var(--g200);
 display:flex;align-items:center;justify-content:space-between;gap:8px}
.card .by{font-size:12px;color:var(--g600);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.card .by b{color:var(--text);font-weight:500}
.card .go{font-family:'Roboto Condensed',sans-serif;font-size:10.5px;font-weight:700;letter-spacing:.6px;
 text-transform:uppercase;color:var(--red);flex-shrink:0}
.card.brief{background:var(--g50)}
.card.brief .foot{background:#ececec}
.ref-tag{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:.8px;
 text-transform:uppercase;color:var(--gtxt)}
.empty{grid-column:1/-1;text-align:center;padding:52px 20px;color:var(--gtxt);font-size:14.5px}

/* CONTRIBUTORS */
.contrib{background:var(--black);color:#fff;padding:78px 0}
.contrib h2{font-family:'Roboto Slab',Georgia,serif;font-size:clamp(22px,2.7vw,32px);font-weight:700;margin-bottom:14px}
.contrib p.sub.lead{color:rgba(255,255,255,.82);margin-top:-18px}
.contrib p.sub{font-size:15px;color:rgba(255,255,255,.55);max-width:68ch;line-height:1.72;margin-bottom:40px}
.clist{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:1px;background:rgba(255,255,255,.1);
 border-radius:5px;overflow:hidden}
.cperson{background:#141414;padding:17px 19px}
.cperson .nm{font-family:'Roboto Slab',Georgia,serif;font-size:15px;font-weight:600;margin-bottom:8px}
.cperson ul{display:flex;flex-direction:column;gap:4px}
.cperson li{font-size:13px}
.cperson li a{color:rgba(255,255,255,.74);display:flex;align-items:center;gap:7px;min-height:24px;padding:2px 0}
.cperson li a:hover{color:#fff;text-decoration:underline}
.cperson .dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}

/* SOURCES */
.sources{background:var(--g100);padding:78px 0;border-top:1px solid var(--g200)}
.sources h2{font-family:'Roboto Slab',Georgia,serif;font-size:clamp(21px,2.6vw,30px);font-weight:700;margin-bottom:12px}
.sources p.sub{font-size:14.5px;color:var(--g600);max-width:66ch;line-height:1.7;margin-bottom:40px}
.sgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.scard{background:#fff;border:1px solid var(--g200);border-radius:5px;padding:25px}
.scard h3{font-family:'Roboto Condensed',sans-serif;font-size:12px;font-weight:700;letter-spacing:1.3px;
 text-transform:uppercase;color:var(--red);padding-bottom:11px;border-bottom:2px solid var(--red);margin-bottom:15px}
.scard li{margin-bottom:4px}
.scard a{display:block;padding:4px 0;font-size:13.5px;line-height:1.5;transition:color .14s}
.scard a:hover{color:var(--red);text-decoration:underline}

/* FOOTER */
footer.site{background:var(--black);color:#fff;padding:40px 0;margin-top:auto;border-top:1px solid rgba(255,255,255,.14)}
footer.site .in{max-width:var(--maxw);margin:0 auto;padding:0 32px;display:flex;align-items:center;
 justify-content:space-between;gap:20px;flex-wrap:wrap}
footer .brand{display:flex;align-items:center;gap:14px}
footer .brand .rule{width:4px;height:44px;background:var(--red)}
footer .brand .t{font-family:'Roboto Condensed',sans-serif;font-weight:700;font-size:14.5px;line-height:1.35}
footer .brand .t span{display:block;font-size:12px;font-weight:400;color:rgba(255,255,255,.7);margin-top:3px}
footer .meta{font-size:12px;color:rgba(255,255,255,.7);text-align:right;line-height:1.75}

/* BREADCRUMB */
.bc{background:var(--g50);border-bottom:1px solid var(--g200);padding:6px 0}
.bc .in{max-width:var(--maxw);margin:0 auto;padding:0 32px;display:flex;align-items:center;gap:4px;font-size:12.5px;color:var(--g600);flex-wrap:wrap}
.bc a,.bc button{color:var(--red);font-weight:500;font-size:13px;min-height:28px;padding:0 4px}
.bc a:hover,.bc button:hover{text-decoration:underline}
.bc .sep{color:var(--gtxt)}

/* DETAIL */
.dhero{padding:54px 0}
.dhero.research{background:var(--research)}
.dhero.insights{background:var(--insights)}
.dhero.ideation{background:var(--ideation)}
.dhero.proto{background:var(--proto)}
.dhero .eyebrow{font-family:'Roboto Condensed',sans-serif;font-size:12px;font-weight:700;letter-spacing:1.8px;
 text-transform:uppercase;margin-bottom:13px}
.dhero h1{font-family:'Roboto Slab',Georgia,serif;font-size:clamp(30px,4.4vw,52px);font-weight:700;line-height:1.05;
 letter-spacing:-.5px;margin-bottom:10px}
.dhero .alts{font-size:14px;font-style:italic;margin-bottom:16px}
.dhero .by{font-size:14px}
.dhero .eyebrow,.dhero h1,.dhero .alts,.dhero .by{color:#1a1a1a}
.dhero .actions{margin-top:20px;display:flex;gap:10px;flex-wrap:wrap}
.dhero .actions button{font-size:13px;font-weight:500;color:#1a1a1a;padding:0 14px;min-height:36px;border:1.5px solid #1a1a1a;border-radius:3px}
.dhero .actions button:hover{background:rgba(0,0,0,.12)}
.dbody{max-width:var(--maxw);margin:0 auto;padding:54px 32px}
.dlayout{display:grid;grid-template-columns:minmax(0,1fr) 330px;grid-template-rows:auto 1fr;column-gap:52px;
 grid-template-areas:"main visual" "main side";align-items:start}
#d-main{grid-area:main;min-width:0}#d-visual{grid-area:visual}#d-side{grid-area:side}
.blk{margin-bottom:42px}
.blk h2{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.9px;
 text-transform:uppercase;color:var(--red);padding-bottom:9px;border-bottom:1px solid var(--g200);margin-bottom:17px}
.prose{font-size:16px;line-height:1.75;max-width:72ch}
.wlist li{padding:10px 0;border-bottom:1px solid var(--g100);font-size:14.5px;line-height:1.62;
 display:flex;gap:12px;align-items:flex-start}
.wlist .d{width:6px;height:6px;border-radius:50%;background:var(--red);margin-top:8px;flex-shrink:0}
.slist{counter-reset:s}
.slist li{counter-increment:s;padding:13px 0;border-bottom:1px solid var(--g100);font-size:14.5px;
 line-height:1.65;display:flex;gap:15px;align-items:flex-start}
.slist li::before{content:counter(s);min-width:27px;height:27px;background:var(--red);color:#fff;border-radius:50%;
 display:flex;align-items:center;justify-content:center;font-family:'Roboto Condensed',sans-serif;
 font-weight:700;font-size:12.5px;flex-shrink:0;margin-top:1px}
.tipbox{border-radius:4px;padding:12px 15px;margin-bottom:8px;font-size:13.5px;line-height:1.62}
.tipbox.tip{background:#f1faea;border-left:3px solid var(--ideation)}
.tipbox.mistake{background:#fef1f0;border-left:3px solid var(--insights)}
.tipbox .lab{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.1px;
 text-transform:uppercase;margin-bottom:4px}
.tipbox.tip .lab{color:var(--idd)}
.tipbox.mistake .lab{color:var(--id)}
.exbox{background:var(--g50);border-left:4px solid var(--red);border-radius:0 5px 5px 0;padding:20px 24px}
.exbox p{font-size:14.5px;line-height:1.74;color:var(--g800)}
.cite{padding:11px 0;border-bottom:1px solid var(--g100);font-size:13.5px;line-height:1.6;color:var(--g700)}
.cite a{color:var(--red);word-break:break-word}
.cite a:hover{text-decoration:underline}

/* SIDEBAR */
.sb{margin-bottom:26px}
.sb h2{font-family:'Roboto Condensed',sans-serif;font-size:11.5px;font-weight:700;letter-spacing:1.8px;
 text-transform:uppercase;color:var(--red);padding-bottom:8px;border-bottom:1px solid var(--g200);margin-bottom:13px}
.sb img{width:100%;border-radius:5px;border:1px solid var(--g200)}
.sb figure{margin:0}
.sb button.zoom{display:block;position:relative;width:100%;padding:0;border-radius:5px;cursor:zoom-in;text-align:left}
.sb button.zoom:hover img{border-color:var(--g400)}
.zoomhint{position:absolute;right:10px;bottom:10px;display:flex;align-items:center;gap:6px;background:rgba(0,0,0,.78);color:#fff;
 font-family:'Roboto Condensed',sans-serif;font-size:12px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;padding:6px 10px;border-radius:3px;pointer-events:none}
html.lb-open{overflow:hidden}
dialog.lb{border:none;padding:0;background:transparent;width:100vw;height:100vh;max-width:none;max-height:none;margin:0;color:#fff}
dialog.lb::backdrop{background:rgba(0,0,0,.92)}
dialog.lb[open]{display:flex;align-items:center;justify-content:center}
.lbin{display:flex;flex-direction:column;align-items:center;max-width:96vw;max-height:100vh;padding:56px 0 18px}
.lbscroll{max-width:96vw;max-height:calc(100vh - 170px);overflow:auto;border-radius:3px;-webkit-overflow-scrolling:touch}
.lbin img{display:block;background:#fff;max-width:none;max-height:none;height:auto}
.lbhint{margin-top:10px;font-size:12.5px;color:rgba(255,255,255,.8)}
.lbcap{max-width:min(96vw,760px);margin-top:14px;font-size:13.5px;line-height:1.6;color:rgba(255,255,255,.9);text-align:center;overflow-y:auto;max-height:90px}
.lbcap a{color:#fff;text-decoration:underline;word-break:break-word}
.lbcap .note{display:block;margin-top:3px;font-style:italic;color:rgba(255,255,255,.8)}
.lbx{position:fixed;top:12px;right:14px;width:44px;height:44px;border-radius:50%;background:#fff;color:#000;font-size:26px;line-height:1;display:flex;align-items:center;justify-content:center}
.lbx:hover{background:#e6e6e6}
dialog.lb :focus-visible{outline:3px solid #fff;outline-offset:3px}
@media(prefers-reduced-motion:no-preference){dialog.lb[open] .lbin{animation:lbin .18s ease-out}}
@keyframes lbin{from{opacity:0;transform:scale(.97)}to{opacity:1;transform:none}}
.sb figcaption{font-size:12px;color:var(--g700);margin-top:8px;line-height:1.55}
.sb figcaption a{color:var(--red);word-break:break-word}
.sb figcaption a:hover{text-decoration:underline}
.sb figcaption .note{display:block;margin-top:3px;color:var(--g600);font-style:italic}
.editnote{background:var(--g50);border-left:3px solid var(--g300);padding:12px 16px;margin:22px 0 34px;
 font-size:13px;line-height:1.65;color:var(--g700);border-radius:0 4px 4px 0;max-width:72ch}
.libbox{margin-top:6px}
.libbox li{list-style:none;padding:9px 0;border-bottom:1px solid var(--g100);font-size:13.5px;line-height:1.55;color:var(--g700)}
.libbox li b{font-weight:500;color:var(--g800)}
.libbox li a{display:inline-block;padding:3px 0;color:var(--g800);text-decoration:underline;text-decoration-color:var(--g400);text-underline-offset:3px}
.libbox li a:hover{text-decoration-color:var(--red);color:var(--red-dk)}
.libbox li .gt{display:block;font-size:12.5px;color:var(--gtxt);margin-top:2px}
.ovlist li{list-style:none;padding:11px 0;border-bottom:1px solid var(--g100);font-size:14px;line-height:1.55;color:var(--g700)}
.ovlist li a{display:inline-block;padding:3px 0;font-weight:500;color:var(--g800);text-decoration:underline;text-decoration-color:var(--g400);text-underline-offset:3px}
.ovlist li a:hover{text-decoration-color:var(--red);color:var(--red-dk)}
.ovlist .pub{display:block;font-size:13px;color:var(--gtxt);margin-top:2px}
.pairlist li{list-style:none;padding:10px 0;border-bottom:1px solid var(--g100);font-size:14px;line-height:1.55;color:var(--g700)}
.pairlist button{display:inline-flex;align-items:center;gap:9px;padding:4px 0;font-size:14.5px;font-weight:500;color:var(--g800);cursor:pointer;background:none;border:0;font-family:inherit;text-align:left}
.pairlist .nm{text-decoration:underline;text-decoration-color:var(--g400);text-underline-offset:3px}
.pairlist button:hover{color:var(--red-dk)}
.pairlist button:hover .nm{text-decoration-color:var(--red)}
.pairlist .d{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.pairlist .ph{font-size:12px;font-weight:400;color:var(--gtxt)}
.pairlist .why{display:block;font-size:13px;color:var(--gtxt);margin-top:1px}
.tplist li{list-style:none;padding:11px 0;border-bottom:1px solid var(--g100);font-size:14px;line-height:1.55;color:var(--g700)}
.tplist li a{display:inline-block;padding:3px 0;font-weight:500;color:var(--g800);text-decoration:underline;text-decoration-color:var(--g400);text-underline-offset:3px}
.tplist li a:hover{text-decoration-color:var(--red);color:var(--red-dk)}
.tplist .pub,.tplist .acc,.tplist .on{display:block;font-size:13px;margin-top:2px;color:var(--gtxt)}
.tplist .on{color:var(--g700)}
.ovlist .on{display:block;font-size:13px;color:var(--g700);margin-top:2px}
.prose strong,.wlist strong,.slist strong{font-weight:700;color:var(--text)}
.cite em{font-style:italic}
.ovnote{font-size:12.5px;color:var(--gtxt);margin-top:10px}
.exbox p+p{margin-top:12px}
.showbox{border:1px solid var(--g200);border-radius:5px;overflow:hidden}
.showbox .fh{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:13px 18px;background:var(--g50);border-bottom:1px solid var(--g200);font-size:14px;color:var(--g700);line-height:1.5}
.showbox .fh .fam{font-size:13px;padding:4px 11px;border-color:var(--g400)}
.showbox .fh button{margin-left:auto;font-size:13px;font-weight:500;color:var(--red-dk);text-decoration:underline;text-underline-offset:3px;min-height:28px;padding:2px 0}
.showbox .cols{display:grid;grid-template-columns:1fr 1fr}
.showbox .col{padding:16px 18px;font-size:14.5px;line-height:1.62;color:var(--g800)}
.showbox .col+.col{border-left:1px solid var(--g200)}
.showbox .col .l{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:6px}
.showbox .col.yes .l{color:var(--idd)}
.showbox .col.no .l{color:var(--id)}
.showbox .foot{padding:11px 18px;border-top:1px solid var(--g200);font-size:12.5px;color:var(--gtxt);line-height:1.55}
.cite{display:flex;gap:14px;align-items:flex-start;justify-content:space-between}
.cite .ct{flex:1;min-width:0}
.cpy{flex-shrink:0;font-size:12.5px;font-weight:500;color:var(--red-dk);text-decoration:underline;text-underline-offset:3px;min-height:28px;padding:2px 2px;white-space:nowrap}
.cpy:hover{color:var(--red)}
.cpyall{margin-top:12px;font-size:13px;font-weight:500;color:var(--g800);border:1.5px solid var(--g400);border-radius:3px;padding:0 14px;min-height:36px}
.cpyall:hover{border-color:var(--g800)}
.libbox .cp{display:flex;gap:16px;margin-top:3px;flex-wrap:wrap}
.noimg{background:var(--g100);border:2px dashed var(--g300);border-radius:5px;padding:30px 22px;text-align:center}
.noimg .t{font-family:'Roboto Condensed',sans-serif;font-size:11.5px;font-weight:700;letter-spacing:1.3px;
 text-transform:uppercase;color:var(--g600);margin-bottom:8px}
.noimg p{font-size:12.5px;color:var(--g600);line-height:1.55}
.ddind{background:#111;border-radius:5px;padding:17px}
.ddind .lab{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.4px;
 text-transform:uppercase;color:rgba(255,255,255,.7);margin-bottom:13px}
.ddbars{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:2px}
.ddseg{display:block;background:none;border:0;padding:6px 0 7px;cursor:pointer;border-radius:3px;font:inherit;color:inherit}
.ddseg i{height:9px;border-radius:2px;background:rgba(255,255,255,.12);display:block;margin-bottom:8px;transition:background .15s}
.ddseg i.research,.ddseg i.insights,.ddseg i.ideation,.ddseg i.proto{background:#c4c4c4}
.ddseg i.on.research{background:var(--research)}
.ddseg i.on.insights{background:var(--insights)}
.ddseg i.on.ideation{background:var(--ideation)}
.ddseg i.on.proto{background:var(--proto)}
.ddseg span{display:block;font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:.2px;
 color:rgba(255,255,255,.78);text-align:center;text-decoration:underline;text-decoration-color:rgba(255,255,255,.28);text-underline-offset:3px}
.ddseg.on span{color:#fff}
.ddseg:hover span{color:#fff;text-decoration-color:#fff}
.ddseg:hover i{filter:brightness(1.35)}
.ddseg:focus-visible{outline:2px solid #fff;outline-offset:2px}
.ddhelp{font-size:11.5px;color:rgba(255,255,255,.72);text-align:center;margin-top:6px}
.ddnote{font-size:12px;color:rgba(255,255,255,.72);line-height:1.6;margin-top:12px;padding-top:12px;
 border-top:1px solid rgba(255,255,255,.09)}
.nlist li{padding:7px 0;border-bottom:1px solid var(--g100);font-size:13px;line-height:1.5;
 display:flex;gap:9px;align-items:flex-start}
.nlist .d{width:5px;height:5px;border-radius:50%;background:var(--g400);margin-top:7px;flex-shrink:0}
.more{display:flex;flex-direction:column;gap:2px}
.more button{padding:8px 11px;border-radius:4px;font-size:13px;display:flex;align-items:center;gap:9px;
 text-align:left;width:100%;transition:background .12s}
.more button:hover{background:var(--g100);color:var(--red)}
.more .d{width:5px;height:5px;border-radius:50%;flex-shrink:0}
.more .ovf{font-size:12px;color:var(--gtxt);padding:7px 11px;font-style:italic}
.seeall{min-height:28px;margin-top:6px;font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;
 letter-spacing:.6px;text-transform:uppercase;color:var(--red);padding:5px 0}
.seeall:hover{text-decoration:underline}
.refbox{background:var(--g50);border:1px solid var(--g200);border-radius:5px;padding:19px 21px}
.refbox .l{font-family:'Roboto Condensed',sans-serif;font-size:11.5px;font-weight:700;letter-spacing:1.4px;
 text-transform:uppercase;color:var(--g600);margin-bottom:9px}
.refbox p{font-size:13.5px;line-height:1.65;color:var(--g800);margin-bottom:13px}
.refbox a{display:inline-block;background:var(--red);color:#fff;padding:9px 17px;border-radius:3px;
 font-family:'Roboto Condensed',sans-serif;font-size:12px;font-weight:700;letter-spacing:.7px;text-transform:uppercase}
.refbox a:hover{background:var(--red-dk)}
.refbox p.gate{font-size:12.5px;color:var(--g700);margin:11px 0 0}
.notice{background:#fffbe9;border:1px solid #f0dc92;border-radius:5px;padding:16px 19px;font-size:13.5px;
 line-height:1.65;color:var(--g700);margin-bottom:34px}


/* PLAN PAGE */
nav.top .plan{border-bottom-color:var(--red-lt);color:#fff}
.shortcount{display:none;margin-left:7px;min-width:20px;padding:1px 6px;border-radius:10px;background:var(--red);color:#fff;font-size:11.5px;font-weight:700;line-height:1.5;text-align:center}
.shortcount.on{display:inline-block}
.planbtn{display:none;margin-left:auto;font-size:12.5px;font-weight:700;color:#fff;padding:9px 12px;border-bottom:3px solid var(--red-lt);flex-shrink:0}
.phero{background:var(--black);color:#fff;padding:60px 0 44px}
.phero .kicker{color:var(--red-lt)}
.phero h1{font-family:'Roboto Slab',Georgia,serif;font-size:clamp(32px,4.6vw,52px);font-weight:700;line-height:1.08;letter-spacing:-.4px;margin-bottom:18px}
.phero h1:focus{outline:none}
.phero .lede{font-size:16.5px;line-height:1.7;color:rgba(255,255,255,.72);max-width:60ch;margin-bottom:28px}
.pjump{display:flex;gap:10px;flex-wrap:wrap}
.pjump button{font-size:13.5px;font-weight:500;color:#fff;border:1.5px solid rgba(255,255,255,.5);border-radius:3px;padding:0 16px;min-height:40px}
.pjump button:hover{border-color:#fff;background:rgba(255,255,255,.08)}
.phero :focus-visible{outline-color:#fff}
.psec{padding:64px 0;border-bottom:1px solid var(--g200);scroll-margin-top:80px}
.psec.alt{background:#f4f4f4}
#plan-q,#plan-pair,#plan-short{scroll-margin-top:80px}
.psec h2{font-family:'Roboto Slab',Georgia,serif;font-size:clamp(22px,2.7vw,30px);font-weight:700;margin-bottom:12px;letter-spacing:-.2px}
.psec p.sub{font-size:15.5px;line-height:1.72;color:var(--g700);max-width:72ch;margin-bottom:28px}
.psec p.sub.s2{margin-bottom:18px}
.btlist{list-style:none;margin:0 0 22px;padding:0;max-width:72ch}
.btlist li{padding:11px 0 11px 18px;border-bottom:1px solid var(--g200);font-size:15px;line-height:1.65;color:var(--g800);position:relative}
.btlist li:before{content:"";position:absolute;left:0;top:21px;width:7px;height:7px;background:var(--red)}
.btlist li b{font-weight:700;color:var(--black)}
.bttools{margin:6px 0 0;font-size:14px;line-height:1.6;color:var(--g700)}
.bttools .lbl{font-weight:700;color:var(--black);margin-right:8px}
.bttools a{display:inline-block;margin:0 14px 0 0;padding:5px 0;font-weight:500;color:var(--g800);text-decoration:underline;text-decoration-color:var(--g400);text-underline-offset:3px}
.bttools a:hover{text-decoration-color:var(--red);color:var(--red-dk)}
.btnext{margin-top:14px}
.btnext button{font-size:14px;font-weight:700;color:var(--red-dk);border-bottom:2px solid var(--red);padding:6px 0}
.btnext button:hover{color:var(--black)}
table.bttab{border-collapse:collapse;width:100%;max-width:860px;margin:6px 0 20px;font-size:14.5px;line-height:1.55}
table.bttab th{text-align:left;background:var(--black);color:#fff;font-weight:700;padding:9px 12px}
table.bttab td{padding:10px 12px;border-bottom:1px solid var(--g200);vertical-align:top;color:var(--g800)}
.btall{list-style:none;margin:0;padding:0;max-width:860px}
.btall li{display:grid;grid-template-columns:minmax(0,1fr);gap:2px;padding:14px 0;border-bottom:1px solid var(--g200)}
.btall .tt a{font-size:16px;font-weight:700;color:var(--black);text-decoration:underline;text-decoration-color:var(--red);text-underline-offset:3px}
.btall .tt a:hover{color:var(--red-dk)}
.btall .tf{font-size:12.5px;color:var(--gtxt)}
.btall .td{font-size:14.5px;line-height:1.6;color:var(--g700);max-width:68ch}
.btnote{font-size:13.5px;line-height:1.6;color:var(--g700);max-width:72ch;margin-top:18px;padding:12px 14px;border-left:3px solid var(--red);background:var(--g50)}
.ph3{font-family:'Roboto Slab',Georgia,serif;font-size:19px;font-weight:700;margin-bottom:8px}
.ph3.gap{margin-top:52px;padding-top:36px;border-top:1px solid var(--g300)}
.qopts{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:6px}
.qopts.modes{grid-template-columns:repeat(3,1fr)}
.qopt{position:relative;display:block;background:#fff;border:1.5px solid var(--g300);border-radius:5px;padding:16px 18px 16px 46px;cursor:pointer;font-size:14.5px;line-height:1.55;color:var(--g800)}
.qopt:hover{border-color:var(--g600)}
.qopt input{position:absolute;left:17px;top:19px;width:18px;height:18px;accent-color:#CC0000;margin:0}
.qopt b{display:block;font-size:15px;font-weight:700;color:var(--text);margin-bottom:3px}
.qopt .ev{display:block;font-size:13px;color:var(--gtxt);margin-top:5px}
.qopt:has(input:checked){border-color:#1a1a1a;box-shadow:inset 0 0 0 1px #1a1a1a;background:#fff}
.qopt:has(input:focus-visible){outline:3px solid var(--red);outline-offset:2px}
.qres{margin-top:26px}
.qres:empty{display:none}
.rbox{background:#fff;border:1px solid var(--g300);border-radius:5px;padding:24px 26px}
.rbox h3{font-family:'Roboto Slab',Georgia,serif;font-size:20px;font-weight:700;margin-bottom:8px}
.rbox p{font-size:14.5px;line-height:1.65;color:var(--g800);max-width:80ch}
.rbox p+p{margin-top:8px}
.rbox .lab{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;color:var(--red);margin:20px 0 8px}
.warnbox{background:#fffbe9;border:1px solid #f0dc92;border-radius:4px;padding:13px 16px;font-size:14px;line-height:1.62;color:var(--g800);margin-top:14px;max-width:80ch}
.warnbox b{font-weight:700}
.okbox{background:#f1faea;border:1px solid #c5e3a5;border-radius:4px;padding:13px 16px;font-size:14px;line-height:1.62;color:var(--g800);margin-top:14px;max-width:80ch}
.sbtn{font-size:12.5px;font-weight:500;color:var(--g800);border:1.5px solid var(--g400);border-radius:3px;padding:0 11px;min-height:30px;white-space:nowrap;flex-shrink:0;background:#fff}
.sbtn:hover{border-color:var(--g800)}
.sbtn.on{background:#1a1a1a;color:#fff;border-color:#1a1a1a}
.dhero .actions .sbtn{background:transparent;border:1.5px solid #1a1a1a;color:#1a1a1a;font-size:13px;min-height:36px;padding:0 14px;border-radius:3px}
.dhero .actions .sbtn:hover{background:rgba(0,0,0,.12)}
.dhero .actions .sbtn.on{background:#1a1a1a;color:#fff}
.herocta{margin:-14px 0 34px}
.navbefore{white-space:nowrap}
@media(max-width:1180px){.navbefore{display:none!important}}
.herocta{display:flex;gap:10px;flex-wrap:wrap}
.herobtn{font-size:14px;font-weight:700;color:#fff;border:1.5px solid rgba(255,255,255,.6);border-radius:3px;padding:0 20px;min-height:44px}
.herobtn:hover{border-color:#fff;background:rgba(255,255,255,.1)}
.mlist li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 16px;align-items:start;padding:12px 0;border-bottom:1px solid var(--g100)}
.mlist li:first-child{border-top:1px solid var(--g100)}
.mlist .nm{display:inline-flex;align-items:center;gap:9px;font-size:15px;font-weight:500;color:var(--g800);text-align:left;padding:2px 0;min-height:28px}
.mlist .nm span.t{text-decoration:underline;text-decoration-color:var(--g400);text-underline-offset:3px}
.mlist .nm:hover{color:var(--red-dk)}
.mlist .nm:hover span.t{text-decoration-color:var(--red)}
.mlist .d{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.mlist .ph{font-size:12px;font-weight:400;color:var(--gtxt)}
.mlist .sl{grid-column:1;font-size:13px;color:var(--g700);line-height:1.5}
.mlist .sl b{font-weight:500;color:var(--text)}
.mlist li .sbtn{grid-column:2;grid-row:1}
.morebtn{margin-top:14px;font-size:13.5px;font-weight:500;color:var(--red-dk);text-decoration:underline;text-underline-offset:3px;min-height:32px}
.prec{border-top:1px solid var(--g200);padding:16px 0}
.prec:first-of-type{border-top:0;padding-top:4px}
.prec .eq{display:flex;gap:10px 14px;flex-wrap:wrap;align-items:center;font-size:15px;color:var(--g800)}
.prec .eq .plus{font-weight:700;color:var(--gtxt)}
.prec .eq .mn{display:inline-flex;align-items:center;gap:7px;font-weight:500;padding:3px 0;min-height:28px;color:var(--g800)}
.prec .eq .mn span.t{text-decoration:underline;text-decoration-color:var(--g400);text-underline-offset:3px}
.prec .eq .mn:hover{color:var(--red-dk)}
.prec .eq .d{width:8px;height:8px;border-radius:50%}
.prec .eq .fam{margin-left:1px}
.prec .add{margin-top:6px;font-size:13.5px;color:var(--g700);line-height:1.6;max-width:80ch}
.prec .sbs{margin-top:10px}
.mfacts{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--g300);border:1px solid var(--g300);border-radius:5px;overflow:hidden;margin:14px 0 4px}
.mfacts div{background:#fff;padding:12px 14px;font-size:13.5px;line-height:1.55;color:var(--g800)}
.mfacts .l{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;color:var(--gtxt);display:block;margin-bottom:4px}
.chkform{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:760px;margin-top:14px}
.fld label{display:block;font-size:13.5px;font-weight:500;margin-bottom:6px;color:var(--g800)}
.fld select{width:100%;min-height:44px;padding:8px 10px;font:inherit;font-size:14.5px;border:1.5px solid var(--g400);border-radius:4px;background:#fff;color:var(--text)}
.fld select:focus-visible,.fld textarea:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.sentence{margin-top:16px;max-width:80ch}
.sentence label{display:block;font-size:14px;font-weight:500;margin-bottom:6px}
.sentence textarea{width:100%;min-height:78px;padding:10px 12px;font:inherit;font-size:14.5px;line-height:1.55;border:1.5px solid var(--g400);border-radius:4px;resize:vertical}
.sentence .row{display:flex;gap:10px;margin-top:8px;flex-wrap:wrap}
.btn2{font-size:13.5px;font-weight:500;color:var(--g800);border:1.5px solid var(--g400);border-radius:3px;padding:0 14px;min-height:38px;background:#fff}
.btn2:hover{border-color:var(--g800)}
.btn2.solid{background:#1a1a1a;color:#fff;border-color:#1a1a1a}
.sempty{background:#fff;border:2px dashed var(--g300);border-radius:5px;padding:30px 24px;text-align:center;font-size:14.5px;color:var(--g700);line-height:1.65}
.stable{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--g300);font-size:13.5px;line-height:1.55}
.stable th{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;color:var(--gtxt);text-align:left;padding:11px 14px;background:var(--g50);border-bottom:1px solid var(--g300);vertical-align:bottom}
.stable td{padding:13px 14px;border-bottom:1px solid var(--g200);vertical-align:top;color:var(--g800)}
.stable td.mn button{font-size:14.5px;font-weight:700;text-align:left;text-decoration:underline;text-decoration-color:var(--g400);text-underline-offset:3px;padding:2px 0;min-height:28px;color:var(--text)}
.stable td.mn button:hover{color:var(--red-dk)}
.stable .ph{display:block;font-size:12px;color:var(--gtxt);margin-top:2px}
.stable .rm{font-size:12.5px;font-weight:500;color:var(--red-dk);text-decoration:underline;text-underline-offset:3px;min-height:28px}
.sact{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.scover{margin-top:18px;font-size:14.5px;line-height:1.65;max-width:80ch;color:var(--g800)}
.sstore{font-size:12.5px;color:var(--gtxt);margin-top:14px}
.tblwrap{overflow-x:auto}

@media(max-width:980px){
 .planbtn{display:block}
 .qopts,.qopts.modes{grid-template-columns:1fr}
 .mfacts{grid-template-columns:1fr 1fr}
 .dlayout{grid-template-columns:minmax(0,1fr);grid-template-rows:none;grid-template-areas:"visual" "main" "side"}
 .sgrid,.ddgrid{grid-template-columns:1fr 1fr}
 nav.top{display:none}
 .srch{max-width:none}
 .phead p{text-align:left}
}
@media(max-width:640px){
 .chkform{grid-template-columns:1fr}
 .mfacts{grid-template-columns:1fr}
 .mlist li{grid-template-columns:1fr}
 .mlist li .sbtn{grid-column:1;grid-row:auto;justify-self:start}
 .stable,.stable tbody,.stable tr,.stable td{display:block}
 .stable thead{display:none}
 .stable tr{border-bottom:1px solid var(--g300);padding:10px 0}
 .stable td{border:0;padding:5px 14px}
 .stable td[data-l]::before{content:attr(data-l) ': ';font-weight:700;color:var(--text)}
 .stable td.mn::before{content:none}
 .rbox{padding:18px 16px}
 .showbox .cols{grid-template-columns:1fr}
 .showbox .col+.col{border-left:0;border-top:1px solid var(--g200)}
 .fdefs{grid-template-columns:1fr}
 .filters .in.fr{padding-left:18px;padding-right:18px}
 .fpanel .in,.fnote .in{padding-left:18px;padding-right:18px}
 .cite{flex-direction:column;gap:2px}
 .wrap,.hin,.filters .in,.bc .in,footer.site .in,.sbanner .in{padding-left:18px;padding-right:18px}
 .dbody{padding:30px 18px}
 .sgrid,.ddgrid,.clist{grid-template-columns:1fr}
 .stats{gap:26px}
 .grid{grid-template-columns:repeat(2,1fr)}
 .dd img.diagram{max-width:100%}
 .logo .txt{display:none}
 .hero{padding:44px 0 40px}
 .dhero{padding:28px 0}
 .dhero .actions button{min-height:40px}
}
@media(max-width:420px){.grid{grid-template-columns:1fr}}
@media print{
 header.site,.filters,.sbanner,.fnote,.fpanel,footer.site,.bc,.skip,.actions,.more,.seeall,#p-home,dialog.lb,.zoomhint,.cpy,.cpyall,.sbtn{display:none!important}
 #p-detail{display:block!important}
 #p-detail:not(.on),#p-plan:not(.on),#p-before:not(.on){display:none!important}
 #p-before.on{display:block!important}
 #p-before .phero,#p-before .bttools,#p-before .btnext{display:none!important}
 #p-plan.on{display:block!important}
 #p-plan .phero,#p-plan #plan-q,#p-plan #plan-pair,#p-plan .sact{display:none!important}
 #p-plan .psec{padding:0;border:0}
 body{color:#000;background:#fff}
 .dhero{background:none!important;padding:0 0 14px;border-bottom:2px solid #000}
 .dhero *{color:#000!important}
 .dbody{padding:18px 0;max-width:none}
 .dlayout{display:block}
 .sb,.blk,.cite,.tipbox,.exbox,.showbox{break-inside:avoid}
 .sb img{max-width:70%}
 .cite a,.sb figcaption a{color:#000}
 .ddind{background:none;border:1px solid #999}
 .ddind *{color:#000!important}
}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}html{scroll-behavior:auto}}
"""

JS = r"""
var APP = JSON.parse(document.getElementById('app-data').textContent);
var M = APP.methods, PC = APP.phaseConfig, PCOL = APP.phaseColor;
var BY = {}; M.forEach(function(m){ BY[m.id] = m; });
var phase = 'all', fam = 'all', query = '', ALTS = [], cur = 'research';
var FAMS = APP.families, FAM = {}; FAMS.forEach(function(f){ FAM[f.id] = f; });
var PHASES = ['research','insights','ideation','proto'];
var SITE_TITLE = document.title;
var shownKey = null, savedY = 0, savedId = '', annTimer = null;

function q(id){ return document.getElementById(id); }
function el(tag, cls, txt){
  var e = document.createElement(tag);
  if (cls) e.className = cls;
  if (txt != null) e.textContent = txt;
  return e;
}
/* **bold** and *italic* markup in card text; everything else stays plain text */
function plain(s){ return String(s == null ? '' : s).replace(/\*+/g, ''); }
function rich(parent, text){
  String(text == null ? '' : text).split(/(\*\*[^*]+\*\*|\*[^*]+\*)/).forEach(function(p){
    if (!p) return;
    if (p.slice(0,2) === '**' && p.length > 4) parent.appendChild(el('strong', null, p.slice(2,-2)));
    else if (p.charAt(0) === '*' && p.length > 2) parent.appendChild(el('em', null, p.slice(1,-1)));
    else parent.appendChild(document.createTextNode(p));
  });
  return parent;
}
function esc(s){ var d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; }
function mark(text, alt){
  if (!alt) return esc(text);
  return String(text).split(/([A-Za-z0-9]+)/).map(function(part, i){
    return (i % 2 === 1 && Search.wordHit(part, alt)) ? '<mark>' + esc(part) + '<\/mark>' : esc(part);
  }).join('');
}
function announce(msg, delay){
  clearTimeout(annTimer);
  annTimer = setTimeout(function(){ q('status').textContent = msg; }, delay == null ? 400 : delay);
}
function reduced(){ return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
function jumpTo(y){ window.scrollTo({top:y, left:0, behavior:'instant'}); }

/* ---------- navigation (hash routes: #method-id) ---------- */
function methodFromHash(){
  var h = location.hash.replace(/^#\/?/, '');
  try { h = decodeURIComponent(h); } catch(e){}
  return BY[h] || null;
}
function clearHash(){ if (location.hash) history.pushState(null, '', location.pathname + location.search); }
function pageFromHash(){ return methodFromHash() ? '' : location.hash.replace(/^#\/?/, ''); }
function planFromHash(){ return pageFromHash() === 'plan'; }
function beforeFromHash(){ return pageFromHash() === 'before'; }
function openBefore(){
  if (!shownKey){ savedY = window.scrollY || 0; savedId = ''; }
  if (beforeFromHash()) route({force:true}); else location.hash = 'before';
}
function openPlan(){
  if (!shownKey){ savedY = window.scrollY || 0; savedId = ''; }
  if (planFromHash()) route({force:true}); else location.hash = 'plan';
}
var BT_SECTIONS = {
  'bt-plan': ['research-plan','planning-matrix'],
  'bt-analysis': ['codebook'],
  'bt-consent': ['consent-script'],
  'bt-protocol': ['interview-guide','observation-notes','deviation-and-recruitment-log'],
  'bt-numbers': ['deviation-and-recruitment-log','codebook'],
  'bt-name': ['method-justification']
};
function btFile(t){ return t.file.replace(/^templates\//,'').replace(/\.[a-z]+$/,''); }
var btDone = false;
function renderBefore(){
  if (btDone) return; btDone = true;
  var T = APP.ownTemplates || [];
  function dl(t){
    var a = document.createElement('a'); a.href = t.file; a.setAttribute('download','');
    a.appendChild(document.createTextNode(t.title));
    a.appendChild(el('span','sr',' (downloads a ' + t.format.toLowerCase() + ')'));
    return a;
  }
  Object.keys(BT_SECTIONS).forEach(function(sid){
    var host = q(sid + '-tools'); if (!host) return;
    host.appendChild(el('span','lbl','Templates:'));
    BT_SECTIONS[sid].forEach(function(k){
      T.forEach(function(t){ if (btFile(t) === k) host.appendChild(dl(t)); });
    });
  });
  var ul = q('bt-all');
  T.forEach(function(t){
    var li = el('li'), tt = el('div','tt'); tt.appendChild(dl(t));
    li.appendChild(tt);
    li.appendChild(el('div','tf', t.format + '. Used at the ' + t.step.toLowerCase() + ' step.'));
    li.appendChild(el('div','td', t.desc));
    ul.appendChild(li);
  });
}
function route(o){
  o = o || {};
  var m = methodFromHash(), isPlan = planFromHash(), isBefore = beforeFromHash(),
      key = m ? m.id : (isPlan ? '~plan' : (isBefore ? '~before' : ''));
  if (key === shownKey && !o.force) return;
  closeLightbox();
  var wasDetail = !!shownKey;
  shownKey = key;
  if (m){
    cur = m.phase; detail(m);
    q('p-home').classList.remove('on'); q('p-plan').classList.remove('on'); q('p-before').classList.remove('on'); q('p-detail').classList.add('on');
    document.title = m.name + ' | ' + SITE_TITLE;
    jumpTo(0);
    q('d-title').focus({preventScroll:true});
  } else if (isPlan){
    q('p-home').classList.remove('on'); q('p-detail').classList.remove('on'); q('p-before').classList.remove('on'); q('p-plan').classList.add('on');
    document.title = 'Plan your research | ' + SITE_TITLE;
    jumpTo(0);
    q('plan-title').focus({preventScroll:true});
  } else if (isBefore){
    q('p-home').classList.remove('on'); q('p-detail').classList.remove('on'); q('p-plan').classList.remove('on'); q('p-before').classList.add('on');
    document.title = 'Before you collect | ' + SITE_TITLE;
    renderBefore();
    jumpTo(0);
    q('before-title').focus({preventScroll:true});
  } else {
    q('p-detail').classList.remove('on'); q('p-plan').classList.remove('on'); q('p-before').classList.remove('on'); q('p-home').classList.add('on');
    document.title = SITE_TITLE;
    if (o.top){ jumpTo(0); }
    else if (wasDetail){
      jumpTo(savedY);
      var a = document.querySelector('.card[data-id="' + savedId + '"] h3 a');
      if (a) a.focus({preventScroll:true});
    }
  }
}
function home(){ clearHash(); route({top:true, force:true}); }
function homePhase(){ setPhase(cur); }
function open(id){
  if (!BY[id]) return;
  if (!shownKey){ savedY = window.scrollY || 0; savedId = id; }
  if (location.hash.replace(/^#\/?/, '') === id) route({force:true}); else location.hash = id;
}
function go(id){ var e = q(id); if (e) e.scrollIntoView({behavior: reduced() ? 'auto' : 'smooth'}); }
function skipTo(id){ var e = q(id); if (e) e.focus(); return false; }
/* ---------- enlarged image ---------- */
var lbTrigger = null;
function lbSize(){
  var im = q('lb-img'); if (!im.naturalWidth) return;
  var vw = window.innerWidth * 0.96, vh = window.innerHeight - 170;
  var fit = Math.min(vw / im.naturalWidth, vh / im.naturalHeight);
  var scale = Math.min(fit, 2);
  if (window.innerWidth < 700) scale = Math.max(fit, Math.min(1, 1.9 * vw / im.naturalWidth));
  im.style.width = Math.round(im.naturalWidth * scale) + 'px';
  var sc = q('lb-scroll'), over = sc.scrollWidth > sc.clientWidth + 2 || sc.scrollHeight > sc.clientHeight + 2;
  q('lb-hint').hidden = !over;
  if (over){ sc.tabIndex = 0; sc.setAttribute('aria-label', 'Enlarged image, scrollable'); } else { sc.removeAttribute('tabindex'); sc.removeAttribute('aria-label'); }
}
function openLightbox(m, trigger, caption){
  var d = q('lb'), im = q('lb-img');
  lbTrigger = trigger;
  d.setAttribute('aria-label', 'Larger image for ' + m.name);
  im.style.width = ''; im.alt = m.imageAlt || (m.name + ' in practice');
  im.onload = lbSize; im.src = m.image;
  var cap = q('lb-cap'); cap.innerHTML = ''; cap.appendChild(caption.cloneNode(true));
  document.documentElement.classList.add('lb-open');
  d.showModal();
  if (im.complete) lbSize();
}
function closeLightbox(){ var d = q('lb'); if (d.open) d.close(); }
function copyLink(){
  var b = q('b-copy');
  function done(ok){
    b.textContent = ok ? 'Link copied' : 'Copy failed';
    announce(ok ? 'Link copied' : 'Could not copy. Copy the address from the browser address bar.', 50);
    setTimeout(function(){ b.textContent = 'Copy link'; }, 2200);
  }
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(location.href).then(function(){ done(true); }, function(){ done(false); });
  } else {
    try {
      var t = document.createElement('textarea'); t.value = location.href; document.body.appendChild(t); t.select();
      var ok = document.execCommand('copy'); document.body.removeChild(t); done(ok);
    } catch(e){ done(false); }
  }
}

/* ---------- search & filter ---------- */
var vocabReady = false;
function ensureVocab(){
  if (vocabReady) return;
  Search.setVocab(M.map(function(m){ return idx(m).all; }));
  vocabReady = true;
}
function search(v){
  ensureVocab();
  query = v.trim().toLowerCase();
  ALTS = query ? Search.alternatives(Search.tokenize(query)) : [];
  var home = q('p-home'), wasSearching = home.classList.contains('searching');
  if (query && fam !== 'all') setFam('all', true);
  home.classList.toggle('searching', !!query);
  if (query !== '' && !wasSearching) jumpTo(0);
  if (query === '' && wasSearching) jumpTo(0);
  q('clr').style.display = query ? 'block' : 'none';
  if (query){
    PHASES.forEach(function(p){ q('sec-'+p).classList.remove('hide'); });
    document.querySelectorAll('.fb').forEach(function(b){ b.classList.remove('on'); b.setAttribute('aria-pressed','false'); });
    q('fb-all').classList.add('on'); q('fb-all').setAttribute('aria-pressed','true'); phase = 'all';
  }
  render(); banner();
}
function clearSearch(){
  q('search').value = ''; query = ''; ALTS = [];
  if (q('p-home').classList.contains('searching')){ q('p-home').classList.remove('searching'); jumpTo(0); }
  q('clr').style.display = 'none';
  render(); banner();
}
function setPhase(p){
  if (query) clearSearch();
  phase = p;
  document.querySelectorAll('.fb').forEach(function(b){
    var on = b.dataset.phase === p;
    b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
  PHASES.forEach(function(x){ q('sec-'+x).classList.toggle('hide', !(p==='all' || p===x)); });
  if (shownKey){ clearHash(); route(); }
  if (fam !== 'all') setFam(fam, true);
  render();
  var n = p==='all' ? M.filter(function(m){ return fam==='all' || m.family===fam; }).length : M.filter(function(m){ return m.phase===p && (fam==='all' || m.family===fam); }).length;
  announce(p==='all' ? 'Showing all ' + n + ' methods' : 'Showing ' + n + ' ' + PC[p].name + ' methods');
  if (p !== 'all') setTimeout(function(){ go('sec-'+p); }, 70);
}

function famCount(f){ return M.filter(function(m){ return (f==='all' || m.family===f) && (phase==='all' || m.phase===phase); }).length; }
function setFam(f, quiet){
  if (!quiet && query) clearSearch();
  fam = f;
  document.querySelectorAll('.ff').forEach(function(b){
    var on = b.dataset.fam === f; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
  var note = q('fnote');
  if (f === 'all'){ note.classList.remove('on'); }
  else {
    var n = famCount(f), F = FAM[f];
    q('fnote-text').textContent = 'Showing ' + n + (n===1 ? ' method' : ' methods') + ' in the ' + F.name + ' family. Evidence: ' + F.evidence.toLowerCase() + '.' + (n === 0 ? ' No methods match this phase and family together.' : '');
    note.classList.add('on');
  }
  if (!quiet){
    if (shownKey){ clearHash(); route(); }
    render();
    announce(f==='all' ? 'Showing all families' : 'Showing ' + famCount(f) + ' ' + FAM[f].name + ' methods');
    if (f !== 'all') setTimeout(function(){ var first = PHASES.filter(function(p){ return !q('sec-'+p).classList.contains('hide') && !q('sec-'+p).classList.contains('nomatch'); })[0]; if (first) go('sec-'+first); }, 70);
  }
}
function toggleFamHelp(){
  var pnl = q('fpanel'), b = q('fhelp'), on = !pnl.classList.contains('on');
  pnl.classList.toggle('on', on); b.setAttribute('aria-expanded', on ? 'true' : 'false');
}

/* full-text index: every field of a card is searchable, with word forms and related terms */
function idx(m){
  if (m._ix) return m._ix;
  var join = function(a){ return plain((a || []).join(' ')); };
  var fields = [
    ['Description', plain(m.whatItIs)],
    ['When to use it', join(m.whenToUse)],
    ['Steps', join(m.howToDoIt)],
    ['What you need', join(m.whatYouNeed)],
    ['Tips', join(m.tips)],
    ['Common mistakes', join(m.mistakes)],
    ['Example', plain(m.example)],
    ['Sources', join(m.sources)]
  ];
  var head = Search.block(m.name + ' ' + join(m.altNames));
  var who = Search.block(m.student || '');
  var fb = fields.map(function(f){ return Search.block(f[1]); });
  m._ix = {fields: fields, head: head, fb: fb,
           hw: Search.merge([head, who]), hwd: Search.merge([head, who, fb[0]]),
           all: Search.merge([head, who].concat(fb))};
  return m._ix;
}
/* best way this card matches the search (typed words first, related terms second), or null */
function evalCard(m){
  if (!query) return {rank: 0, alt: null};
  var x = idx(m), best = null;
  ALTS.forEach(function(a){
    if (!Search.hasAll(x.all, a)) return;
    var r = Search.hasAll(x.head, a) ? 0 : Search.hasAll(x.hw, a) ? 1 : Search.hasAll(x.hwd, a) ? 2 : 3;
    r += a.pen;
    if (best === null || r < best.rank) best = {rank: r, alt: a};
  });
  return best;
}
function hit(m){ return !query || evalCard(m) !== null; }
function excerpt(m, alt){
  /* shows where in the card a body match sits; null when the card snippet already shows it */
  var x = idx(m);
  for (var i = 0; i < x.fields.length; i++){
    var text = x.fields[i][1], at = Search.findPos(text.toLowerCase(), alt);
    if (at === -1) continue;
    if (i === 0 && at < 100) return null;
    var from = Math.max(0, at - 55), to = Math.min(text.length, at + 90);
    return {label: x.fields[i][0], text: (from > 0 ? '… ' : '') + text.slice(from, to).trim() + (to < text.length ? ' …' : '')};
  }
  return null;
}
function banner(){
  var b = q('sbanner');
  if (!query){ b.classList.remove('on'); count(); return; }
  var n = 0, labels = [];
  M.forEach(function(m){
    var ev = evalCard(m);
    if (!ev) return;
    n++;
    if (!Search.hasAll(idx(m).all, ALTS[0]) && ev.alt.label && labels.indexOf(ev.alt.label) === -1) labels.push(ev.alt.label);
  });
  b.classList.add('on');
  var msg = n === 0
    ? 'No methods match "' + query + '". Try fewer or different words.'
    : n + (n===1 ? ' method matches ' : ' methods match ') + '"' + query + '"' +
      (labels.length ? '. Related terms also searched: ' + labels.slice(0,3).join(', ') + '.' : '');
  q('btext').textContent = msg;
  q('fcount').textContent = n + (n===1?' method':' methods');
  announce(msg);
}
function count(){
  var n = M.filter(function(m){ return (phase==='all' || m.phase===phase) && (fam==='all' || m.family===fam); }).length;
  q('fcount').textContent = n + (n===1?' method':' methods');
}

/* ---------- card grid ---------- */
function render(){
  PHASES.forEach(function(p){
    var g = q('grid-'+p); if (!g) return;
    var list = M.filter(function(m){
      if (m.phase !== p) return false;
      if (!query && phase!=='all' && phase!==p) return false;
      if (fam !== 'all' && m.family !== fam) return false;
      return true;
    }).map(function(m, i){ return {m:m, ev:evalCard(m), i:i}; })
      .filter(function(o){ return o.ev !== null; });
    if (query){ list.sort(function(a,b){ return a.ev.rank - b.ev.rank || a.i - b.i; }); }
    q('sec-'+p).classList.toggle('nomatch', (!!query || fam !== 'all') && !list.length);
    g.innerHTML = '';
    if (!list.length){
      if (!query && fam === 'all') g.appendChild(el('div','empty','No methods.'));
      return;
    }
    list.forEach(function(o){
      var m = o.m, ev = o.ev, alt = ev.alt;
      var c = el('article', 'card' + (m.kind==='brief' ? ' brief' : ''));
      c.dataset.id = m.id;
      c.appendChild(el('div','bar '+m.phase));
      if (m.image){
        var t = el('div','thumb');
        var im = document.createElement('img');
        im.src = m.image; im.alt = m.imageAlt || (m.name + ' in practice'); im.loading = 'lazy';
        t.appendChild(im); c.appendChild(t);
      }
      var b = el('div','body');
      var tg = el('div','tags');
      tg.appendChild(el('span','ph '+m.phase, PC[m.phase].name));
      tg.appendChild(el('span','fam', FAM[m.family].name));
      b.appendChild(tg);
      var h = el('h3');
      var ha = document.createElement('a');
      ha.href = '#' + m.id;
      ha.addEventListener('click', function(){ savedY = window.scrollY || 0; savedId = m.id; });
      if (query) ha.innerHTML = mark(m.name, alt); else ha.textContent = m.name;
      h.appendChild(ha);
      b.appendChild(h);
      var wi = plain(m.whatItIs), snip = wi.length > 112 ? wi.slice(0,112) + '…' : wi;
      var pp = el('p');
      var ex = (query && Math.floor(ev.rank) >= 2) ? excerpt(m, alt) : null;
      if (ex) pp.innerHTML = '<b>' + esc(ex.label) + ':<\/b> ' + mark(ex.text, alt);
      else if (query) pp.innerHTML = mark(snip, alt);
      else pp.textContent = snip;
      b.appendChild(pp);
      c.appendChild(b);
      var f = el('div','foot');
      var by = el('span','by');
      if (m.student){
        by.appendChild(document.createTextNode('By '));
        by.appendChild(el('b', null, m.student));
      } else {
        by.appendChild(el('span','ref-tag', m.origin==='draft' ? 'Draft entry' : 'Reference entry'));
      }
      f.appendChild(by);
      var go = el('span','go','View'); go.setAttribute('aria-hidden','true');
      f.appendChild(go);
      c.appendChild(f);
      g.appendChild(c);
    });
  });
  if (!query) count();
}

/* ---------- detail page ---------- */
function section(parent, title, node){
  var w = el('section','blk');
  w.appendChild(el('h2', null, title));
  w.appendChild(node);
  parent.appendChild(w);
}
var BOOKS = [
  {k:'Universal Methods of Design', url:'https://ebookcentral.proquest.com/lib/ncsu/detail.action?docID=6039458', gated:true,
   cite:'Martin & Hanington, 2012', ref:'Martin, B., & Hanington, B. (2012). *Universal methods of design: 100 ways to research complex problems, develop innovative ideas, and design effective solutions*. Rockport Publishers.'},
  {k:'101 Design Methods', url:'https://ebookcentral.proquest.com/lib/ncsu/detail.action?docID=861699', gated:true,
   cite:'Kumar, 2013', ref:'Kumar, V. (2013). *101 design methods: A structured approach for driving innovation in your organization*. Wiley.'},
  {k:'The Field Guide to Human-Centered Design', url:'https://www.designkit.org/resources/1.html', gated:false,
   cite:'IDEO.org, 2015', ref:'IDEO.org. (2015). *The field guide to human-centered design*. IDEO.org.'},
  {k:'Innovating for People', url:'https://www.luma-institute.com', gated:false,
   cite:'LUMA Institute, 2012', ref:'LUMA Institute. (2012). *Innovating for people: Handbook of human-centered design methods*. LUMA Institute.'},
  {k:'The User Experience Team of One', url:'https://rosenfeldmedia.com/books/the-user-experience-team-of-one/', gated:false,
   cite:'Buley, 2013', ref:'Buley, L. (2013). *The user experience team of one: A research and design survival guide*. Rosenfeld Media.'}
];
/* copy a citation as plain text and, where the browser allows, as formatted text with italics */
function toHtml(t){ return esc(t).replace(/\*([^*]+)\*/g, '<i>$1<\/i>'); }
function copyRich(text, html, done){
  function fallback(){
    try {
      var t = document.createElement('textarea'); t.value = text; t.setAttribute('readonly',''); t.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
      document.body.appendChild(t); t.select();
      var ok = document.execCommand('copy'); document.body.removeChild(t); done(ok);
    } catch(e){ done(false); }
  }
  function plainOnly(){
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function(){ done(true); }, fallback);
    else fallback();
  }
  try {
    if (navigator.clipboard && navigator.clipboard.write && window.ClipboardItem){
      var item = new ClipboardItem({'text/plain': new Blob([text], {type:'text/plain'}), 'text/html': new Blob([html], {type:'text/html'})});
      navigator.clipboard.write([item]).then(function(){ done(true); }, plainOnly);
      return;
    }
  } catch(e){}
  plainOnly();
}
function copyButton(label, aria, getPair){
  var b = el('button','cpy', label); b.type = 'button';
  b.setAttribute('aria-label', aria);
  b.addEventListener('click', function(){
    var pr = getPair();
    copyRich(plain(pr[0]), pr[1], function(ok){
      b.textContent = ok ? 'Copied' : 'Copy failed';
      announce(ok ? 'Copied to the clipboard' : 'Could not copy. Select the text and copy it yourself.', 50);
      setTimeout(function(){ b.textContent = label; }, 2000);
    });
  });
  return b;
}
function bookInfo(name){
  for (var i = 0; i < BOOKS.length; i++){ if (String(name).indexOf(BOOKS[i].k) === 0) return BOOKS[i]; }
  return null;
}
function detail(m){
  var pc = PC[m.phase];
  q('bc-phase').textContent = pc.name;
  q('bc-name').textContent  = m.name;

  var hero = q('dhero'); hero.className = 'dhero ' + m.phase;
  var acts = hero.querySelector('.actions'), oldSb = acts.querySelector('.sbtn');
  if (oldSb) acts.removeChild(oldSb);
  acts.appendChild(shortBtn(m.id));
  q('d-eyebrow').textContent = pc.name;
  q('d-title').textContent   = m.name;
  q('d-alts').textContent    = (m.altNames && m.altNames.length) ? 'Also known as ' + m.altNames.join(', ') : '';
  var by = q('d-by'); by.innerHTML = '';
  if (m.student){
    by.appendChild(document.createTextNode('Card written by '));
    var sb = el('b', null, m.student); sb.style.fontWeight = '700';
    by.appendChild(sb);
    by.appendChild(document.createTextNode(', a student in D 492 Intro to Design Research, ' + (m.semester || 'Spring 2026')));
  } else {
    by.appendChild(el('em', null, m.origin==='draft'
      ? 'Draft entry, written for this site and not yet reviewed'
      : 'Reference entry, not yet documented by a student'));
  }

  /* main column */
  var main = q('d-main'); main.innerHTML = '';
  if (m.origin === 'draft' && m.draftNote){
    main.appendChild(el('div','notice', m.draftNote));
  }
  if (m.kind === 'brief'){
    main.appendChild(el('div','notice',
      'This method has a short reference entry. Full documentation is written by students, and this card is available for a future class to complete.'));
  }
  section(main, 'What it is', rich(el('p','prose'), m.whatItIs));

  if (m.family && FAM[m.family]){
    var F = FAM[m.family], sbx = el('div','showbox');
    var fh = el('div','fh');
    fh.appendChild(el('span','fam', F.name));
    fh.appendChild(el('span', null, 'Evidence: ' + F.evidence.toLowerCase() + '.'));
    var fb = el('button', null, 'See all ' + F.name + ' methods'); fb.type = 'button';
    fb.addEventListener('click', function(){ setPhase('all'); setFam(m.family); });
    fh.appendChild(fb);
    sbx.appendChild(fh);
    var cols = el('div','cols');
    var c1 = el('div','col yes'); c1.appendChild(el('div','l','Can show')); c1.appendChild(el('p', null, m.show)); cols.appendChild(c1);
    var c2 = el('div','col no'); c2.appendChild(el('div','l','Cannot show')); c2.appendChild(el('p', null, m.limit)); cols.appendChild(c2);
    sbx.appendChild(cols);
    if (m.family === 'analyze') sbx.appendChild(el('div','foot','Analysis methods work on data you collected with another family. Their findings are only as strong as that data.'));
    else sbx.appendChild(el('div','foot','Pair this with a method from a different family so that each covers the other\u2019s blind spot.'));
    section(main, 'What it can show', sbx);
  }

  if (m.kind === 'full'){
    if (m.whenToUse && m.whenToUse.length){
      var u = el('ul','wlist');
      m.whenToUse.forEach(function(x){
        var li = el('li'); li.appendChild(el('span','d')); li.appendChild(rich(el('span'),x)); u.appendChild(li);
      });
      section(main, 'When to use it', u);
    }
    if (m.howToDoIt && m.howToDoIt.length){
      var o = el('ol','slist');
      m.howToDoIt.forEach(function(x){ var li = el('li'); li.appendChild(rich(el('span'), x)); o.appendChild(li); });
      section(main, 'How to do it', o);
    }
    if (m.example){
      var ex = el('div','exbox');
      String(m.example).split(/\n\n+/).forEach(function(para){ if (para.trim()) ex.appendChild(el('p', null, para.trim())); });
      section(main, 'Example in practice', ex);
    }
  }
  if (m.kind === 'full' && m.editorNote){
    main.appendChild(el('p','editnote', 'Editorial note: ' + m.editorNote));
  }
  if (m.kind === 'full' && m.expandedNote){
    main.appendChild(el('p','editnote', m.expandedNote));
  }
  if (m.kind === 'full' && m.sources && m.sources.length){
    var sw = el('div');
    m.sources.forEach(function(s){
      var d = el('div','cite'), ct = el('span','ct');
      var parts = String(s).split(/(https?:\/\/\S+)/);
      parts.forEach(function(p){
        if (/^https?:\/\//.test(p)){
          var a = document.createElement('a');
          a.href = p; a.target = '_blank'; a.rel = 'noopener'; a.textContent = p;
          ct.appendChild(a);
        } else if (p) {
          rich(ct, p);
        }
      });
      d.appendChild(ct);
      d.appendChild(copyButton('Copy reference', 'Copy this reference: ' + plain(s).slice(0, 60), function(){ return [s, toHtml(s)]; }));
      sw.appendChild(d);
    });
    var ca = el('button','cpyall','Copy all references'); ca.type = 'button';
    ca.addEventListener('click', function(){
      copyRich(m.sources.map(plain).join('\n\n'), m.sources.map(function(x){ return '<p>' + toHtml(x) + '<\/p>'; }).join(''), function(ok){
        ca.textContent = ok ? 'Copied' : 'Copy failed';
        announce(ok ? 'All references copied' : 'Could not copy.', 50);
        setTimeout(function(){ ca.textContent = 'Copy all references'; }, 2000);
      });
    });
    sw.appendChild(ca);
    section(main, 'Where to learn more', sw);
  }

  if (m.kind === 'brief' && m.overview && m.overview.length){
    var ow = el('div'), ou = el('ul','ovlist');
    m.overview.forEach(function(o){
      var li = el('li'), a = document.createElement('a');
      a.href = o.url; a.target = '_blank'; a.rel = 'noopener';
      a.appendChild(document.createTextNode(o.title));
      a.appendChild(el('span','sr',' (opens in a new tab)'));
      li.appendChild(a);
      li.appendChild(el('span','pub', o.publisher));
      if (o.note) li.appendChild(el('span','on', o.note));
      ou.appendChild(li);
    });
    ow.appendChild(ou);
    ow.appendChild(el('p','ovnote','Free to read online. These pages are not part of the course books. Links checked October 2026.'));
    section(main, 'Where to learn more', ow);
  }

  if (m.templates && m.templates.length){
    var tw = el('div'), tu = el('ul','tplist');
    m.templates.forEach(function(o){
      var li = el('li'), a = document.createElement('a');
      a.href = o.url;
      if (o.own){ a.setAttribute('download',''); }
      else { a.target = '_blank'; a.rel = 'noopener'; }
      a.appendChild(document.createTextNode(o.title));
      a.appendChild(el('span','sr', o.own ? ' (downloads a file)' : ' (opens in a new tab)'));
      li.appendChild(a);
      li.appendChild(el('span','pub', o.own ? 'Made for this site. ' + o.format + '.' : o.publisher + '. ' + o.format + '.'));
      li.appendChild(el('span','acc', o.access));
      if (o.note) li.appendChild(el('span','on', o.note));
      tu.appendChild(li);
    });
    tw.appendChild(tu);
    var anyOwn = m.templates.some(function(o){ return o.own; }), anyExt = m.templates.some(function(o){ return !o.own; });
    tw.appendChild(el('p','ovnote',
      (anyOwn ? 'Templates marked "Made for this site" are drafted here, are not course materials, and are not official forms. ' : '') +
      (anyExt ? 'Other links go to other websites and are made by their publishers. Links checked October 2026.' : '')));
    section(main, 'Templates and worksheets', tw);
  }

  if (m.pairs && m.pairs.length){
    var pu = el('ul','pairlist');
    m.pairs.forEach(function(pr){
      var o = BY[pr.id]; if (!o) return;
      var li = el('li'), b = document.createElement('button');
      b.type = 'button';
      var dot = el('span','d'); dot.style.background = PCOL[o.phase]; dot.setAttribute('aria-hidden','true');
      b.appendChild(dot); b.appendChild(el('span','nm', o.name));
      b.appendChild(el('span','ph', PC[o.phase].name));
      b.addEventListener('click', function(){ open(o.id); });
      li.appendChild(b); li.appendChild(el('span','why', pr.why));
      pu.appendChild(li);
    });
    section(main, 'Pairs well with', pu);
  }

  if (m.library && m.library.length){
    var lu = el('ul','libbox');
    m.library.forEach(function(e){
      var li = el('li'), bk = bookInfo(e.book);
      if (bk){
        var ba = document.createElement('a');
        ba.href = bk.url; ba.target = '_blank'; ba.rel = 'noopener';
        ba.appendChild(el('b', null, e.book));
        ba.appendChild(el('span','sr',' (opens in a new tab)'));
        li.appendChild(ba);
      } else {
        li.appendChild(el('b', null, e.book));
      }
      li.appendChild(document.createTextNode(', ' + e.where));
      if (bk && bk.gated) li.appendChild(el('span','gt','Library link. Off campus, an NC State sign-in is required.'));
      if (bk && bk.ref){
        var pg = /p\.\s*(\d+)/.exec(e.where), it = '(' + bk.cite + (pg ? ', p. ' + pg[1] : '') + ')';
        var cp = el('span','cp');
        cp.appendChild(copyButton('Copy in-text citation', 'Copy the in-text citation ' + it, function(){ return [it, esc(it)]; }));
        cp.appendChild(copyButton('Copy reference', 'Copy the reference for ' + bk.k, function(){ return [bk.ref, toHtml(bk.ref)]; }));
        li.appendChild(cp);
      }
      lu.appendChild(li);
    });
    section(main, 'Where this method appears in the course books', lu);
  }

  /* sidebar */
  var sbv = q('d-visual'); sbv.innerHTML = '';
  var sb = q('d-side'); sb.innerHTML = '';
  var vis = el('div','sb'); vis.appendChild(el('h2', null, 'Visual reference'));
  if (m.image){
    var fig = document.createElement('figure');
    var im = document.createElement('img');
    im.src = m.image; im.alt = m.imageAlt || (m.name + ' in practice'); im.loading = 'lazy';
    var zb = document.createElement('button'); zb.type = 'button'; zb.className = 'zoom';
    zb.appendChild(im);
    zb.appendChild(el('span','sr',', opens a larger view'));
    var zh = el('span','zoomhint','Enlarge'); zh.setAttribute('aria-hidden','true');
    zb.appendChild(zh);
    fig.appendChild(zb);
    var fc = document.createElement('figcaption');
    var parts = [];
    if (m.imageCredit) fc.appendChild(document.createTextNode(m.imageCredit));
    if (m.imageSource || m.imageSourceUrl){
      fc.appendChild(document.createTextNode(' Source: '));
      if (m.imageSourceUrl){
        var sa2 = document.createElement('a');
        sa2.href = m.imageSourceUrl; sa2.target = '_blank'; sa2.rel = 'noopener';
        sa2.textContent = m.imageSource || m.imageSourceUrl;
        fc.appendChild(sa2);
        fc.appendChild(document.createTextNode('.'));
      } else {
        fc.appendChild(document.createTextNode(m.imageSource + (/[.)]$/.test(m.imageSource) ? '' : '.')));
      }
    } else if (m.imageCredit){
      fc.appendChild(document.createTextNode(' The student did not list an original source.'));
    }
    if (m.imageNote){
      fc.appendChild(el('span','note', m.imageNote));
    }
    fig.appendChild(fc);
    zb.addEventListener('click', function(){ openLightbox(m, zb, fc); });
    vis.appendChild(fig);
  } else {
    var ni = el('div','noimg');
    ni.appendChild(el('div','t','No image yet'));
    ni.appendChild(el('p', null, 'An image showing this method in practice will be added here.'));
    vis.appendChild(ni);
  }
  sbv.appendChild(vis);

  var dd = el('div','sb'); dd.appendChild(el('h2', null, 'Where it sits'));
  var ind = el('div','ddind');
  ind.appendChild(el('div','lab','Double Diamond position'));
  var bars = el('div','ddbars');
  PHASES.forEach(function(p){
    var b = el('button','ddseg' + (p===m.phase ? ' on' : ''));
    b.type = 'button';
    b.setAttribute('aria-label', 'See all ' + PC[p].name + ' methods' + (p===m.phase ? ' (this card is in this phase)' : ''));
    var i = document.createElement('i');
    i.className = (p===m.phase ? 'on ' + p : p);
    b.appendChild(i);
    b.appendChild(el('span', null, PC[p].name));
    b.addEventListener('click', function(){ setPhase(p); });
    bars.appendChild(b);
  });
  ind.appendChild(bars);
  ind.appendChild(el('div','ddhelp','Select a phase to see its methods.'));
  ind.appendChild(el('div','ddnote', pc.ddNote));
  dd.appendChild(ind); sb.appendChild(dd);

  if (m.kind === 'full'){
    if (m.whatYouNeed && m.whatYouNeed.length){
      var n = el('div','sb'); n.appendChild(el('h2', null, 'What you need'));
      var nu = el('ul','nlist');
      m.whatYouNeed.forEach(function(x){
        var li = el('li'); li.appendChild(el('span','d')); li.appendChild(el('span', null, x)); nu.appendChild(li);
      });
      n.appendChild(nu); sb.appendChild(n);
    }
    var tipsAll = (m.tips||[]).map(function(t){ return {k:'tip', t:t}; })
                 .concat((m.mistakes||[]).map(function(t){ return {k:'mistake', t:t}; }));
    if (tipsAll.length){
      var tw = el('div','sb'); tw.appendChild(el('h2', null, 'Tips and common mistakes'));
      tipsAll.forEach(function(o){
        var d = el('div','tipbox ' + o.k);
        d.appendChild(el('div','lab', o.k==='tip' ? 'Tip' : 'Common mistake'));
        d.appendChild(el('span', null, o.t));
        tw.appendChild(d);
      });
      sb.appendChild(tw);
    }
  } else if (m.referenceUrl){
    var rb = el('div','sb'); rb.appendChild(el('h2', null, 'Read more'));
    var box2 = el('div','refbox');
    box2.appendChild(el('div','l','Primary source'));
    box2.appendChild(el('p', null, m.reference));
    var a = document.createElement('a');
    a.href = m.referenceUrl; a.target = '_blank'; a.rel = 'noopener';
    var gated = /ebookcentral\.proquest\.com|prox\.lib\.ncsu\.edu|proxying\.lib\.ncsu\.edu/.test(m.referenceUrl);
    a.textContent = gated ? 'Open in NC State Libraries' : 'Open the source';
    box2.appendChild(a);
    if (gated) box2.appendChild(el('p','gate','Library link. Off campus, an NC State sign-in is required.'));
    rb.appendChild(box2); sb.appendChild(rb);
  }

  var mo = el('div','sb');
  mo.appendChild(el('h2', null, 'More in ' + pc.name));
  var list = el('div','more');
  var peers = M.filter(function(x){ return x.phase===m.phase && x.id!==m.id; });
  peers.slice(0,8).forEach(function(p){
    var b = document.createElement('button');
    var d = el('span','d'); d.style.background = PCOL[m.phase];
    b.appendChild(d); b.appendChild(el('span', null, p.name));
    b.addEventListener('click', function(){ open(p.id); });
    list.appendChild(b);
  });
  if (peers.length > 8) list.appendChild(el('div','ovf','and ' + (peers.length-8) + ' more'));
  mo.appendChild(list);
  var sa = el('button','seeall','See all ' + pc.name + ' methods');
  sa.addEventListener('click', homePhase);
  mo.appendChild(sa);
  sb.appendChild(mo);
}


/* ---------- shortlist ---------- */
var LSKEY = 'drm-shortlist-v1', SHORT = [];
try { var _sv = JSON.parse(localStorage.getItem(LSKEY) || '[]'); if (Array.isArray(_sv)) SHORT = _sv.filter(function(id){ return BY[id]; }); } catch(e){}
function saveShort(){ try { localStorage.setItem(LSKEY, JSON.stringify(SHORT)); } catch(e){} }
function inShort(id){ return SHORT.indexOf(id) !== -1; }
function setShort(id, on, quiet){
  var i = SHORT.indexOf(id);
  if (on && i === -1) SHORT.push(id); else if (!on && i !== -1) SHORT.splice(i, 1); else return;
  saveShort(); syncShort();
  if (!quiet) announce(BY[id].name + (on ? ' added to' : ' removed from') + ' your shortlist. ' + SHORT.length + (SHORT.length === 1 ? ' method' : ' methods') + ' on the list.', 50);
}
function paintShort(b){
  var on = inShort(b.dataset.short);
  b.classList.toggle('on', on);
  b.innerHTML = '';
  b.appendChild(document.createTextNode(on ? 'On your shortlist' : 'Add to shortlist'));
  b.appendChild(el('span','sr', ': ' + BY[b.dataset.short].name + (on ? '. Select to remove.' : '')));
}
function shortBtn(id){
  var b = el('button','sbtn'); b.type = 'button'; b.dataset.short = id;
  b.addEventListener('click', function(){ setShort(id, !inShort(id)); });
  paintShort(b);
  return b;
}
function syncShort(){
  document.querySelectorAll('.shortcount').forEach(function(c){
    c.classList.toggle('on', SHORT.length > 0);
    c.innerHTML = '';
    var a = el('span', null, String(SHORT.length)); a.setAttribute('aria-hidden','true');
    c.appendChild(a); c.appendChild(el('span','sr', ' methods on your shortlist'));
  });
  document.querySelectorAll('.sbtn[data-short]').forEach(paintShort);
  renderShort();
}
function srcLine(m){
  var e = m.library && m.library[0];
  return e ? e.book + ', ' + e.where : '';
}
function shortText(){
  var base = location.origin + location.pathname;
  var out = ['Shortlist from Design Research Methods (' + base + ')', ''];
  SHORT.forEach(function(id, i){
    var m = BY[id];
    out.push((i + 1) + '. ' + m.name + ' (' + PC[m.phase].name + ' phase, ' + FAM[m.family].name + ' family)');
    out.push('   Can show: ' + m.show);
    out.push('   Cannot show: ' + m.limit);
    var sl = srcLine(m); if (sl) out.push('   Where to read: ' + sl);
    out.push('   Card: ' + base + '#' + m.id);
    out.push('');
  });
  return out.join('\n');
}
function renderShort(){
  var w = q('short'); if (!w) return;
  w.innerHTML = '';
  if (!SHORT.length){
    w.appendChild(el('div','sempty','Your shortlist is empty. Add a method with the “Add to shortlist” button on any card, or from the lists above.'));
    return;
  }
  var wrap = el('div','tblwrap'), t = document.createElement('table'); t.className = 'stable';
  var cap = document.createElement('caption'); cap.className = 'sr'; cap.textContent = 'Methods on your shortlist'; t.appendChild(cap);
  var th = document.createElement('thead'), hr = document.createElement('tr');
  ['Method','Family','Can show','Cannot show','Where to read',''].forEach(function(h){
    var c = document.createElement('th'); c.scope = 'col';
    if (h) c.textContent = h; else c.appendChild(el('span','sr','Remove'));
    hr.appendChild(c);
  });
  th.appendChild(hr); t.appendChild(th);
  var tb = document.createElement('tbody');
  SHORT.forEach(function(id){
    var m = BY[id], r = document.createElement('tr');
    var c1 = document.createElement('td'); c1.className = 'mn';
    var b1 = el('button', null, m.name); b1.type = 'button'; b1.addEventListener('click', function(){ open(m.id); });
    c1.appendChild(b1); c1.appendChild(el('span','ph', PC[m.phase].name + ' phase'));
    r.appendChild(c1);
    [['Family', FAM[m.family].name], ['Can show', m.show], ['Cannot show', m.limit], ['Where to read', srcLine(m) || 'See the card']].forEach(function(x){
      var c = document.createElement('td'); c.dataset.l = x[0]; c.textContent = x[1]; r.appendChild(c);
    });
    var c6 = document.createElement('td');
    var rb = el('button','rm','Remove'); rb.type = 'button';
    rb.appendChild(el('span','sr',' ' + m.name + ' from your shortlist'));
    rb.addEventListener('click', function(){ setShort(m.id, false); });
    c6.appendChild(rb); r.appendChild(c6);
    tb.appendChild(r);
  });
  t.appendChild(tb); wrap.appendChild(t); w.appendChild(wrap);
  var fams = [];
  SHORT.forEach(function(id){ var f = BY[id].family; if (f !== 'analyze' && fams.indexOf(f) === -1) fams.push(f); });
  var msg;
  if (fams.length === 0) msg = 'Your list holds analysis methods only. Analysis methods work on data that another method collected, so add at least two methods that collect evidence.';
  else if (fams.length === 1) msg = 'Your collecting methods all come from the ' + FAM[fams[0]].name + ' family, so they share one blind spot. Add a method from a different family to check them.';
  else msg = 'Your collecting methods cover ' + fams.length + ' families: ' + fams.map(function(f){ return FAM[f].name; }).join(', ') + '. For each pair, finish the sentence “My second method checks my first because ...”.';
  w.appendChild(el('p','scover', msg));
  var act = el('div','sact');
  var cb = el('button','btn2 solid','Copy as text'); cb.type = 'button';
  cb.addEventListener('click', function(){
    var tx = shortText();
    copyRich(tx, '<pre>' + esc(tx) + '<\/pre>', function(ok){
      cb.textContent = ok ? 'Copied' : 'Copy failed';
      announce(ok ? 'Shortlist copied to the clipboard' : 'Could not copy.', 50);
      setTimeout(function(){ cb.textContent = 'Copy as text'; }, 2000);
    });
  });
  var pb = el('button','btn2','Print'); pb.type = 'button'; pb.addEventListener('click', function(){ window.print(); });
  var xb = el('button','btn2','Clear list'); xb.type = 'button';
  var armed = false, tm = null;
  xb.addEventListener('click', function(){
    if (!armed){
      armed = true; xb.textContent = 'Select again to clear the list';
      tm = setTimeout(function(){ armed = false; xb.textContent = 'Clear list'; }, 3500);
      return;
    }
    clearTimeout(tm); SHORT = []; saveShort(); syncShort(); announce('Shortlist cleared', 50);
  });
  act.appendChild(cb); act.appendChild(pb); act.appendChild(xb);
  w.appendChild(act);
  w.appendChild(el('p','sstore','Saved in this browser on this device only.'));
}

/* ---------- plan page ---------- */
function methodRow(m){
  var li = el('li');
  var nb = el('button','nm'); nb.type = 'button';
  var dot = el('span','d'); dot.style.background = PCOL[m.phase]; dot.setAttribute('aria-hidden','true');
  nb.appendChild(dot); nb.appendChild(el('span','t', m.name)); nb.appendChild(el('span','ph', PC[m.phase].name));
  nb.addEventListener('click', function(){ open(m.id); });
  li.appendChild(nb);
  var sl = el('div','sl'); sl.appendChild(el('b', null, 'Can show: ')); sl.appendChild(document.createTextNode(m.show));
  li.appendChild(sl);
  li.appendChild(shortBtn(m.id));
  return li;
}
function showBox(F){
  var sbx = el('div','showbox');
  var cols = el('div','cols');
  var c1 = el('div','col yes'); c1.appendChild(el('div','l','Can show')); c1.appendChild(el('p', null, F.show)); cols.appendChild(c1);
  var c2 = el('div','col no'); c2.appendChild(el('div','l','Cannot show')); c2.appendChild(el('p', null, F.limit)); cols.appendChild(c2);
  sbx.appendChild(cols);
  return sbx;
}
function radioCard(group, value, title, extra, onPick){
  var lb = el('label','qopt'), inp = document.createElement('input');
  inp.type = 'radio'; inp.name = group; inp.value = value;
  inp.addEventListener('change', function(){ onPick(value); });
  lb.appendChild(inp);
  lb.appendChild(el('b', null, title));
  if (extra) lb.appendChild(el('span','ev', extra));
  return lb;
}
var QTEXT = {read:'What exists, what was made, or how something came to be', ask:'What people say, believe, remember, value, or prefer',
  watch:'What people actually do, and in what setting', test:'Whether one version works better than another, and by how much',
  make:'What is possible, or how people respond to something that does not exist yet', analyze:'What the data I already have is telling me'};
function showQuestion(f){
  var F = FAM[f], out = q('qres'); out.innerHTML = '';
  var box = el('div','rbox');
  box.appendChild(el('h3', null, F.name + ' methods'));
  box.appendChild(el('p', null, 'Evidence you need: ' + F.evidence.toLowerCase() + '.'));
  box.appendChild(showBox(F));
  if (f === 'watch'){
    var w1 = el('div','warnbox'); w1.appendChild(el('b', null, 'The say and do gap. '));
    w1.appendChild(document.createTextNode('If your question is about what people do, asking will not answer it. People report their behavior inaccurately, especially about frequency, time, and anything they feel judged about. Use a method that watches, or pair an asking method with one that watches.'));
    box.appendChild(w1);
  }
  if (f === 'test'){
    var w2 = el('div','warnbox'); w2.appendChild(el('b', null, 'Questions about effect and cause. '));
    w2.appendChild(document.createTextNode('A question such as “what effect does X have on Y” or “does X cause Y” needs a comparison of at least two conditions that differ in one respect. If you cannot run that comparison well, narrow the question to what you can show, such as how people describe X. Or build a small controlled comparison and report it as suggestive rather than conclusive. Do not ask people about X and then write that X causes Y.'));
    box.appendChild(w2);
  }
  var all = M.filter(function(m){ return m.family === f; });
  var home = all.filter(function(m){ return f === 'analyze' ? m.phase === 'insights' : m.phase === 'research'; });
  var rest = all.filter(function(m){ return home.indexOf(m) === -1; });
  box.appendChild(el('div','lab', f === 'analyze' ? 'Methods for making sense of data' : 'Methods for gathering this evidence'));
  var ul = el('ul','mlist'); home.forEach(function(m){ ul.appendChild(methodRow(m)); }); box.appendChild(ul);
  if (rest.length){
    var ul2 = el('ul','mlist'); ul2.hidden = true; ul2.id = 'qmore';
    rest.forEach(function(m){ ul2.appendChild(methodRow(m)); });
    var mb = el('button','morebtn','Show ' + rest.length + ' more ' + F.name + ' methods from other phases'); mb.type = 'button';
    mb.setAttribute('aria-expanded','false'); mb.setAttribute('aria-controls','qmore');
    mb.addEventListener('click', function(){
      var on = ul2.hidden; ul2.hidden = !on; mb.setAttribute('aria-expanded', on ? 'true' : 'false');
      mb.textContent = on ? 'Hide the other ' + F.name + ' methods' : 'Show ' + rest.length + ' more ' + F.name + ' methods from other phases';
    });
    box.appendChild(mb); box.appendChild(ul2);
  }
  var nx = el('p'); nx.style.marginTop = '20px';
  nx.appendChild(document.createTextNode('Next, choose a second method from a different family. '));
  var nb = el('button','morebtn','Go to the pair builder'); nb.type = 'button'; nb.style.marginTop = '0'; nb.addEventListener('click', function(){ go('plan-pair'); });
  nx.appendChild(nb); box.appendChild(nx);
  out.appendChild(box);
}
function methodLinks(ids, note, lead){
  var f = document.createDocumentFragment();
  if (lead) f.appendChild(document.createTextNode(lead + ' '));
  ids.forEach(function(id, i){
    if (i) f.appendChild(document.createTextNode(' or '));
    var m = BY[id], b = el('button','mn'); b.type = 'button';
    var d = el('span','d'); d.style.background = PCOL[m.phase]; d.setAttribute('aria-hidden','true');
    b.appendChild(d); b.appendChild(el('span','t', m.name)); b.appendChild(el('span','fam', FAM[m.family].name));
    b.addEventListener('click', function(){ open(id); });
    f.appendChild(b);
  });
  if (note) f.appendChild(document.createTextNode(' ' + note));
  return f;
}
function showMode(id){
  var md = (APP.modes || []).filter(function(x){ return x.id === id; })[0], out = q('mres'); out.innerHTML = '';
  if (!md) return;
  var box = el('div','rbox');
  box.appendChild(el('h3', null, 'Research ' + md.name.toLowerCase()));
  [['What it contributes', md.gives], ['What you hand in', md.handIn], ['Families it leans on', md.leans], ['A sign you have drifted', md.drift]].forEach(function(x){
    var p = el('p'); p.appendChild(el('b', null, x[0] + ': ')); p.appendChild(document.createTextNode(x[1])); box.appendChild(p);
  });
  box.appendChild(el('div','lab','Pairs that work for this mode'));
  md.pairs.forEach(function(pr){
    var r = el('div','prec'), eq = el('div','eq');
    eq.appendChild(methodLinks(pr.first.ids, pr.first.note, pr.first.lead));
    eq.appendChild(el('span','plus','plus'));
    eq.appendChild(methodLinks(pr.second.ids, pr.second.note, pr.second.lead));
    r.appendChild(eq);
    r.appendChild(el('p','add', pr.adds));
    var ids = pr.first.ids.concat(pr.second.ids);
    var ab = el('button','btn2 sbs','Add these ' + ids.length + ' methods to your shortlist'); ab.type = 'button';
    ab.addEventListener('click', function(){
      ids.forEach(function(i){ setShort(i, true, true); });
      announce(ids.length + ' methods added to your shortlist.', 50);
    });
    r.appendChild(ab);
    box.appendChild(r);
  });
  var w = el('div','warnbox'); w.appendChild(el('b', null, 'Write the checking sentence. '));
  w.appendChild(document.createTextNode('Finish this sentence in your plan: “My second method checks my first because ...” If you cannot finish it, you have two methods on the same question rather than a method and a check. Researchers call this triangulation.'));
  box.appendChild(w);
  var w2 = el('p'); w2.style.marginTop = '14px'; w2.style.fontSize = '13.5px'; w2.style.color = 'var(--gtxt)';
  w2.textContent = 'If your mode changes later, that is allowed and sometimes right. Write down the date, the reason, and what changed in your plan.';
  box.appendChild(w2);
  out.appendChild(box);
}
var SUGG = {read:['ask','watch'], ask:['watch','read'], watch:['ask'], test:['ask','watch'], make:['watch','ask']};
function showCheck(){
  var a = q('pa').value, b = q('pb').value, out = q('cres'); out.innerHTML = '';
  if (!a || !b) return;
  if (a === b){ out.appendChild(el('div','warnbox','Choose two different methods.')); return; }
  var A = BY[a], B = BY[b], box = el('div','rbox');
  box.appendChild(el('h3', null, A.name + ' with ' + B.name));
  var g = el('div','mfacts');
  [[A.name + ' can show', A.show], [A.name + ' cannot show', A.limit], [B.name + ' can show', B.show], [B.name + ' cannot show', B.limit]].forEach(function(x){
    var d = el('div'); d.appendChild(el('span','l', x[0])); d.appendChild(document.createTextNode(x[1])); g.appendChild(d);
  });
  box.appendChild(g);
  var fa = FAM[A.family], fb = FAM[B.family], ok = false;
  if (A.family === 'analyze' || B.family === 'analyze'){
    box.appendChild(el('div','warnbox','An analysis method does not collect evidence. It works on data that another method collected. Choose two methods that collect evidence, from different families, and then choose the analysis method for the data both produce.'));
  } else if (A.family === B.family){
    var wb = el('div','warnbox'); wb.appendChild(el('b', null, 'Both are in the ' + fa.name + ' family. '));
    wb.appendChild(document.createTextNode('Two methods from one family share a blind spot. Neither can show: ' + fa.limit.charAt(0).toLowerCase() + fa.limit.slice(1) + ' Try replacing one with a method from another family:'));
    box.appendChild(wb);
    var ul = el('ul','mlist');
    (SUGG[A.family] || []).forEach(function(f){
      M.filter(function(m){ return m.family === f && m.phase === 'research'; }).slice(0, 3).forEach(function(m){ ul.appendChild(methodRow(m)); });
    });
    box.appendChild(ul);
  } else {
    ok = true;
    var ob = el('div','okbox'); ob.appendChild(el('b', null, 'Different families: ' + fa.name + ' and ' + fb.name + '. '));
    ob.appendChild(document.createTextNode('Each method can cover what the other cannot show. Read the four lines above and check that the second method answers the gap the first one leaves.'));
    box.appendChild(ob);
    if ((A.family === 'test' && B.family === 'read') || (A.family === 'read' && B.family === 'test')){
      box.appendChild(el('div','warnbox','Testing and reading rarely appear together in published design research. Check that the two are really answering the same question.'));
    }
  }
  if (ok){
    var s = el('div','sentence'), lb = el('label', null, 'Finish the checking sentence'); lb.setAttribute('for','chk-sentence');
    var ta = document.createElement('textarea'); ta.id = 'chk-sentence';
    ta.value = 'My second method, ' + B.name + ', checks my first, ' + A.name + ', because ';
    s.appendChild(lb); s.appendChild(ta);
    var row = el('div','row');
    var cs = el('button','btn2','Copy sentence'); cs.type = 'button';
    cs.addEventListener('click', function(){
      copyRich(ta.value, esc(ta.value), function(k){ cs.textContent = k ? 'Copied' : 'Copy failed'; announce(k ? 'Sentence copied' : 'Could not copy.', 50); setTimeout(function(){ cs.textContent = 'Copy sentence'; }, 2000); });
    });
    row.appendChild(cs); s.appendChild(row); box.appendChild(s);
  }
  var ab = el('button','btn2','Add both to your shortlist'); ab.type = 'button'; ab.style.marginTop = '16px';
  ab.addEventListener('click', function(){ setShort(a, true, true); setShort(b, true, true); announce(A.name + ' and ' + B.name + ' added to your shortlist.', 50); });
  box.appendChild(ab);
  out.appendChild(box);
}
function buildPlan(){
  var qo = q('qopts');
  FAMS.forEach(function(f){
    qo.appendChild(radioCard('qg', f.id, QTEXT[f.id], 'Evidence: ' + f.evidence.toLowerCase() + '. Family: ' + f.name + '.', showQuestion));
  });
  var mo = q('mopts');
  (APP.modes || []).forEach(function(md){ mo.appendChild(radioCard('mode', md.id, md.name, md.gives, showMode)); });
  ['pa','pb'].forEach(function(id){
    var sel = q(id), o0 = document.createElement('option'); o0.value = ''; o0.textContent = 'Choose a method'; sel.appendChild(o0);
    FAMS.forEach(function(f){
      var g = document.createElement('optgroup'), list = M.filter(function(m){ return m.family === f.id; });
      g.label = f.name + ' (' + list.length + ')';
      list.slice().sort(function(x, y){ return x.name.localeCompare(y.name); }).forEach(function(m){
        var o = document.createElement('option'); o.value = m.id; o.textContent = m.name; g.appendChild(o);
      });
      sel.appendChild(g);
    });
    sel.addEventListener('change', showCheck);
  });
  syncShort();
}

/* ---------- contributors ---------- */
function contributors(){
  var wrap = q('clist');
  var byStu = {};
  M.forEach(function(m){ if (m.student){ (byStu[m.student] = byStu[m.student] || []).push(m); } });
  Object.keys(byStu).sort(function(a,b){
    return a.split(' ').pop().localeCompare(b.split(' ').pop());
  }).forEach(function(s){
    var p = el('div','cperson');
    p.appendChild(el('div','nm', s));
    var u = document.createElement('ul');
    byStu[s].forEach(function(m){
      var li = el('li');
      var la = document.createElement('a'); la.href = '#' + m.id;
      var d = el('span','dot'); d.style.background = PCOL[m.phase];
      la.appendChild(d); la.appendChild(el('span', null, m.name));
      li.appendChild(la);
      u.appendChild(li);
    });
    p.appendChild(u); wrap.appendChild(p);
  });
}

/* ---------- init ---------- */
q('stat-methods').textContent = APP.total;
q('stat-cards').textContent   = APP.fullCount;
q('stat-students').textContent= APP.students.length;
q('stat-drafts').textContent  = APP.draftCount;
PHASES.forEach(function(p){
  q('ddn-'+p).textContent = APP.counts[p] + ' methods';
  q('chipn-'+p).textContent = String(APP.counts[p]);
});
Search.init(JSON.parse(document.getElementById('syn-data').textContent));
(function(){
  var d = q('lb');
  d.addEventListener('click', function(e){ if (e.target === d) d.close(); });
  d.addEventListener('keydown', function(e){
    if (e.key !== 'Tab') return;
    var f = [].slice.call(d.querySelectorAll('button, a[href], [tabindex="0"]')).filter(function(x){ return x.getClientRects().length; });
    if (!f.length) return;
    e.preventDefault();
    var i = f.indexOf(document.activeElement);
    f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
  });
  d.addEventListener('close', function(){
    document.documentElement.classList.remove('lb-open');
    if (lbTrigger && document.body.contains(lbTrigger)) lbTrigger.focus();
  });
  window.addEventListener('resize', function(){ if (d.open) lbSize(); });
})();
(function(){
  var w = q('fdefs');
  FAMS.forEach(function(f){
    var d = el('div'); d.appendChild(el('b', null, f.name));
    d.appendChild(document.createTextNode('Answers: ' + f.asks.charAt(0).toLowerCase() + f.asks.slice(1) + '. Evidence: ' + f.evidence.toLowerCase() + '.'));
    w.appendChild(d);
  });
  document.querySelectorAll('.ff').forEach(function(b){
    var f = b.dataset.fam;
    if (f !== 'all') b.appendChild(el('span','n', String(M.filter(function(m){ return m.family === f; }).length)));
  });
})();
buildPlan();
contributors();
render();
window.addEventListener('hashchange', function(){ route(); });
window.addEventListener('popstate', function(){ route(); });
route();
"""

JS = open('search.js', encoding='utf-8').read() + '\n' + JS
SYN = open('synonyms.json', encoding='utf-8').read()
assert '</script' not in SYN.lower()

LOGO = ('<img src="https://cdn.ncsu.edu/brand-assets/logos/ncstate-brick-2x1-red.png" '
        'alt="NC State University" onerror="this.style.display=\'none\';this.parentNode.classList.add(\'nologo\')">')

def header(page='home'):
    home_page = page == 'home'
    back = "window.scrollTo(0,0)" if home_page else "home()"
    last = ('<button class="plain" onclick="go(\'sec-sources\')">Sources</button>'
            if home_page else '<button class="plain" onclick="home()">All methods</button>')
    sid  = {'home':'search','detail':'search2','plan':'search3','before':'search4'}[page]
    handler = ('oninput="search(this.value)" onkeydown="if(event.key===\'Escape\')clearSearch()"'
               if home_page else
               'onkeydown="if(event.key===\'Enter\'&&this.value.trim()){home();document.getElementById(\'search\').value=this.value;search(this.value);}"')
    clr = ('<button class="clr" id="clr" onclick="clearSearch()" aria-label="Clear search">&#215;</button>'
           if home_page else '')
    mid = {'home':'main-home','detail':'main-detail','plan':'main-plan','before':'main-before'}[page]
    return f'''<a class="skip" href="#{mid}" onclick="return skipTo('{mid}')">Skip to main content</a>
<header class="site">
<div class="hbar"></div>
<div class="hin">
 <button class="logo" onclick="{back}" aria-label="Design Research Methods home">
  {LOGO}
  <span class="div"></span>
  <span class="txt"><b>Design Research Methods</b>College of Design</span>
 </button>
 <div class="srch" role="search">
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
  <input id="{sid}" type="search" placeholder="Search methods, students" autocomplete="off" aria-label="Search methods" {handler}>
  {clr}
 </div>
 <button class="planbtn" onclick="openPlan()" aria-label="Plan your research">Plan<span class="shortcount"></span></button>
 <nav class="top" aria-label="Browse by phase">
  <button class="r" onclick="setPhase('research')">Research</button>
  <button class="i" onclick="setPhase('insights')">Insights</button>
  <button class="d" onclick="setPhase('ideation')">Ideation</button>
  <button class="p" onclick="setPhase('proto')">Prototyping</button>
  <button class="plan" onclick="openPlan()">Plan your research<span class="shortcount"></span></button>
  <button class="plain navbefore" onclick="openBefore()">Before you collect</button>
  {last}
 </nav>
</div>
</header>'''

FOOT = '''<footer class="site"><div class="in">
 <div class="brand"><div class="rule"></div>
  <div class="t">NC STATE UNIVERSITY<span>College of Design</span></div>
 </div>
 <div class="meta">Most method cards were written by Design Studies students at NC State's College of Design. Drafted cards are marked.<br>
  Site created and maintained by Andr&eacute;s T&eacute;llez, Assistant Professor of Design Studies.<br>
  Published for students, faculty, and design practitioners.</div>
</div></footer>'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Design Research Methods | NC State University</title>
<meta name="description" content="A reference of 117 design research methods organized across the Double Diamond, with method cards written by students at NC State University.">
<meta property="og:type" content="website">
<meta property="og:title" content="Design Research Methods | NC State University">
<meta property="og:description" content="A reference of 117 design research methods organized across the Double Diamond, with method cards written by students.">
<meta property="og:url" content="https://atb1982.github.io/design-research-methods/">
<meta property="og:image" content="https://atb1982.github.io/design-research-methods/images/double-diamond.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23000'/%3E%3Cpath d='M3 16 9.5 9.5 16 16 9.5 22.5ZM16 16 22.5 9.5 29 16 22.5 22.5Z' fill='%23CC0000'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;1,400&family=Roboto+Condensed:wght@400;700&family=Roboto+Slab:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<noscript><p style="padding:24px;font:16px/1.5 Roboto,Arial,sans-serif">This site needs JavaScript to show the method cards. Please turn JavaScript on and reload the page.</p></noscript>
<div class="sr" id="status" role="status" aria-live="polite" aria-atomic="true"></div>
<script type="application/json" id="app-data">{data_json}</script>
<script type="application/json" id="syn-data">{SYN}</script>

<div id="p-home" class="page on">
{header('home')}
<main id="main-home" tabindex="-1">
<section class="hero"><div class="wrap">
 <p class="kicker">NC State College of Design</p>
 <h1>Design Research<br><em>Methods</em></h1>
 <p class="lede">A working reference of 117 methods used to plan research, make sense of what it
  finds, generate ideas, and test them. Most detailed cards were researched and written by
  students. Eighteen more were drafted for the site and are marked as drafts until they are reviewed.</p>
 <p class="herocta"><button class="herobtn" onclick="openPlan()">Plan your research</button> <button class="herobtn" onclick="openBefore()">Before you collect</button></p>
 <div class="chips">
  <button class="chip research" onclick="setPhase('research')">Research <span id="chipn-research"></span></button>
  <button class="chip insights" onclick="setPhase('insights')">Insights <span id="chipn-insights"></span></button>
  <button class="chip ideation" onclick="setPhase('ideation')">Ideation <span id="chipn-ideation"></span></button>
  <button class="chip proto" onclick="setPhase('proto')">Prototyping <span id="chipn-proto"></span></button>
 </div>
 <div class="stats">
  <div class="stat"><b id="stat-methods"></b><span>Methods</span></div>
  <div class="stat"><b id="stat-cards"></b><span>Student-written cards</span></div>
  <div class="stat"><b id="stat-students"></b><span>Contributors</span></div>
  <div class="stat"><b id="stat-drafts"></b><span>Draft entries awaiting review</span></div>
 </div>
</div></section>

<div class="filters" role="group" aria-label="Filter methods by phase"><div class="in">
 <button class="fb on all" id="fb-all" data-phase="all" aria-pressed="true" onclick="setPhase('all')">All methods</button>
 <button class="fb research" data-phase="research" aria-pressed="false" onclick="setPhase('research')">Research</button>
 <button class="fb insights" data-phase="insights" aria-pressed="false" onclick="setPhase('insights')">Insights</button>
 <button class="fb ideation" data-phase="ideation" aria-pressed="false" onclick="setPhase('ideation')">Ideation</button>
 <button class="fb proto" data-phase="proto" aria-pressed="false" onclick="setPhase('proto')">Prototyping</button>
 <span class="fcount" id="fcount"></span>
</div>
<div class="in fr" role="group" aria-label="Filter methods by evidence family">
 <span class="flab" id="flab">Evidence family</span>
 <button class="ff on" data-fam="all" aria-pressed="true" onclick="setFam('all')">All</button>
 <button class="ff" data-fam="read" aria-pressed="false" onclick="setFam('read')">Read</button>
 <button class="ff" data-fam="ask" aria-pressed="false" onclick="setFam('ask')">Ask</button>
 <button class="ff" data-fam="watch" aria-pressed="false" onclick="setFam('watch')">Watch</button>
 <button class="ff" data-fam="test" aria-pressed="false" onclick="setFam('test')">Test</button>
 <button class="ff" data-fam="make" aria-pressed="false" onclick="setFam('make')">Make</button>
 <button class="ff" data-fam="analyze" aria-pressed="false" onclick="setFam('analyze')">Analyze</button>
 <button class="fhelp" id="fhelp" aria-expanded="false" aria-controls="fpanel" onclick="toggleFamHelp()">What are families?</button>
</div></div>
<div class="fpanel" id="fpanel"><div class="in">
 <p class="lead">The phase tells you when in a project a designer would reach for a method. The family tells you what kind of evidence the method produces, which decides what a finding from it can support. A method sits in one phase and one family. To build a sound argument, choose methods from different families.</p>
 <div class="fdefs" id="fdefs"></div>
</div></div>
<div class="fnote" id="fnote"><div class="in"><span id="fnote-text"></span><button type="button" onclick="setFam('all')">Show all families</button></div></div>
<div class="sbanner" id="sbanner"><div class="in">
 <span id="btext"></span><button onclick="clearSearch()">Clear search</button>
</div></div>

<section class="dd" id="sec-dd"><div class="wrap">
 <p class="kicker" style="color:var(--red)">Framework</p>
 <h2>The Double Diamond</h2>
 <p class="intro">The Double Diamond, published by the UK Design Council in 2005, describes design
  as two cycles of opening up and narrowing down. The first diamond works on the problem: research
  widens what the team knows, then insight work converges on a clear definition of what is actually
  wrong. The second diamond works on the solution: ideation opens the field of possible responses,
  then prototyping and testing narrow it to something that holds up in use. Every method in this
  collection is filed under the moment in that sequence where it does its work.</p>
 <img class="diagram" src="images/double-diamond.png" alt="The Double Diamond model: Discover and Define form the first diamond, Develop and Deliver form the second">
 <div class="ddgrid">
  <div class="ddc research"><div class="step">First diamond, opening up</div><div class="ph">Research</div>
   <h3>Discover</h3><p>Gather evidence about people, contexts, and the conditions a design has to work in.</p>
   <div class="n" id="ddn-research"></div></div>
  <div class="ddc insights"><div class="step">First diamond, narrowing down</div><div class="ph">Insights</div>
   <h3>Define</h3><p>Interpret what the research found and settle on the problem worth solving.</p>
   <div class="n" id="ddn-insights"></div></div>
  <div class="ddc ideation"><div class="step">Second diamond, opening up</div><div class="ph">Ideation</div>
   <h3>Develop</h3><p>Generate a wide field of possible responses before committing to any one.</p>
   <div class="n" id="ddn-ideation"></div></div>
  <div class="ddc proto"><div class="step">Second diamond, narrowing down</div><div class="ph">Prototyping</div>
   <h3>Deliver</h3><p>Make ideas tangible and find out what survives contact with real use.</p>
   <div class="n" id="ddn-proto"></div></div>
 </div>
</div></section>

<section class="phase" id="sec-research"><div class="wrap"><div class="phead">
 <div class="pleft"><span class="badge research">Research</span><h2>Research methods</h2></div>
 <p>Gathering evidence about people, contexts, and existing conditions through direct and indirect inquiry.</p>
</div><div class="grid" id="grid-research"></div></div></section>

<section class="phase" id="sec-insights"><div class="wrap"><div class="phead">
 <div class="pleft"><span class="badge insights">Insights</span><h2>Insights methods</h2></div>
 <p>Organizing and interpreting what research found, so a team can agree on the real problem.</p>
</div><div class="grid" id="grid-insights"></div></div></section>

<section class="phase" id="sec-ideation"><div class="wrap"><div class="phead">
 <div class="pleft"><span class="badge ideation">Ideation</span><h2>Ideation methods</h2></div>
 <p>Generating and exploring many possible directions before narrowing to one.</p>
</div><div class="grid" id="grid-ideation"></div></div></section>

<section class="phase" id="sec-proto"><div class="wrap"><div class="phead">
 <div class="pleft"><span class="badge proto">Prototyping</span><h2>Prototyping methods</h2></div>
 <p>Making ideas tangible and evaluating them through simulation, expert review, and user feedback.</p>
</div><div class="grid" id="grid-proto"></div></div></section>

<section class="sources" id="sec-sources"><div class="wrap">
 <p class="kicker">Further reading</p>
 <h2>Additional resources</h2>
 <p class="sub">The books, toolkits, and reference sites that this collection draws on. Library
  links require an NC State login.</p>
 <div class="sgrid">
  <div class="scard"><h3>Books via University Libraries</h3><ul>
   <li><a href="https://ebookcentral.proquest.com/lib/ncsu/detail.action?docID=6039458" target="_blank" rel="noopener">Universal Methods of Design, expanded and revised. Bruce Hanington and Bella Martin</a></li>
   <li><a href="https://ebookcentral.proquest.com/lib/ncsu/detail.action?docID=861699" target="_blank" rel="noopener">101 Design Methods. Vijay Kumar</a></li>
   <li><a href="https://www-taylorfrancis-com.prox.lib.ncsu.edu/books/edit/10.4324/9781003182443/routledge-companion-design-research-paul-rodgers-joyce-yee" target="_blank" rel="noopener">The Routledge Companion to Design Research. Paul A. Rodgers and Joyce Yee</a></li>
   <li><a href="https://proxying.lib.ncsu.edu/index.php?url=https://search-ebscohost-com.prox.lib.ncsu.edu/login.aspx?direct=true&amp;db=nlebk&amp;AN=658202&amp;site=ehost-live&amp;scope=site" target="_blank" rel="noopener">The Design of Everyday Things. Don Norman</a></li>
  </ul></div>
  <div class="scard"><h3>Toolkits</h3><ul>
   <li><a href="https://www.designkit.org/resources/1.html" target="_blank" rel="noopener">IDEO.org, The Field Guide to Human-Centered Design</a></li>
   <li><a href="https://dschool.stanford.edu/tools/design-thinking-bootleg" target="_blank" rel="noopener">d.school, Design Thinking Bootleg</a></li>
   <li><a href="https://apphaus.sap.com/toolkit" target="_blank" rel="noopener">SAP, Innovation Toolkit</a></li>
   <li><a href="https://www.luma-institute.com" target="_blank" rel="noopener">LUMA Institute, Innovating for People</a></li>
   <li><a href="https://servicedesigntools.org" target="_blank" rel="noopener">Oblo, Service Design Tools</a></li>
   <li><a href="http://designresearchmethods.com/tools" target="_blank" rel="noopener">PolyU, Design Research Methods</a></li>
   <li><a href="https://openpracticelibrary.com" target="_blank" rel="noopener">Red Hat, Open Practice Library</a></li>
   <li><a href="http://learndbir.org/tools/co-design-tools" target="_blank" rel="noopener">DBIR, Co-Design Tools</a></li>
   <li><a href="https://digital.gov/guides/hcd/" target="_blank" rel="noopener">Digital.gov, Human-Centered Design Guide Series</a></li>
   <li><a href="https://methods.18f.gov/" target="_blank" rel="noopener">18F, Methods</a></li>
   <li><a href="https://www.innovation.wiki/en/" target="_blank" rel="noopener">verrocchio Institute, Innovation Wiki</a></li>
  </ul></div>
  <div class="scard"><h3>Other resources</h3><ul>
   <li><a href="https://www.designcouncil.org.uk/our-resources/the-double-diamond/" target="_blank" rel="noopener">The Double Diamond, Design Council</a></li>
   <li><a href="https://www.interaction-design.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed" target="_blank" rel="noopener">The Encyclopedia of Human-Computer Interaction</a></li>
   <li><a href="https://www.nngroup.com/articles/which-ux-research-methods/" target="_blank" rel="noopener">Nielsen Norman Group, When to Use Which User-Experience Research Methods</a></li>
   <li><a href="https://www.nngroup.com/articles/research-methods-glossary/" target="_blank" rel="noopener">Nielsen Norman Group, UX Research Methods Glossary</a></li>
   <li><a href="https://www.nngroup.com/articles/" target="_blank" rel="noopener">Nielsen Norman Group articles</a></li>
   <li><a href="https://www.healthdesign.org/certification-outreach/edac/about-ebd" target="_blank" rel="noopener">Center for Health Design, About Evidence-Based Design</a></li>
   <li><a href="https://www.usability.gov" target="_blank" rel="noopener">Usability.gov</a></li>
  </ul></div>
 </div>
</div></section>

<section class="contrib" id="sec-contributors"><div class="wrap">
 <p class="kicker">Credits</p>
 <h2>Who wrote these cards</h2>
 <p class="sub">Each student in D 492 Intro to Design Research (Spring 2026) was assigned two methods from different phases of the design
  process, researched them against published sources, and wrote the card you see here. Each
  student also chose the image shown with their cards, and the credit under every image names the
  student and the original source. Select a method to read their work.</p>
 <p class="sub lead">Project lead and editor: Andr&eacute;s T&eacute;llez, Assistant Professor of Design Studies, NC State College of Design. He designed and built this site, edited the cards, and selected the reference entries, further reading, and templates.</p>
 <div class="clist" id="clist"></div>
</div></section>
</main>
{FOOT}
</div>

<div id="p-detail" class="page">
{header('detail')}
<nav class="bc" aria-label="Breadcrumb"><div class="in">
 <button onclick="home()">All methods</button><span class="sep" aria-hidden="true">/</span>
 <button id="bc-phase" onclick="homePhase()"></button><span class="sep" aria-hidden="true">/</span>
 <span id="bc-name" aria-current="page"></span>
</div></nav>
<main id="main-detail" tabindex="-1">
<div id="dhero" class="dhero"><div class="wrap">
 <p class="eyebrow" id="d-eyebrow"></p>
 <h1 id="d-title" tabindex="-1"></h1>
 <p class="alts" id="d-alts"></p>
 <p class="by" id="d-by"></p>
 <div class="actions"><button type="button" id="b-copy" onclick="copyLink()">Copy link</button><button type="button" onclick="window.print()">Print this card</button></div>
</div></div>
<div class="dbody"><div class="dlayout">
 <aside id="d-visual" aria-label="Image"></aside>
 <div id="d-main"></div>
 <aside id="d-side" aria-label="Quick reference"></aside>
</div></div>
</main>
{FOOT}
</div>

<div id="p-plan" class="page">
{header('plan')}
<nav class="bc" aria-label="Breadcrumb"><div class="in">
 <button onclick="home()">All methods</button><span class="sep" aria-hidden="true">/</span>
 <span aria-current="page">Plan your research</span>
</div></nav>
<main id="main-plan" tabindex="-1">
<section class="phero"><div class="wrap">
 <p class="kicker">Planning tools</p>
 <h1 id="plan-title" tabindex="-1">Plan your research</h1>
 <p class="lede">Match your question to the kind of evidence it needs, choose two methods that check each other, and keep a shortlist to compare. Everything here points back to the method cards.</p>
 <div class="pjump" role="navigation" aria-label="On this page">
  <button onclick="go('plan-q')">Match your question</button>
  <button onclick="go('plan-pair')">Choose two methods</button>
  <button onclick="go('plan-short')">Your shortlist <span class="shortcount"></span></button>
  <button onclick="openBefore()">Before you collect</button>
 </div>
</div></section>

<section class="psec" id="plan-q"><div class="wrap">
 <h2>What does your question ask?</h2>
 <p class="sub">Most questions carry a verb that decides which kind of evidence you need before you choose a method. Pick the option that is closest to your question. If you have several sub-questions, run this once for each.</p>
 <div class="qopts" id="qopts" role="radiogroup" aria-label="What your question asks"></div>
 <div class="qres" id="qres" aria-live="polite"></div>
</div></section>

<section class="psec alt" id="plan-pair"><div class="wrap">
 <h2>Choose two methods that check each other</h2>
 <p class="sub">One method leaves a gap that a reader can see. A second method from a different family covers it, and that is what turns a set of findings into an argument. Start from the mode of your project, or test a pair you already have in mind.</p>
 <h3 class="ph3">Start from your mode</h3>
 <p class="sub s2">Your mode is a commitment about what you will produce and what you can claim. Write one sentence describing what you will hand in at the end, then choose the mode that matches that sentence.</p>
 <div class="qopts modes" id="mopts" role="radiogroup" aria-label="Mode of your project"></div>
 <div class="qres" id="mres" aria-live="polite"></div>
 <h3 class="ph3 gap">Check your own pair</h3>
 <div class="chkform">
  <div class="fld"><label for="pa">First method</label><select id="pa"></select></div>
  <div class="fld"><label for="pb">Second method</label><select id="pb"></select></div>
 </div>
 <div class="qres" id="cres" aria-live="polite"></div>
</div></section>

<section class="psec" id="plan-short"><div class="wrap">
 <h2>Your shortlist</h2>
 <p class="sub">Add methods from a card, from the lists above, or from a pair. Compare them side by side, then copy or print the list. The list stays on this device and is not sent anywhere.</p>
 <div id="short"></div>
</div></section>
</main>
{FOOT}
</div>

<div id="p-before" class="page">
{header('before')}
<nav class="bc" aria-label="Breadcrumb"><div class="in">
 <button onclick="home()">All methods</button><span class="sep" aria-hidden="true">/</span>
 <span aria-current="page">Before you collect</span>
</div></nav>
<main id="main-before" tabindex="-1">
<section class="phero"><div class="wrap">
 <p class="kicker">Planning tools</p>
 <h1 id="before-title" tabindex="-1">Before you collect</h1>
 <p class="lede">Most of what goes wrong in a student research project is set before the first interview or observation. Settle these six things first, then collect. This page does not replace your instructor&rsquo;s guidance or your institution&rsquo;s research ethics review.</p>
 <div class="pjump" role="navigation" aria-label="On this page">
  <button onclick="go('bt-plan')">Plan</button>
  <button onclick="go('bt-analysis')">Analysis</button>
  <button onclick="go('bt-consent')">Consent</button>
  <button onclick="go('bt-protocol')">Protocol</button>
  <button onclick="go('bt-numbers')">Numbers</button>
  <button onclick="go('bt-name')">Naming</button>
  <button onclick="go('bt-templates')">All templates</button>
 </div>
</div></section>

<section class="psec" id="bt-plan"><div class="wrap">
 <h2>Write the plan first</h2>
 <p class="sub">A plan written in advance lets you tell a reader what changed and why. A plan written afterward only describes what happened.</p>
 <ul class="btlist">
  <li><b>Question and mode.</b> One main question, three to five sub-questions, and the mode of your project: into, through, or for design.</li>
  <li><b>Two methods from different families.</b> Each should cover what the other cannot show. Write the checking sentence: &ldquo;My second method checks my first because &hellip;&rdquo;</li>
  <li><b>A target sample, as a number.</b> Write it before you recruit, and write what you will do if recruitment stalls. Reducing to a smaller sample and saying so is honest. Switching to a different population without saying so is not.</li>
  <li><b>A timeline with room for delay.</b> Recruitment and scheduling almost always take longer than you expect.</li>
 </ul>
 <p class="bttools" id="bt-plan-tools"></p>
 <p class="btnext"><button onclick="openPlan()">Open Plan your research</button></p>
</div></section>

<section class="psec alt" id="bt-analysis"><div class="wrap">
 <h2>Decide how you will analyze, now</h2>
 <p class="sub">Criteria written after you have seen the material tend to fit the material. Write them before.</p>
 <ul class="btlist">
  <li><b>A codebook before you code.</b> Each code has a name, a one-sentence definition, an example, and a note on what it excludes.</li>
  <li><b>A second coder.</b> Ask someone to code about 20 percent of your material with your codebook. Record where you disagreed and how you settled it.</li>
  <li><b>Scales defined in advance.</b> If you rate or score things, write what a 1 and a 5 mean before you look at the items.</li>
  <li><b>An exclusion rule.</b> Decide what counts as off-topic or unusable before you see the material.</li>
  <li><b>What would count against your claim.</b> Name the evidence that would weaken your argument, then look for it.</li>
 </ul>
 <p class="bttools" id="bt-analysis-tools"></p>
</div></section>

<section class="psec" id="bt-consent"><div class="wrap">
 <h2>Settle consent before you contact anyone</h2>
 <p class="sub">Consent is arranged in advance, and your paper should say what you did. Whether your project needs formal review is decided by your instructor or institution, and it is decided before you collect.</p>
 <ul class="btlist">
  <li><b>Tell people what they are joining.</b> Who you are, what the project is, what you will ask or do, how long it takes, and that taking part is voluntary and they may stop at any time.</li>
  <li><b>Ask for recording separately.</b> Audio, video, and photos each need their own yes.</li>
  <li><b>Promise only what you will do.</b> If you promise anonymity, no participant is named anywhere in your paper, including the appendix. If you promise to delete recordings, delete them.</li>
  <li><b>Take extra care with some groups.</b> Minors, people recruited through health or support communities, and people affected by a recent crisis need added protection. If your question points there, talk to your instructor or your ethics office before you contact anyone.</li>
  <li><b>Store data where only you can reach it,</b> and remove identifying details from transcripts.</li>
 </ul>
 <p class="bttools" id="bt-consent-tools"></p>
</div></section>

<section class="psec alt" id="bt-protocol"><div class="wrap">
 <h2>Write the protocol, then keep the record</h2>
 <p class="sub">A protocol is what you will do, written so that another person could do it. A record shows what you did.</p>
 <ul class="btlist">
  <li><b>Try your instrument once.</b> Run the interview guide, survey, or observation sheet with a classmate before you use it with participants.</li>
  <li><b>Write a question that could surprise you.</b> Include one that could return an answer you do not want. Ask about a specific recent event instead of habits.</li>
  <li><b>Sample different times.</b> When you observe, spread sessions across days and hours so one unusual hour does not stand for the whole.</li>
  <li><b>Keep description and interpretation apart.</b> Write what happened in one column and what you think it means in another.</li>
  <li><b>Log every change.</b> Record the date, what changed, and why. A study that changed is normal. A study whose changes are hidden looks unreliable.</li>
 </ul>
 <p class="bttools" id="bt-protocol-tools"></p>
</div></section>

<section class="psec" id="bt-numbers"><div class="wrap">
 <h2>Report numbers honestly</h2>
 <p class="sub">Small samples are fine for a first project. Presenting them as larger than they are is the problem.</p>
 <ul class="btlist">
  <li><b>Below about 20 responses,</b> report counts (&ldquo;7 of 12&rdquo;), not percentages.</li>
  <li><b>Target and actual.</b> Report both, and the gap, in your methods section.</li>
  <li><b>Who the sample can speak for.</b> A convenience sample describes the people you reached. Do not call it representative.</li>
  <li><b>What a rating meant.</b> If you report scores, say what the scale meant and who defined it.</li>
  <li><b>Agreement between coders.</b> Report the number of agreements (&ldquo;14 of 16 excerpts&rdquo;) and how you settled the rest.</li>
 </ul>
 <p class="bttools" id="bt-numbers-tools"></p>
</div></section>

<section class="psec alt" id="bt-name"><div class="wrap">
 <h2>Name the method for what you actually did</h2>
 <p class="sub">A method name is a claim about rigor, and a reader who knows the method will check it. If what you did does not meet the requirements, use the name that fits.</p>
 <table class="bttab">
  <thead><tr><th scope="col">If you wrote</th><th scope="col">And what you did was</th><th scope="col">Use instead</th></tr></thead>
  <tbody>
   <tr><td>Focus group</td><td>Participants commented on a shared board over several days, without meeting</td><td>Asynchronous expert review</td></tr>
   <tr><td>Thematic analysis</td><td>You counted word frequencies or made a word cloud</td><td>Word frequency analysis</td></tr>
   <tr><td>Systematic literature review</td><td>You gathered sources without stated inclusion criteria or a search protocol</td><td>Purposive or scoping literature review</td></tr>
   <tr><td>A/B test</td><td>Each respondent saw both versions and picked one</td><td>Forced choice preference test</td></tr>
   <tr><td>Heuristic evaluation</td><td>One person applied part of a heuristic set</td><td>Informal expert review</td></tr>
   <tr><td>Case study</td><td>You interviewed people at one organization</td><td>Interview study</td></tr>
  </tbody>
 </table>
 <p class="sub">To use the stronger name, meet its requirements. A systematic review needs stated inclusion criteria and a documented search. A heuristic evaluation needs several evaluators and a complete heuristic set. Thematic analysis needs a codebook and coded excerpts.</p>
 <p class="bttools" id="bt-name-tools"></p>
</div></section>

<section class="psec" id="bt-templates"><div class="wrap">
 <h2>All templates</h2>
 <p class="sub">Each file is a starting point to fill in and adapt. The same files appear on the method cards where they apply.</p>
 <ul class="btall" id="bt-all"></ul>
 <p class="btnote">These templates were drafted for this site. They are not official forms and are not course materials. The consent script does not replace formal review, and your instructor or institution decides what your project needs.</p>
</div></section>
</main>
{FOOT}
</div>

<dialog id="lb" class="lb" aria-label="Larger image">
 <button type="button" class="lbx" aria-label="Close larger image" onclick="closeLightbox()">&times;</button>
 <div class="lbin"><div class="lbscroll" id="lb-scroll"><img id="lb-img" alt=""></div><p class="lbhint" id="lb-hint" hidden>Drag to move around the image, or pinch to zoom.</p><div class="lbcap" id="lb-cap"></div></div>
</dialog>

<script>{JS}</script>
</body>
</html>'''

open('index.html','w',encoding='utf-8').write(html)

# safety
import re
js = html.split('<script>')[1].split('</script>')[0]
bad = [x for x in re.findall(r"'[^'\\]*(?:\\.[^'\\]*)*'", js) if '</' in x]
print('unsafe JS literals:', bad or 'none')
print('HTML entities in JS:', 'none' if not re.search(r'&[a-z]+;', js) else 'FOUND')
print(f'index.html written: {len(html):,} bytes')
