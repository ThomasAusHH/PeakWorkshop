"""Packs the Nexus Mods upload for Peak Workshop and writes the Nexus texts. Only packages - never uploads.

Output (dist/ and nexus/):
  dist/PeakWorkshop-<version>-nexus.zip   extract-into-game-folder layout (what Nexus/Vortex expect for BepInEx mods):
                                           BepInEx/plugins/PeakWorkshop/PeakWorkshop.dll (+ README, CHANGELOG, THIRD-PARTY-NOTICES)
  nexus/description.bbcode                 mod page description (Nexus BBCode), made from thunderstore/README.md
  nexus/summary.txt                        short "brief overview" (manifest description, <= 350 characters)
  nexus/changelog-<version>.txt            this version's changes as plain lines for the Nexus changelog form
  nexus/upload-<version>.txt               what to fill in on the Nexus upload form

The DLL is the same release build as for Thunderstore (dist/PeakWorkshop.dll, built with DebugType=none).

Usage:  python tools/make_nexus.py [--dll path]
"""
import json
import os
import re
import sys
import zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
TS = os.path.join(ROOT, "thunderstore")
OUT_TEXT = os.path.join(ROOT, "nexus")
DIST = os.path.join(ROOT, "dist")
DISCORD = "https://discord.com/channels/1363179626435707082/1555303572415971388"
THUNDERSTORE = "https://thunderstore.io/c/peak/p/PeakCode/PeakWorkshop/"
BEPINEX = "https://thunderstore.io/c/peak/p/BepInEx/BepInExPack_PEAK/"

# Nexus has its own install flow - this replaces the README's "Installation" section.
NEXUS_INSTALL = f"""## Installation

**You need BepInEx for PEAK first:** [BepInExPack for PEAK]({BEPINEX}) (5.4.75301). Without it the mod does nothing.

**Manual install:**
1. Install BepInExPack for PEAK into your PEAK folder (the folder with `PEAK.exe`).
2. Extract this archive into the same PEAK folder - the DLL ends up in `PEAK/BepInEx/plugins/PeakWorkshop/PeakWorkshop.dll`.
3. Start PEAK. The **Peak Workshop** sign drops into the main menu.

**Updating:** extract the new archive over the old one. Your maps and settings stay in `PEAK/BepInEx/PeakWorkshop/` and are not touched.

**Prefer a mod manager?** Peak Workshop is also on [Thunderstore]({THUNDERSTORE}) - with r2modman or the Thunderstore Mod Manager BepInEx comes along automatically.
"""


def die(msg):
    print("ERROR:", msg)
    sys.exit(1)


# ------------------------------------------------------------------ Markdown -> Nexus BBCode
def inline(s):
    s = re.sub(r"\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)", r"[url=\3][img]\2[/img][/url]", s)   # linked image
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"[img]\2[/img]", s)                                  # image
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"[url=\2]\1[/url]", s)                                 # link
    s = re.sub(r"\*\*(.+?)\*\*", r"[b]\1[/b]", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"[i]\1[/i]", s)
    s = re.sub(r"`([^`]+)`", r"[font=Courier New]\1[/font]", s)
    return s


def table_to_bbcode(rows):
    """Nexus has no tables: a row of images followed by a row of captions becomes image, caption, image, caption ..."""
    out = []
    i = 0
    while i < len(rows):
        row = rows[i]
        nxt = rows[i + 1] if i + 1 < len(rows) else None
        has_img = any("![" in c for c in row)
        if has_img and nxt is not None and not any("![" in c for c in nxt):
            for k, cell in enumerate(row):
                if cell:
                    out.append(inline(cell))
                if k < len(nxt) and nxt[k]:
                    out.append(inline(nxt[k]))
                out.append("")
            i += 2
            continue
        for cell in row:
            if cell:
                out.append(inline(cell))
        out.append("")
        i += 1
    return out


def md_to_bbcode(md):
    out = []
    lines = md.replace("\r\n", "\n").split("\n")
    in_list = None    # "ul" | "ol"
    table = []

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("[/list]")
            in_list = None

    def close_table():
        if table:
            out.extend(table_to_bbcode(table))
            table.clear()

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("|"):
            close_list()
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-{3,}:?", c) or c == "" for c in cells):
                table.append(cells)
            continue
        close_table()
        m_ul = re.match(r"^\s*[-*] (.*)$", line)
        m_ol = re.match(r"^\s*\d+\. (.*)$", line)
        if m_ul or m_ol:
            kind = "ul" if m_ul else "ol"
            if in_list != kind:
                close_list()
                out.append("[list]" if kind == "ul" else "[list=1]")
                in_list = kind
            out.append("[*]" + inline((m_ul or m_ol).group(1)))
            continue
        close_list()
        h = re.match(r"^(#{1,6}) (.*)$", line)
        if h:
            size = {1: 6, 2: 5, 3: 4}.get(len(h.group(1)), 3)
            out.append("")
            out.append(f"[size={size}][b]{inline(h.group(2))}[/b][/size]")
            continue
        if re.fullmatch(r"-{3,}|\*{3,}", line.strip()):
            out.append("[line]")
            continue
        out.append(inline(line))
    close_table()
    close_list()
    text = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def replace_section(md, title, new):
    pat = re.compile(r"^## " + re.escape(title) + r"\s*\n.*?(?=^## |\Z)", re.S | re.M)
    if not pat.search(md):
        die(f"README has no section '## {title}'")
    return pat.sub(new.rstrip() + "\n\n", md, count=1)


