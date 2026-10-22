/* Search helpers: light stemming (Porter), spelling and word-form groups, related-term expansion.
   Data comes from synonyms.json: {"forms": [[word, word, ...]], "related": [[term, term, ...]]} */
var Search = (function(){
  var step2list = {ational:'ate',tional:'tion',enci:'ence',anci:'ance',izer:'ize',bli:'ble',alli:'al',entli:'ent',eli:'e',
    ousli:'ous',ization:'ize',ation:'ate',ator:'ate',alism:'al',iveness:'ive',fulness:'ful',ousness:'ous',aliti:'al',
    iviti:'ive',biliti:'ble',logi:'log'};
  var step3list = {icate:'ic',ative:'',alize:'al',iciti:'ic',ical:'ic',ful:'',ness:''};
  var c = '[^aeiou]', v = '[aeiouy]', C = c + '[^aeiouy]*', V = v + '[aeiou]*';
  var mgr0 = '^(' + C + ')?' + V + C, meq1 = '^(' + C + ')?' + V + C + '(' + V + ')?$';
  var mgr1 = '^(' + C + ')?' + V + C + V + C, s_v = '^(' + C + ')?' + v;

  function porter(w){
    var stem, suffix, firstch, re, re2, re3, re4, fp;
    if (w.length < 3) return w;
    firstch = w.substr(0,1);
    if (firstch === 'y') w = firstch.toUpperCase() + w.substr(1);
    re = /^(.+?)(ss|i)es$/; re2 = /^(.+?)([^s])s$/;
    if (re.test(w)) w = w.replace(re, '$1$2'); else if (re2.test(w)) w = w.replace(re2, '$1$2');
    re = /^(.+?)eed$/; re2 = /^(.+?)(ed|ing)$/;
    if (re.test(w)){ fp = re.exec(w); re = new RegExp(mgr0); if (re.test(fp[1])) w = w.replace(/.$/, ''); }
    else if (re2.test(w)){
      fp = re2.exec(w); stem = fp[1]; re2 = new RegExp(s_v);
      if (re2.test(stem)){
        w = stem; re2 = /(at|bl|iz)$/; re3 = new RegExp('([^aeiouylsz])\\1$'); re4 = new RegExp('^' + C + v + '[^aeiouwxy]$');
        if (re2.test(w)) w = w + 'e'; else if (re3.test(w)) w = w.replace(/.$/, ''); else if (re4.test(w)) w = w + 'e';
      }
    }
    re = /^(.+?)y$/;
    if (re.test(w)){ fp = re.exec(w); stem = fp[1]; re = new RegExp(s_v); if (re.test(stem)) w = stem + 'i'; }
    re = /^(.+?)(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti|logi)$/;
    if (re.test(w)){ fp = re.exec(w); stem = fp[1]; suffix = fp[2]; re = new RegExp(mgr0); if (re.test(stem)) w = stem + step2list[suffix]; }
    re = /^(.+?)(icate|ative|alize|iciti|ical|ful|ness)$/;
    if (re.test(w)){ fp = re.exec(w); stem = fp[1]; suffix = fp[2]; re = new RegExp(mgr0); if (re.test(stem)) w = stem + step3list[suffix]; }
    re = /^(.+?)(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ou|ism|ate|iti|ous|ive|ize)$/;
    re2 = /^(.+?)(s|t)(ion)$/;
    if (re.test(w)){ fp = re.exec(w); stem = fp[1]; re = new RegExp(mgr1); if (re.test(stem)) w = stem; }
    else if (re2.test(w)){ fp = re2.exec(w); stem = fp[1] + fp[2]; re2 = new RegExp(mgr1); if (re2.test(stem)) w = stem; }
    re = /^(.+?)e$/;
    if (re.test(w)){
      fp = re.exec(w); stem = fp[1]; re = new RegExp(mgr1); re2 = new RegExp(meq1); re3 = new RegExp('^' + C + v + '[^aeiouwxy]$');
      if (re.test(stem) || (re2.test(stem) && !(re3.test(stem)))) w = stem;
    }
    re = /ll$/; re2 = new RegExp(mgr1);
    if (re.test(w) && re2.test(w)) w = w.replace(/.$/, '');
    if (firstch === 'y') w = firstch.toLowerCase() + w.substr(1);
    return w;
  }

  var FORM = {}, APART = {}, RELATED = [], memo = {}, VOCAB = {};
  var STOP = {a:1, an:1, the:1, of:1, to:1, for:1, and:1, or:1, in:1, on:1, with:1, is:1, are:1, do:1, does:1, my:1, me:1};

  function words(t){ return (String(t).toLowerCase().match(/[a-z0-9]+/g) || []); }
  function stem(w){
    w = String(w).toLowerCase().replace(/[^a-z0-9]/g, '');
    if (w in memo) return memo[w];
    var s = APART[w] || porter(w); s = FORM[s] || s; memo[w] = s; return s;
  }
  function init(syn){
    FORM = {}; APART = {}; memo = {}; RELATED = [];
    ((syn && syn.apart) || []).forEach(function(g){
      g.forEach(function(w){ APART[w.toLowerCase()] = '=' + g[0].toLowerCase(); });
    });
    ((syn && syn.forms) || []).forEach(function(g){
      var canon = porter(g[0].toLowerCase());
      g.forEach(function(w){ FORM[APART[w.toLowerCase()] || porter(w.toLowerCase())] = canon; });
    });
    ((syn && syn.related) || []).forEach(function(g){
      RELATED.push(g.map(function(t){
        var toks = tokenize(t);
        return {text: t.toLowerCase(), toks: toks, st: toks.map(stem)};
      }));
    });
  }
  function plain(t){ return /^[a-z0-9]+$/.test(t); }
  /* a typed word that already appears on the site is treated as complete (matched by stem);
     anything else is treated as the start of a word still being typed */
  function setVocab(blocks){ VOCAB = {}; blocks.forEach(function(b){ b.ws.forEach(function(w){ VOCAB[w] = 1; }); }); }
  function wordMatch(w, tok, st){
    return stem(w) === st || (tok.length >= 3 && !VOCAB[tok] && w.indexOf(tok) === 0);
  }
  function variants(t){ return [t, t.replace(/-/g, ' '), t.replace(/-/g, '')]; }

  /* split a typed query into tokens: lower case, stop words dropped unless nothing else is left */
  function tokenize(query){
    var t = String(query).toLowerCase().trim().split(/\s+/).filter(Boolean);
    var kept = t.filter(function(x){ return !STOP[x]; });
    return kept.length ? kept : t;
  }
  /* the typed query plus alternatives made by swapping one related term; each alternative has a small ranking penalty */
  function alternatives(tokens){
    var st = tokens.map(stem);
    var out = [{toks: tokens, st: st, pen: 0, label: ''}], seen = {};
    seen[tokens.join(' ')] = 1;
    RELATED.forEach(function(g){
      g.forEach(function(term, gi){
        for (var i = 0; i + term.st.length <= st.length; i++){
          var ok = true;
          for (var k = 0; k < term.st.length; k++) if (st[i + k] !== term.st[k]){ ok = false; break; }
          if (!ok) continue;
          g.forEach(function(other, oi){
            if (oi === gi) return;
            var toks = tokens.slice(0, i).concat(other.toks).concat(tokens.slice(i + term.st.length));
            var key = toks.join(' ');
            if (seen[key]) return; seen[key] = 1;
            out.push({toks: toks, st: toks.map(stem), pen: 0.5, label: other.text});
          });
        }
      });
    });
    return out;
  }
  /* index one block of text: lower-case text, its words, and the stems of those words */
  function block(text){
    var low = String(text || '').toLowerCase(), ws = words(low), st = {};
    ws.forEach(function(w){ st[stem(w)] = 1; });
    return {low: low, ws: ws, st: st};
  }
  function merge(blocks){
    var low = [], ws = [], st = {};
    blocks.forEach(function(b){ low.push(b.low); ws = ws.concat(b.ws); for (var k in b.st) st[k] = 1; });
    return {low: low.join(' | '), ws: ws, st: st};
  }
  /* does one token match this block? whole-word start (typing a word prefix), same stem, or the literal text for tokens with symbols */
  function tokHit(b, tok, st){
    if (plain(tok)){
      if (b.st[st]) return true;
      if (tok.length >= 3 && !VOCAB[tok]){ for (var i = 0; i < b.ws.length; i++) if (b.ws[i].indexOf(tok) === 0) return true; }
      return false;
    }
    var vs = variants(tok);
    for (var j = 0; j < vs.length; j++) if (b.low.indexOf(vs[j]) !== -1) return true;
    return false;
  }
  function hasAll(b, alt){
    for (var i = 0; i < alt.toks.length; i++) if (!tokHit(b, alt.toks[i], alt.st[i])) return false;
    return true;
  }
  /* highlight: whole words that start with, or share a stem with, a token */
  function wordHit(w, alt){
    var lw = w.toLowerCase();
    for (var i = 0; i < alt.toks.length; i++){
      var t = alt.toks[i];
      if (plain(t)){ if (wordMatch(lw, t, alt.st[i])) return true; }
      else if (t.split(/[^a-z0-9]+/).some(function(p){ return p.length >= 3 && p === lw; })) return true;
    }
    return false;
  }
  /* first position in a lower-case string where the alternative matches, or -1 */
  function findPos(low, alt){
    var best = -1;
    for (var i = 0; i < alt.toks.length; i++){
      var t = alt.toks[i], at = -1;
      if (plain(t)){
        var re = /[a-z0-9]+/g, m;
        while ((m = re.exec(low))){ if (wordMatch(m[0], t, alt.st[i])){ at = m.index; break; } }
      } else {
        var vs = variants(t);
        for (var j = 0; j < vs.length; j++){ var k = low.indexOf(vs[j]); if (k !== -1 && (at === -1 || k < at)) at = k; }
      }
      if (at !== -1 && (best === -1 || at < best)) best = at;
    }
    return best;
  }
  return {init: init, setVocab: setVocab, stem: stem, tokenize: tokenize, alternatives: alternatives, block: block, merge: merge,
          tokHit: tokHit, hasAll: hasAll, wordHit: wordHit, findPos: findPos, words: words};
})();
if (typeof module !== 'undefined') module.exports = Search;
