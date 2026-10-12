#!/usr/bin/env python3
"""Render README.md from MANUSCRIPT_STATUS.yaml (manuscript-tracking readme_template 1.3).

Usage:  python3 hyman2026local_render_readme.py [--yaml MANUSCRIPT_STATUS.yaml] [--out README.md] [--check]
  --check   render to memory and diff against the README on disk; exit 1 on any difference.

The README is a rendered artifact: edit the YAML and re-run this script, never the README.
Requires Python 3 and PyYAML. Deterministic: the same YAML always gives the same bytes.
"""
import argparse, difflib, sys
import yaml

DASH = "—"
YES, NO = "✅", "❌"


def v(x):
    """Null rendering for table cells."""
    return DASH if x is None or x == "" else str(x)


def render(d):
    m, tv, dist, sub = d["manuscript"], d["target_venue"], d["distribution"], d["submission"]
    assets, meta = d.get("assets") or {}, d["metadata"]
    L = []
    a = L.append
    a(f"# {m['title']}")
    a("")
    if m.get("subtitle"):
        a(m["subtitle"])
        a("")
    ver = f"**Manuscript ID:** `{m['short_id']}` · **Current version:** {m['current_version']} ({m['current_pages']} pp)"
    if m.get("si_file"):
        ver += f" + SI {m['current_si_version']} ({m['current_si_pages']} pp)"
    a(ver)
    a(f"**Last updated:** {meta['last_updated']} · **MREP score:** {v(m.get('mrep_score'))}/100")
    a("")
    a("---")
    a("")
    a("## Authors")
    a("")
    if tv.get("authors_anonymized"):
        a("Authors anonymized for double-blind review")
    else:
        for au in m["authors"]:
            line = f"- **{au['name']}**, {au['affiliation']} · `{au['email']}` · ORCID: {au['orcid']}"
            if au.get("is_corresponding"):
                line += " · *corresponding author*"
            a(line)
    a("")
    a("---")
    a("")
    a("## Target Journal")
    a("")
    a(f"**{tv['journal']}** ({v(tv.get('publisher'))})")
    a("")
    a("| Field | Value |")
    a("|---|---|")
    a(f"| Submission system | {v(tv.get('submission_system'))} |")
    a(f"| URL | {v(tv.get('url'))} |")
    a(f"| Blinding | {v(tv.get('blinding'))} |")
    a(f"| Page limit | {tv.get('page_limit') or 'none'} |")
    a(f"| Format class | `{tv.get('format_class')}` |")
    a("")
    a("**Format requirements:**")
    for it in tv.get("format_requirements") or []:
        a(f"- {it}")
    a("")
    a("**Required documents at submission:**")
    for it in tv.get("required_documents") or []:
        a(f"- {it}")
    a("")
    if tv.get("backup_journals"):
        a("**Backup journals (in priority order):**")
        for i, j in enumerate(tv["backup_journals"], 1):
            a(f"{i}. {j}")
        a("")
    a("---")
    a("")
    a("## Submission Status")
    a("")
    a(f"**Current status: `{sub['status']}`**")
    a("")
    a("| Field | Value |")
    a("|---|---|")
    a(f"| Prepared date | {v(sub.get('prepared_date'))} |")
    a(f"| Submitted date | {v(sub.get('submitted_date'))} |")
    a(f"| Manuscript ID (journal) | {v(sub.get('manuscript_id'))} |")
    a(f"| Current round | {v(sub.get('current_round'))} |")
    a(f"| Editor assigned | {v(sub.get('editor_assigned'))} |")
    a(f"| Decision expected by | {v(sub.get('decision_expected_by'))} |")
    a("")
    if sub.get("notes"):
        a(f"> {sub['notes']}")
        a("")
    a("---")
    a("")
    a("## Distribution Channels")
    a("")
    ax, gh, zn = dist["arxiv"], dist["github"], dist["zenodo"]
    a("### arXiv")
    a("")
    a("| Field | Value |")
    a("|---|---|")
    a(f"| Posted? | {YES + ' Yes' if ax.get('posted') is True else ('pending' if ax.get('posted') == 'pending' else NO + ' Not yet')} |")
    a(f"| Identifier | {v(ax.get('identifier'))} |")
    a(f"| URL | {v(ax.get('url'))} |")
    a(f"| Posted date | {v(ax.get('posted_date'))} |")
    a(f"| Primary category | {v(ax.get('primary_category'))} |")
    a(f"| Cross-list | {', '.join(ax.get('cross_list') or []) or DASH} |")
    a(f"| Package built? | {YES if ax.get('package_built') else NO} |")
    a(f"| Package path | `{v(ax.get('package_path'))}` |")
    a("")
    a("### GitHub")
    a("")
    a("| Field | Value |")
    a("|---|---|")
    a(f"| Repository created? | {YES + ' Yes' if gh.get('created') else NO + ' Not yet'} |")
    a(f"| URL | {v(gh.get('url'))} |")
    a(f"| Visibility | {v(gh.get('visibility'))} |")
    a(f"| Canonical YAML URL | {v(gh.get('canonical_yaml_url'))} |")
    a(f"| Package built? | {YES if gh.get('package_built') else NO} |")
    a(f"| Package path | `{v(gh.get('package_path'))}` |")
    a("")
    a("### Zenodo")
    a("")
    a("| Field | Value |")
    a("|---|---|")
    a(f"| DOI minted? | {YES if zn.get('minted') else NO} |")
    a(f"| DOI | {v(zn.get('doi'))} |")
    a(f"| URL | {v(zn.get('url'))} |")
    a("")
    a("---")
    a("")
    if d.get("referee_history"):
        a("## Referee History")
        a("")
        for rd in d["referee_history"]:
            a(f"### Round {rd['round']}")
            a("")
            a("| Field | Value |")
            a("|---|---|")
            a(f"| Reports received | {v(rd.get('reports_received_date'))} |")
            a(f"| Decision | `{v(rd.get('decision'))}` |")
            a(f"| Reports file | `{v(rd.get('reports_file'))}` |")
            a(f"| Response letter | `{v(rd.get('response_letter'))}` |")
            a(f"| Revised version | {v(rd.get('revised_version_packaged'))} |")
            a(f"| Resubmitted date | {v(rd.get('resubmitted_date'))} |")
            a("")
            a(f"**Reports summary:** {v(rd.get('reports_summary'))}")
            a("")
        a("---")
        a("")
    cs, bib = m["compile_state"], m["bibliography"]
    a("## Compile State (latest)")
    a("")
    a("| Metric | Value |")
    a("|---|---:|")
    a(f"| Main paper pages | {m['current_pages']} |")
    a(f"| SI pages | {m.get('current_si_pages') or 'n/a'} |")
    a(f"| Errors | {cs['errors']} |")
    a(f"| Undefined references | {cs['undef_refs']} |")
    a(f"| Overfull hboxes | {cs['overfull_hboxes']} |")
    a(f"| Last compiled | {m['last_compiled']} |")
    a("")
    a(f"**Bibliography:** `{bib['bib_file']}` ({bib['entries']} entries, `{bib['style']}` style)")
    a("")
    a("---")
    a("")
    if assets:
        s = assets["summary"]
        status = {"pass": YES + " PASS", "fail": NO + " FAIL"}.get(s.get("integrity_status"), DASH + " never run")
        a("## Reproducibility")
        a("")
        a(f"**Integrity check:** {status} (last run {v(s.get('last_integrity_check'))})")
        a("")
        a("| Registered | Count |")
        a("|---|---:|")
        a(f"| Figures | {s['figures_total']} |")
        a(f"| Tables | {s['tables_total']} |")
        a(f"| Deposited (code + data present, hashed) | {s['deposited']} |")
        a(f"| Awaited (not yet provided) | {s['awaited']} |")
        a(f"| External (hosted elsewhere) | {s['external']} |")
        a(f"| Unhashed (registered, hash pending) | {s['unhashed']} |")
        a("")
        items = assets.get("items") or []
        def unhashed(it):
            hs = [it["generator"].get("sha256")] + [x.get("sha256") for x in it.get("inputs") or []] \
                 + [x.get("sha256") for x in it.get("outputs") or []]
            return any(h is None for h in hs)
        gaps = [it for it in items if it["status"] == "awaited" or (it["status"] == "deposited" and unhashed(it))]
        if s.get("awaited", 0) > 0 or s.get("unhashed", 0) > 0 or s.get("integrity_status") == "fail" or gaps:
            a("**⚠️ Reproducibility gaps — these block submission and block CGR/COR packaging:**")
            for it in gaps:
                own = f", owed by {it['owner']}" if it.get("owner") not in (None, "self") else ""
                a(f"- `{it['id']}` ({it['kind']}, `{it['label']}`) — {it['status']}{own}: {it.get('provenance_note') or 'generator/data not yet registered'}")
        else:
            a("*All figures and tables have deposited or externally-archived generators with verified hashes. Repository is reproducible.*")
        a("")
        a("**Asset map:**")
        a("")
        a("| ID | Kind | Status | Generator | Output | Verified |")
        a("|---|---|---|---|---|---|")
        for it in items:
            out = (it.get("outputs") or [{}])[0].get("path")
            a(f"| `{it['id']}` | {it['kind']} | {it['status']} | `{v(it['generator'].get('path'))}` | `{v(out)}` | {v(it.get('last_verified'))} |")
        a("")
        a("---")
        a("")
    if d.get("companion_papers"):
        a("## Companion Papers")
        a("")
        for c in d["companion_papers"]:
            a(f"### `{c['short_id']}` — {c['title']}")
            a("")
            a("| Field | Value |")
            a("|---|---|")
            a(f"| Target venue | {v(c.get('target_venue'))} |")
            a(f"| Status | `{v(c.get('status'))}` |")
            a(f"| Relationship | {v(c.get('relationship'))} |")
            a(f"| YAML available | {YES if c.get('yaml_available') else NO} |")
            warn = "" if c.get("confirmed") else " ⚠️ memory-derived, unconfirmed"
            a(f"| Last confirmed | {v(c.get('last_confirmed'))}{warn} |")
            a("")
            if c.get("coordination_notes"):
                a(f"> {c['coordination_notes']}")
                a("")
        a("---")
        a("")
    a("## File Manifest (Current Working Set)")
    a("")
    a("This package contains:")
    a(f"- `{m['main_file']}` — main manuscript source")
    a(f"- `{bib['bib_file']}` — bibliography")
    if m.get("si_file"):
        a(f"- `{m['si_file']}` — Supplementary Information")
    for path, desc in (meta.get("readme_extra_files") or {}).items():
        a(f"- `{path}` — {desc}")
    a("- `MANUSCRIPT_STATUS.yaml` — structured status + asset registry (this README's source of truth)")
    a("- `CHANGELOG.md` — chronological change record")
    a("- `README.md` — this file (rendered from YAML; do not edit directly)")
    a("")
    a("Every file that backs a manuscript figure or table is registered in `assets:` and is protected from deletion during branch cleanup.")
    a("")
    a("---")
    a("")
    stem = m["main_file"][:-4] if m["main_file"].endswith(".tex") else m["main_file"]
    a("## Compilation")
    a("")
    a("### Main paper")
    a("")
    a("```")
    a(f"pdflatex {m['main_file']}")
    a(f"bibtex {stem}")
    a(f"pdflatex {m['main_file']}")
    a(f"pdflatex {m['main_file']}")
    a("```")
    a("")
    if m.get("si_file"):
        sstem = m["si_file"][:-4]
        a("### Supplementary Information")
        a("```")
        for c in (f"pdflatex {m['si_file']}", f"bibtex {sstem}", f"pdflatex {m['si_file']}", f"pdflatex {m['si_file']}"):
            a(c)
        a("```")
        a("")
    a("---")
    a("")
    a("*This README is rendered from `MANUSCRIPT_STATUS.yaml`. To update, edit the YAML and re-render via the manuscript-tracking skill. Do not edit this README directly.*")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--yaml", default="MANUSCRIPT_STATUS.yaml")
    ap.add_argument("--out", default="README.md")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    text = render(yaml.safe_load(open(a.yaml, encoding="utf-8")))
    if a.check:
        old = open(a.out, encoding="utf-8").read()
        diff = list(difflib.unified_diff(old.splitlines(), text.splitlines(), "README.md (disk)", "README.md (rendered)", lineterm=""))
        print("\n".join(diff) if diff else "README matches the YAML render.")
        sys.exit(1 if diff else 0)
    open(a.out, "w", encoding="utf-8").write(text)
    print(f"rendered {a.out} from {a.yaml}")


if __name__ == "__main__":
    main()
