#!/usr/bin/env python3

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPOSITORY = "bispitalieri/biolaris-media"
RELEASE_API = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"
TAP_ROOT = Path(__file__).resolve().parents[1]
CASK_PATH = TAP_ROOT / "Casks" / "biolaris-media.rb"
USER_AGENT = "biolaris-media-homebrew-tap"


def fetch_json(url):
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def asset_checksum(asset, expected_name):
    if asset.get("name") != expected_name:
        raise ValueError(f"Unexpected release asset name: {asset.get('name')!r}")

    digest = asset.get("digest")
    if digest:
        algorithm, separator, value = digest.partition(":")
        if separator and algorithm == "sha256" and re.fullmatch(r"[0-9a-f]{64}", value):
            return value

    request = Request(
        asset["browser_download_url"],
        headers={"User-Agent": USER_AGENT},
    )
    checksum = hashlib.sha256()
    with urlopen(request, timeout=120) as response:
        while chunk := response.read(1024 * 1024):
            checksum.update(chunk)
    return checksum.hexdigest()


def render_cask(version, checksums):
    return f'''cask "biolaris-media" do
  on_macos do
    arch arm: "aarch64", intel: "x86_64"

    version "{version}"
    sha256 arm:   "{checksums["arm"]}",
           intel: "{checksums["intel"]}"

    url "https://github.com/{REPOSITORY}/releases/download/v#{{version}}/Biolaris-Media_#{{version}}_darwin-#{{arch}}.dmg"
    name "Biolaris Media"
    desc "Desktop media conversion and compression tools"
    homepage "https://github.com/{REPOSITORY}"

    livecheck do
      url :url
      strategy :github_latest
    end

    auto_updates true

    app "Biolaris Media.app"

    uninstall_postflight_steps do
      run "/usr/bin/pkill",
          args:         ["-f", "Biolaris Media.app"],
          must_succeed: false
    end

    uninstall quit:   "dev.biolaris-media.app",
              delete: "~/Library/LaunchAgents/dev.biolaris-media.app.plist"

    zap trash: [
      "~/Library/Application Support/dev.biolaris-media.app",
      "~/Library/Caches/dev.biolaris-media.app",
      "~/Library/Preferences/dev.biolaris-media.app.plist",
      "~/Library/Saved Application State/dev.biolaris-media.app.savedState",
      "~/Library/WebKit/dev.biolaris-media.app",
    ]
  end
  on_linux do
    version "{version}"
    sha256 "{checksums["linux"]}"

    url "https://github.com/{REPOSITORY}/releases/download/v#{{version}}/Biolaris-Media_#{{version}}_linux-x86_64.AppImage"
    name "Biolaris Media"
    desc "Desktop media conversion and compression tools"
    homepage "https://github.com/{REPOSITORY}"

    depends_on arch: :x86_64

    app_image "Biolaris-Media_#{{version}}_linux-x86_64.AppImage", target: "Biolaris-Media.AppImage"
  end
end
'''


def main():
    release = fetch_json(RELEASE_API)
    if release.get("draft") or release.get("prerelease"):
        raise ValueError("The latest upstream release is not a stable published release")

    tag = release.get("tag_name", "")
    match = re.fullmatch(r"v?(\d+\.\d+\.\d+)", tag)
    if not match:
        raise ValueError(f"Unsupported upstream release tag: {tag!r}")
    version = match.group(1)

    existing_cask = CASK_PATH.read_text()
    existing_match = re.search(r'^\s*version "(\d+\.\d+\.\d+)"$', existing_cask, re.MULTILINE)
    if not existing_match:
        raise ValueError(f"Could not read the current cask version from {CASK_PATH}")

    current_version = tuple(map(int, existing_match.group(1).split(".")))
    upstream_version = tuple(map(int, version.split(".")))
    if upstream_version <= current_version:
        print(f"Cask is current ({existing_match.group(1)}); upstream release is {version}.")
        return

    assets = {asset["name"]: asset for asset in release.get("assets", [])}
    checksums = {}
    for architecture, suffix in (
        ("arm", "darwin-aarch64"),
        ("intel", "darwin-x86_64"),
        ("linux", "linux-x86_64"),
    ):
        extension = "AppImage" if architecture == "linux" else "dmg"
        asset_name = f"Biolaris-Media_{version}_{suffix}.{extension}"
        asset = assets.get(asset_name)
        if asset is None:
            raise ValueError(f"Release {tag} is missing required asset {asset_name}")
        checksums[architecture] = asset_checksum(asset, asset_name)

    CASK_PATH.write_text(render_cask(version, checksums))
    print(f"Updated cask from {existing_match.group(1)} to {version}.")


if __name__ == "__main__":
    try:
        main()
    except (HTTPError, URLError, TimeoutError, KeyError, ValueError) as error:
        print(f"Unable to update Biolaris Media cask: {error}", file=sys.stderr)
        raise SystemExit(1) from error