# ------------------------------------------------------------------ changelog
def changelog_for(version, md):
    """This version's changes as plain text: intro paragraph, SECTION HEADINGS and "- " bullets (continuation lines joined)."""
    m = re.search(r"^## " + re.escape(version) + r"\b[^\n]*$(.*?)(?=^## |\Z)", md, re.S | re.M)
    if not m:
        die(f"CHANGELOG.md has no section for {version}")
    blocks = []    # (kind, text): para | head | item
    for raw in m.group(1).splitlines():
        s = raw.strip()
        if not s:
            if blocks and blocks[-1][0] == "para":
                blocks.append(("gap", ""))
            continue
        if s.startswith("**") and s.endswith("**") and s.count("**") == 2:
            blocks.append(("head", s.strip("*").upper()))
        elif s.startswith("- "):
            blocks.append(("item", s[2:]))
        elif blocks and blocks[-1][0] in ("item", "para"):
            blocks[-1] = (blocks[-1][0], blocks[-1][1] + " " + s)
        else:
            blocks.append(("para", s))

    def plain(t):
        t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
        return t.replace("**", "").replace("`", "")

    out = []
    for kind, t in blocks:
        if kind == "head":
            out += ["", plain(t)]
        elif kind == "item":
            out.append("- " + plain(t))
        elif kind == "para":
            out.append(plain(t))
    return "\n".join(out).strip() + "\n"


# ------------------------------------------------------------------ main
def main():
    dll = os.path.join(DIST, "PeakWorkshop.dll")
    if "--dll" in sys.argv:
        dll = sys.argv[sys.argv.index("--dll") + 1]
    if not os.path.isfile(dll):
        die(f"DLL not found: {dll} - copy the release build there first")
    manifest = json.load(open(os.path.join(TS, "manifest.json"), encoding="utf-8-sig"))
    version = manifest["version_number"]
    summary = manifest["description"]
    if len(summary) > 350:
        die("summary longer than 350 characters")

    data = open(dll, "rb").read()
    for pat in ("Peak Ripp Unity", "C:\\Users\\", ".pdb"):
        for enc in ("utf-8", "utf-16-le"):
            if pat.encode(enc) in data:
                die(f"DLL contains a local path/pdb reference ({pat!r}) - build with DebugType=none and --no-incremental")

    readme = open(os.path.join(TS, "README.md"), encoding="utf-8").read()
    changelog = open(os.path.join(TS, "CHANGELOG.md"), encoding="utf-8").read()
    notices = os.path.join(TS, "THIRD-PARTY-NOTICES.md")
    if re.search(r"\{[A-Z][A-Z_0-9]*\}", readme):
        die("README still has placeholders - run tools/finalize.py")

    os.makedirs(OUT_TEXT, exist_ok=True)
    os.makedirs(DIST, exist_ok=True)
    nexus_md = replace_section(readme, "Installation", NEXUS_INSTALL)
    bb = md_to_bbcode(nexus_md)
    open(os.path.join(OUT_TEXT, "description.bbcode"), "w", encoding="utf-8").write(bb)
    open(os.path.join(OUT_TEXT, "summary.txt"), "w", encoding="utf-8").write(summary + "\n")
    cl = changelog_for(version, changelog)
    open(os.path.join(OUT_TEXT, f"changelog-{version}.txt"), "w", encoding="utf-8").write(cl)

    zpath = os.path.join(DIST, f"PeakWorkshop-{version}-nexus.zip")
    base = "BepInEx/plugins/PeakWorkshop/"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(dll, base + "PeakWorkshop.dll")
        z.writestr(base + "README.md", nexus_md)
        z.write(os.path.join(TS, "CHANGELOG.md"), base + "CHANGELOG.md")
        z.write(notices, base + "THIRD-PARTY-NOTICES.md")

    upload = f"""Nexus Mods upload - Peak Workshop {version}
================================================

FILE
  Archive:        dist/PeakWorkshop-{version}-nexus.zip
  File name:      Peak Workshop {version}
  Version:        {version}
  Category:       Main Files  (on an update: move the old file to "Old versions")
  File description (short):
    Main file. Extract into your PEAK folder (needs BepInExPack for PEAK).
  Changelog:      paste nexus/changelog-{version}.txt  (also set the mod version to {version})

MOD PAGE (first upload / when the texts change)
  Name:           Peak Workshop
  Game:           PEAK
  Summary:        nexus/summary.txt  ({len(summary)} characters)
  Description:    nexus/description.bbcode  (BBCode editor / "Source" view, paste as is)
  Category:       Gameplay (or Overhauls)
  Author:         Gummybär
  Primary image:  media/banner.png - more images: media/screenshots/*.jpg and media/gifs/*.gif
  Requirements:   off-site "BepInExPack for PEAK" -> {BEPINEX}
  Permissions:    as you like; the archive contains Unity Companion License / MIT notices (THIRD-PARTY-NOTICES.md)
  Links:          Discord {DISCORD}
                  GitHub  https://github.com/ThomasAusHH/PeakWorkshop
                  Thunderstore {THUNDERSTORE}
"""
    open(os.path.join(OUT_TEXT, f"upload-{version}.txt"), "w", encoding="utf-8").write(upload)
    print(f"Packed: {zpath} ({os.path.getsize(zpath) / 1e6:.1f} MB)")
    print(f"Texts:  nexus/description.bbcode ({len(bb)} chars), nexus/summary.txt, nexus/changelog-{version}.txt, nexus/upload-{version}.txt")
    print("Upload it yourself on nexusmods.com (game PEAK). This script never uploads.")


if __name__ == "__main__":
    main()
