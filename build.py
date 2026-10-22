import json
_d = json.load(open('data.json', encoding='utf-8'))
_ov = json.load(open('overview_links.json', encoding='utf-8'))
_ids = {m['id']: m for m in _d['methods']}
for _k, _v in _ov.items():
    assert _k in _ids and _ids[_k]['kind'] == 'brief', _k
    for _l in _v:
        assert _l['url'].startswith('https://') and _l['title'] and _l['publisher'], _l
    _ids[_k]['overview'] = _v
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
#sec-dd,#sec-research,#sec-insights,#sec-ideation,#sec-proto,#sec-sources,#sec-contributors{scroll-margin-top:122px}
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
.card .ph{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.3px;
 text-transform:uppercase;display:block;margin-bottom:6px}
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
.pairbox{background:#111;color:#fff;border-radius:6px;padding:26px;margin-top:40px}
.pairbox .lab{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.8px;
 text-transform:uppercase;color:var(--red-lt);margin-bottom:8px}
.pairbox h3{font-family:'Roboto Slab',Georgia,serif;font-size:17px;font-weight:700;margin-bottom:14px}
.pairbox p{font-size:14px;line-height:1.75;color:rgba(255,255,255,.62)}
.pairbox button{margin-top:15px;background:rgba(255,255,255,.1);padding:7px 14px;border-radius:3px;
 font-size:12.5px;color:rgba(255,255,255,.72)}
.pairbox button:hover{background:rgba(255,255,255,.18);color:#fff}

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
.ovlist .on{display:block;font-size:13px;color:var(--g700);margin-top:2px}
.ovnote{font-size:12.5px;color:var(--gtxt);margin-top:10px}
.exbox p+p{margin-top:12px}
.noimg{background:var(--g100);border:2px dashed var(--g300);border-radius:5px;padding:30px 22px;text-align:center}
.noimg .t{font-family:'Roboto Condensed',sans-serif;font-size:11.5px;font-weight:700;letter-spacing:1.3px;
 text-transform:uppercase;color:var(--g600);margin-bottom:8px}
.noimg p{font-size:12.5px;color:var(--g600);line-height:1.55}
.ddind{background:#111;border-radius:5px;padding:17px}
.ddind .lab{font-family:'Roboto Condensed',sans-serif;font-size:11px;font-weight:700;letter-spacing:1.4px;
 text-transform:uppercase;color:rgba(255,255,255,.7);margin-bottom:13px}
.ddbars{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:9px}
.ddbars i{height:9px;border-radius:2px;background:rgba(255,255,255,.12);display:block}
.ddbars i.on.research{background:var(--research)}
.ddbars i.on.insights{background:var(--insights)}
.ddbars i.on.ideation{background:var(--ideation)}
.ddbars i.on.proto{background:var(--proto)}
.ddlabs{display:grid;grid-template-columns:repeat(4,1fr);gap:4px}
.ddlabs span{font-family:'Roboto Condensed',sans-serif;font-size:10.5px;font-weight:700;letter-spacing:.2px;
 text-transform:uppercase;color:rgba(255,255,255,.66);text-align:center}
.ddlabs span.on{color:#fff}
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

@media(max-width:980px){
 .dlayout{grid-template-columns:minmax(0,1fr);grid-template-rows:none;grid-template-areas:"visual" "main" "side"}
 .sgrid,.ddgrid{grid-template-columns:1fr 1fr}
 nav.top{display:none}
 .srch{max-width:none}
 .phead p{text-align:left}
}
@media(max-width:640px){
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
 header.site,.filters,.sbanner,footer.site,.bc,.skip,.actions,.more,.seeall,.pairbox button,#p-home,dialog.lb,.zoomhint{display:none!important}
 #p-detail{display:block!important}
 body{color:#000;background:#fff}
 .dhero{background:none!important;padding:0 0 14px;border-bottom:2px solid #000}
 .dhero *{color:#000!important}
 .dbody{padding:18px 0;max-width:none}
 .dlayout{display:block}
 .sb,.blk,.cite,.tipbox,.exbox{break-inside:avoid}
 .sb img{max-width:70%}
 .cite a,.sb figcaption a{color:#000}
 .pairbox{background:none;color:#000;border:1px solid #000}
 .pairbox *{color:#000!important}
 .ddind{background:none;border:1px solid #999}
 .ddind *{color:#000!important}
}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}html{scroll-behavior:auto}}
"""

JS = r"""
var APP = JSON.parse(document.getElementById('app-data').textContent);
var M = APP.methods, PC = APP.phaseConfig, PCOL = APP.phaseColor;
var BY = {}; M.forEach(function(m){ BY[m.id] = m; });
var phase = 'all', query = '', ALTS = [], cur = 'research';
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
function route(o){
  o = o || {};
  var m = methodFromHash(), key = m ? m.id : '';
  if (key === shownKey && !o.force) return;
  closeLightbox();
  var wasDetail = !!shownKey;
  shownKey = key;
  if (m){
    cur = m.phase; detail(m);
    q('p-home').classList.remove('on'); q('p-detail').classList.add('on');
    document.title = m.name + ' | ' + SITE_TITLE;
    jumpTo(0);
    q('d-title').focus({preventScroll:true});
  } else {
    q('p-detail').classList.remove('on'); q('p-home').classList.add('on');
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
  render();
  var n = p==='all' ? M.length : M.filter(function(m){ return m.phase===p; }).length;
  announce(p==='all' ? 'Showing all ' + n + ' methods' : 'Showing ' + n + ' ' + PC[p].name + ' methods');
  if (p !== 'all') setTimeout(function(){ go('sec-'+p); }, 70);
}

/* full-text index: every field of a card is searchable, with word forms and related terms */
function idx(m){
  if (m._ix) return m._ix;
  var join = function(a){ return (a || []).join(' '); };
  var fields = [
    ['Description', m.whatItIs || ''],
    ['When to use it', join(m.whenToUse)],
    ['Steps', join(m.howToDoIt)],
    ['What you need', join(m.whatYouNeed)],
    ['Tips', join(m.tips)],
    ['Common mistakes', join(m.mistakes)],
    ['Example', m.example || ''],
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
  var n = phase==='all' ? M.length : M.filter(function(m){ return m.phase===phase; }).length;
  q('fcount').textContent = n + (n===1?' method':' methods');
}

/* ---------- card grid ---------- */
function render(){
  PHASES.forEach(function(p){
    var g = q('grid-'+p); if (!g) return;
    var list = M.filter(function(m){
      if (m.phase !== p) return false;
      if (!query && phase!=='all' && phase!==p) return false;
      return true;
    }).map(function(m, i){ return {m:m, ev:evalCard(m), i:i}; })
      .filter(function(o){ return o.ev !== null; });
    if (query){ list.sort(function(a,b){ return a.ev.rank - b.ev.rank || a.i - b.i; }); }
    q('sec-'+p).classList.toggle('nomatch', !!query && !list.length);
    g.innerHTML = '';
    if (!list.length){
      if (!query) g.appendChild(el('div','empty','No methods.'));
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
      b.appendChild(el('span','ph '+m.phase, PC[m.phase].name));
      var h = el('h3');
      var ha = document.createElement('a');
      ha.href = '#' + m.id;
      ha.addEventListener('click', function(){ savedY = window.scrollY || 0; savedId = m.id; });
      if (query) ha.innerHTML = mark(m.name, alt); else ha.textContent = m.name;
      h.appendChild(ha);
      b.appendChild(h);
      var snip = m.whatItIs.length > 112 ? m.whatItIs.slice(0,112) + '…' : m.whatItIs;
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
        by.appendChild(el('span','ref-tag','Reference entry'));
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
  {k:'Universal Methods of Design', url:'https://ebookcentral.proquest.com/lib/ncsu/detail.action?docID=6039458', gated:true},
  {k:'101 Design Methods', url:'https://ebookcentral.proquest.com/lib/ncsu/detail.action?docID=861699', gated:true},
  {k:'The Field Guide to Human-Centered Design', url:'https://www.designkit.org/resources/1.html', gated:false},
  {k:'Innovating for People', url:'https://www.luma-institute.com', gated:false},
  {k:'The User Experience Team of One', url:'https://rosenfeldmedia.com/books/the-user-experience-team-of-one/', gated:false}
];
function bookInfo(name){
  for (var i = 0; i < BOOKS.length; i++){ if (String(name).indexOf(BOOKS[i].k) === 0) return BOOKS[i]; }
  return null;
}
function detail(m){
  var pc = PC[m.phase];
  q('bc-phase').textContent = pc.name;
  q('bc-name').textContent  = m.name;

  var hero = q('dhero'); hero.className = 'dhero ' + m.phase;
  q('d-eyebrow').textContent = pc.name + ' · ' + pc.ddPhase;
  q('d-title').textContent   = m.name;
  q('d-alts').textContent    = (m.altNames && m.altNames.length) ? 'Also known as ' + m.altNames.join(', ') : '';
  var by = q('d-by'); by.innerHTML = '';
  if (m.student){
    by.appendChild(document.createTextNode('Card written by '));
    var sb = el('b', null, m.student); sb.style.fontWeight = '700';
    by.appendChild(sb);
    by.appendChild(document.createTextNode(', a student in D 492 Intro to Design Research, ' + (m.semester || 'Spring 2026')));
  } else {
    by.appendChild(el('em', null, 'Reference entry, not yet documented by a student'));
  }

  /* main column */
  var main = q('d-main'); main.innerHTML = '';
  if (m.kind === 'brief'){
    main.appendChild(el('div','notice',
      'This method has a short reference entry. Full documentation is written by students, and this card is available for a future class to complete.'));
  }
  section(main, 'What it is', el('p','prose', m.whatItIs));

  if (m.kind === 'full'){
    if (m.whenToUse && m.whenToUse.length){
      var u = el('ul','wlist');
      m.whenToUse.forEach(function(x){
        var li = el('li'); li.appendChild(el('span','d')); li.appendChild(el('span',null,x)); u.appendChild(li);
      });
      section(main, 'When to use it', u);
    }
    if (m.howToDoIt && m.howToDoIt.length){
      var o = el('ol','slist');
      m.howToDoIt.forEach(function(x){ o.appendChild(el('li', null, x)); });
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
      var d = el('div','cite');
      var parts = String(s).split(/(https?:\/\/\S+)/);
      parts.forEach(function(p){
        if (/^https?:\/\//.test(p)){
          var a = document.createElement('a');
          a.href = p; a.target = '_blank'; a.rel = 'noopener'; a.textContent = p;
          d.appendChild(a);
        } else if (p) {
          d.appendChild(document.createTextNode(p));
        }
      });
      sw.appendChild(d);
    });
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
      lu.appendChild(li);
    });
    section(main, 'Where this method appears in the course books', lu);
  }

  /* paired method */
  if (m.pairedWith && BY[m.pairedWith]){
    var p2 = BY[m.pairedWith];
    var box = el('div','pairbox');
    box.appendChild(el('div','lab','Paired in the same submission'));
    box.appendChild(el('h3', null, m.name + ' and ' + p2.name));
    box.appendChild(el('p', null,
      m.student + ' documented both methods together, one from the ' + PC[m.phase].name +
      ' phase and one from the ' + PC[p2.phase].name +
      ' phase, and described how the two work in sequence on a single project.'));
    var btn = el('button', null, 'Open the ' + p2.name + ' card');
    btn.addEventListener('click', function(){ open(p2.id); });
    box.appendChild(btn);
    main.appendChild(box);
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
  var bars = el('div','ddbars'), labs = el('div','ddlabs');
  PHASES.forEach(function(p){
    var i = document.createElement('i');
    i.className = (p===m.phase ? 'on ' + p : '');
    bars.appendChild(i);
    var s = el('span', p===m.phase ? 'on' : null, PC[p].ddPhase);
    labs.appendChild(s);
  });
  ind.appendChild(bars); ind.appendChild(labs);
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

def header(home_page=True):
    back = "window.scrollTo(0,0)" if home_page else "home()"
    last = ('<button class="plain" onclick="go(\'sec-sources\')">Sources</button>'
            if home_page else '<button class="plain" onclick="home()">All methods</button>')
    sid  = 'search' if home_page else 'search2'
    handler = ('oninput="search(this.value)" onkeydown="if(event.key===\'Escape\')clearSearch()"'
               if home_page else
               'onkeydown="if(event.key===\'Enter\'&&this.value.trim()){home();document.getElementById(\'search\').value=this.value;search(this.value);}"')
    clr = ('<button class="clr" id="clr" onclick="clearSearch()" aria-label="Clear search">&#215;</button>'
           if home_page else '')
    mid = 'main-home' if home_page else 'main-detail'
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
 <nav class="top" aria-label="Browse by phase">
  <button class="r" onclick="setPhase('research')">Research</button>
  <button class="i" onclick="setPhase('insights')">Insights</button>
  <button class="d" onclick="setPhase('ideation')">Ideation</button>
  <button class="p" onclick="setPhase('proto')">Prototyping</button>
  {last}
 </nav>
</div>
</header>'''

FOOT = '''<footer class="site"><div class="in">
 <div class="brand"><div class="rule"></div>
  <div class="t">NC STATE UNIVERSITY<span>College of Design</span></div>
 </div>
 <div class="meta">Method cards written by students<br>
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
{header(True)}
<main id="main-home" tabindex="-1">
<section class="hero"><div class="wrap">
 <p class="kicker">NC State College of Design</p>
 <h1>Design Research<br><em>Methods</em></h1>
 <p class="lede">A working reference of 117 methods used to plan research, make sense of what it
  finds, generate ideas, and test them. The detailed cards were researched and written by
  students.</p>
 <div class="chips">
  <button class="chip research" onclick="setPhase('research')">Research <span id="chipn-research"></span></button>
  <button class="chip insights" onclick="setPhase('insights')">Insights <span id="chipn-insights"></span></button>
  <button class="chip ideation" onclick="setPhase('ideation')">Ideation <span id="chipn-ideation"></span></button>
  <button class="chip proto" onclick="setPhase('proto')">Prototyping &amp; Testing <span id="chipn-proto"></span></button>
 </div>
 <div class="stats">
  <div class="stat"><b id="stat-methods"></b><span>Methods</span></div>
  <div class="stat"><b id="stat-cards"></b><span>Student-written cards</span></div>
  <div class="stat"><b id="stat-students"></b><span>Contributors</span></div>
 </div>
</div></section>

<div class="filters" role="group" aria-label="Filter methods by phase"><div class="in">
 <button class="fb on all" id="fb-all" data-phase="all" aria-pressed="true" onclick="setPhase('all')">All methods</button>
 <button class="fb research" data-phase="research" aria-pressed="false" onclick="setPhase('research')">Research</button>
 <button class="fb insights" data-phase="insights" aria-pressed="false" onclick="setPhase('insights')">Insights</button>
 <button class="fb ideation" data-phase="ideation" aria-pressed="false" onclick="setPhase('ideation')">Ideation</button>
 <button class="fb proto" data-phase="proto" aria-pressed="false" onclick="setPhase('proto')">Prototyping &amp; Testing</button>
 <span class="fcount" id="fcount"></span>
</div></div>
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
  <div class="ddc proto"><div class="step">Second diamond, narrowing down</div><div class="ph">Prototyping &amp; Testing</div>
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
 <div class="pleft"><span class="badge proto">Prototyping &amp; Testing</span><h2>Prototyping and testing methods</h2></div>
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
 <p class="sub">Each student was assigned two methods from different phases of the design
  process, researched them against published sources, and wrote the card you see here. Each
  student also chose the image shown with their cards, and the credit under every image names the
  student and the original source. Select a method to read their work.</p>
 <div class="clist" id="clist"></div>
</div></section>
</main>
{FOOT}
</div>

<div id="p-detail" class="page">
{header(False)}
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
