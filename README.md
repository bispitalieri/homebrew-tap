# Biolaris Media — Homebrew Tap

Install **Biolaris Media** using Homebrew on macOS and Linux.

This repository provides the official Homebrew Cask for Biolaris Media. All application packages are downloaded directly from the official [Biolaris Media GitHub Releases](https://github.com/bispitalieri/biolaris-media/releases).

## Requirements

- [Homebrew](https://brew.sh/) installed.
- macOS (Apple Silicon or Intel) or Linux (x86_64).
- Internet connection.

## Installation

### 1. Add the Biolaris tap

```sh
brew tap bispitalieri/tap
```

### 2. Trust the cask

Homebrew 6 and newer may require explicit trust before installing casks from third-party taps.

```sh
brew trust bispitalieri/tap
```

This authorizes Homebrew to load the Biolaris Media cask without granting trust to every package in the tap.

### 3. Install Biolaris Media

```sh
brew install --cask biolaris-media
```

Homebrew automatically selects the appropriate package for your platform:

| Platform | Package |
|---|---|
| macOS Apple Silicon (ARM64) | DMG |
| macOS Intel (x86_64) | DMG |
| Linux x86_64 | AppImage |

All packages are official release artifacts published in [GitHub Releases](https://github.com/bispitalieri/biolaris-media/releases).

## Updating

To update Homebrew's metadata and install the latest available version:

```sh
brew update
brew upgrade --cask biolaris-media
```

The cask is automatically maintained by a GitHub Actions workflow that:

- Checks for new stable releases every six hours.
- Supports manual execution.
- Verifies architecture-specific DMG and Linux AppImage SHA-256 checksums.
- Updates the cask version, download URLs, and checksums.
- Commits changes automatically when a newer release is available.

No manual intervention or cross-repository credentials are required by the updater. The workflow uses the public upstream GitHub Releases API and the tap repository's standard `contents: write` permission.

## Uninstallation

To uninstall Biolaris Media:

```sh
brew uninstall --cask biolaris-media
```

### macOS: Remove application data

To additionally remove Biolaris Media's application-specific support data, caches, preferences, saved window state, WebKit data, and launch-agent plist, run:

```sh
brew zap --cask biolaris-media
```

**Note:** `zap` removes additional application data that would normally be preserved during a regular uninstall.

### Linux

On Linux, uninstalling the cask removes the AppImage and its Homebrew-managed desktop integration.

User data stored outside the Homebrew prefix is left untouched.

## Troubleshooting

### Untrusted tap error

If Homebrew reports:

```text
Error: Refusing to load cask bispitalieri/tap/biolaris-media from untrusted tap
```

Run:

```sh
brew trust --cask bispitalieri/tap/biolaris-media
```

Then retry the installation:

```sh
brew install --cask biolaris-media
```

### Check the installed version

```sh
brew list --cask --versions biolaris-media
```

### Refresh the tap

If the cask does not show the latest version:

```sh
brew update
brew upgrade --cask biolaris-media
```

## Issues and Support

For application bugs, feature requests, or general Biolaris Media support, please use the main repository:

- [Biolaris Media — Issues](https://github.com/bispitalieri/biolaris-media/issues)

For Homebrew-specific problems, such as incorrect checksums, installation failures, or cask configuration issues, please open an issue in this repository:

- [Homebrew Tap — Issues](https://github.com/bispitalieri/homebrew-tap/issues)

## License

Biolaris Media is distributed under the [AGPL-3.0-only license](https://github.com/bispitalieri/biolaris-media/blob/main/LICENSE).