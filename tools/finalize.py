#!/usr/bin/env python3
"""Fill the README templates and the Thunderstore manifest with the real links.

    python tools/finalize.py --user <github_user> [--repo PeakWorkshop] [--branch main] [--team PeakCode]
                             [--yt-trailer ID|URL] [--yt-t1 ID|URL] ... [--yt-t4 ID|URL]
                             [--yt-channel https://www.youtube.com/@PeakWorkshop]
                             [--discord <link to the Peak Workshop thread>] [--live]

Tutorial numbers are the RELEASE numbers: --yt-t1 3D assets, --yt-t2 items, --yt-t3 NPCs, --yt-t4 map.

--team is the Thunderstore team (ASCII letters, digits, underscore). --live adds the Thunderstore
downloads badge - use it only once the package is published and indexed, before that it shows as broken.

Writes:
    README.md                    (from README.template.md, GitHub flavour)
    thunderstore/README.md       (from thunderstore/README.template.md)
    thunderstore/manifest.json   (from thunderstore/manifest.template.json, website_url filled)

Videos without an id: the trailer thumbnail links to the GitHub release page instead.
All four tutorials are always listed (card + title, in release order). One without its own id links to
--yt-channel (channel or playlist), or to the GitHub release page if that is missing too.
--discord is the link to the Peak Workshop thread on the PEAK Modding Discord (feedback, bug reports, help).
Without it the READMEs name "PEAK Modding Discord (Peak Workshop thread)" as plain text, no link.
Only writes local files - never uploads anything. Safe to run again.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Release numbering: key t<n> = --yt-t<n> = card tutorial_<n>_*.jpg
TUTORIALS = [
    ("t1", "#1 Import 3D Assets", "GLB, OBJ, FBX or a ZIP - fix scale and textures, credit it, place it.", "tutorial_1_import_3d_assets_play.jpg"),
    ("t2", "#2 Create Custom Items", "Turn a 3D model into a flare gun with recoil, knockback and loot spawns.", "tutorial_2_custom_items_play.jpg"),
    ("t3", "#3 Create NPCs", "Talking characters, quests that change the world, and a boss fight.", "tutorial_3_npcs_play.jpg"),
    ("t4", "#4 Build a Map from the Bare Preset", "From the Bare preset to a playable map - terrain, scatter areas, platforms, spawns, "
           "and the asset, item and NPC from #1-#3 put together.", "tutorial_4_build_a_map_play.jpg"),
]
DISCORD_TEXT = "PEAK Modding Discord (Peak Workshop thread)"


def yt_id(value):
    """Accept a bare id or any YouTube URL; return the 11-char id or None."""
    if not value:
        return None
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", value)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value
    sys.exit(f"Not a YouTube id or URL: {value!r}")


def yt_url(vid):
    return f"https://www.youtube.com/watch?v={vid}"


def trailer_block(base, release, vid, html):
    thumb = f"{base}/media/video_thumbs/trailer_play.jpg"
    if vid:
        link, label = yt_url(vid), "Watch the trailer on YouTube"
    else:
        link, label = release, "Watch the trailer (download)"
    if html:
        return (f'<p align="center">\n  <a href="{link}"><img src="{thumb}" alt="{label}" width="80%"></a>\n'
                f'  <br><b><a href="{link}">▶ {label}</a></b>\n</p>')
    return f"### [▶ {label}]({link})\n\n[![{label}]({thumb})]({link})"


def tutorials_block(base, ids, fallback, html):
    """All four tutorials, always, in release order. fallback = channel/playlist URL or the release page."""
    rows = [(thumb, title, blurb, yt_url(ids[key]) if ids.get(key) else fallback) for key, title, blurb, thumb in TUTORIALS]
    head = ("### " if html else "## ") + "Video tutorials\n\nNew to building? These step-by-step videos take you from your first imported 3D model to a finished map.\n\n"
    if html:
        cells = []
        for key, title, blurb, url in rows:
            cells.append(f'    <td width="50%" valign="top"><a href="{url}"><img src="{base}/media/video_thumbs/{key}" '
                         f'alt="Tutorial {title}"></a><br><b><a href="{url}">{title}</a></b><br><sub>{blurb}</sub></td>')
        trs = ["  <tr>\n" + "\n".join(cells[i:i + 2]) + "\n  </tr>" for i in range(0, len(cells), 2)]
        return head + "<table>\n" + "\n".join(trs) + "\n</table>"
    # Thunderstore: plain Markdown table, two per row (image row + caption row)
    out = [head + "| | |", "|---|---|"]
    for i in range(0, len(rows), 2):
        pair = rows[i:i + 2]
        imgs = [f"[![Tutorial {t}]({base}/media/video_thumbs/{k})]({u})" for k, t, b, u in pair]
        caps = [f"**[{t}]({u})** - {b}" for k, t, b, u in pair]
        if len(pair) == 1:
            imgs.append(" ")
            caps.append(" ")
        out.append("| " + " | ".join(imgs) + " |")
        out.append("| " + " | ".join(caps) + " |")
    return "\n".join(out)


def validate_manifest(m):
    """Thunderstore package rules (same checks as the upload form)."""
    errs = []
    if not re.fullmatch(r"[a-zA-Z0-9_]+", m.get("name", "")):
        errs.append("name must match ^[a-zA-Z0-9_]+$")
    if not re.fullmatch(r"\d+\.\d+\.\d+", m.get("version_number", "")):
        errs.append("version_number must be Major.Minor.Patch")
    if len(m.get("description", "")) > 250:
        errs.append("description is longer than 250 characters")
    if not re.fullmatch(r"https?://\S+", m.get("website_url", "")):
        errs.append("website_url must be a URL (or empty)")
    for d in m.get("dependencies", []):
        if not re.fullmatch(r"[A-Za-z0-9_]+-[A-Za-z0-9_]+-\d+\.\d+\.\d+", d):
            errs.append(f"bad dependency string: {d}")
    if errs:
        sys.exit("manifest.json invalid: " + "; ".join(errs))


def fill(text, values):
    for k, v in values.items():
        text = text.replace("{" + k + "}", v)
    text = re.sub(r"\n{3,}", "\n\n", text)
    left = sorted(set(re.findall(r"\{[A-Z_0-9]+\}", text)))
    if left:
        sys.exit(f"Unfilled placeholders: {', '.join(left)}")
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--user", required=True, help="GitHub user or organisation")
    ap.add_argument("--repo", default="PeakWorkshop")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--yt-trailer")
    for n in range(1, 5):
        ap.add_argument(f"--yt-t{n}")
    ap.add_argument("--yt-channel", help="YouTube channel or playlist URL - link for tutorials without their own id")
    ap.add_argument("--discord", help="link to the Peak Workshop thread on the PEAK Modding Discord (optional)")
    ap.add_argument("--team", default="PeakCode", help="Thunderstore team name (default PeakCode)")
    ap.add_argument("--live", action="store_true", help="package is live on Thunderstore: add the downloads badge")
    a = ap.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_]+", a.team):
        sys.exit("--team must match ^[A-Za-z0-9_]+$ (Thunderstore rule)")

    manifest_tpl = json.loads((ROOT / "thunderstore/manifest.template.json").read_text(encoding="utf-8"))
    version = manifest_tpl["version_number"]
    base = f"https://raw.githubusercontent.com/{a.user}/{a.repo}/{a.branch}"
    repo_url = f"https://github.com/{a.user}/{a.repo}"
    release = f"{repo_url}/releases/latest"
    trailer = yt_id(a.yt_trailer)
    tut = {f"t{n}": yt_id(getattr(a, f"yt_t{n}")) for n in range(1, 5)}

    common = {"GITHUB_USER": a.user, "REPO": a.repo, "RELEASE": release, "VERSION": version,
              "TEAM": a.team, "TEAM_BADGE": a.team.replace("_", "__")}
    common["DOWNLOADS_BADGE"] = (f'<a href="https://thunderstore.io/c/peak/p/{a.team}/PeakWorkshop/"><img alt="Downloads" '
                                 f'src="https://img.shields.io/thunderstore/dt/{a.team}/PeakWorkshop?style=for-the-badge&color=1B2340"></a>'
                                 if a.live else "")
    for name, url in (("--discord", a.discord), ("--yt-channel", a.yt_channel)):
        if url and not re.fullmatch(r"https?://\S+", url):
            sys.exit(f"{name} must be a URL: {url!r}")
    tut_fallback = a.yt_channel or release
    if a.discord:
        discord = f"[{DISCORD_TEXT}]({a.discord})"
        discord_badge = (f'<a href="{a.discord}"><img alt="Discord - Peak Workshop thread" '
                         f'src="https://img.shields.io/badge/Discord-Peak_Workshop_thread-5865F2'
                         f'?style=for-the-badge&logo=discord&logoColor=white"></a>')
    else:
        discord, discord_badge = DISCORD_TEXT, ""

    for tpl, out, html in [("README.template.md", "README.md", True),
                           ("thunderstore/README.template.md", "thunderstore/README.md", False)]:
        text = (ROOT / tpl).read_text(encoding="utf-8")
        values = dict(common,
                      TRAILER=trailer_block(base, release, trailer, html),
                      TUTORIALS=tutorials_block(base, tut, tut_fallback, html),
                      DISCORD=discord, DISCORD_BADGE=discord_badge)
        # BASE last-but-not-least: the generated blocks above contain it already resolved
        values["BASE"] = base
        (ROOT / out).write_text(fill(text, values), encoding="utf-8", newline="\n")
        print(f"wrote {out}")

    manifest_tpl["website_url"] = repo_url
    validate_manifest(manifest_tpl)
    (ROOT / "thunderstore/manifest.json").write_text(json.dumps(manifest_tpl, indent=2, ensure_ascii=False) + "\n",
                                                    encoding="utf-8", newline="\n")
    print("wrote thunderstore/manifest.json")
    if not trailer:
        print("note: no YouTube id for the trailer - its thumbnail links to the release page")
    missing = [k for k, v in tut.items() if not v]
    if missing:
        print("note: no YouTube id for " + ", ".join(missing) + " - linked to "
              + ("the channel/playlist" if a.yt_channel else "the release page (no --yt-channel)"))
    if not a.discord:
        print(f"note: no --discord - the READMEs name the {DISCORD_TEXT} as plain text, without a link")


if __name__ == "__main__":
    main()
