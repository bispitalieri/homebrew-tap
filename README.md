# Biolaris Media Homebrew tap

Install Biolaris Media with Homebrew:

```sh
brew tap bispitalieri/homebrew-tap
```

On macOS, install the official Apple silicon or Intel app:

```sh
brew install --cask biolaris-media
```

On Linux x86_64, install the official AppImage:

```sh
brew install --cask biolaris-media
```

Both use artifacts from
[Biolaris Media GitHub Releases](https://github.com/bispitalieri/biolaris-media/releases).

## Uninstall

Homebrew removes the installed application and managed files when uninstalling.
On macOS, `brew uninstall --cask biolaris-media` quits the app first. To also
remove its app-specific support data, caches, preferences, saved window state,
WebKit data, and launch-agent plist, run:

```sh
brew zap --cask biolaris-media
```

On Linux, `brew uninstall --cask biolaris-media` removes the AppImage and its
Homebrew-managed desktop integration. User data outside the Homebrew prefix is
left untouched.

## Automatic updates

The `Update Biolaris Media cask` GitHub Actions workflow checks the latest stable
release every six hours and can also be started manually. When a newer version
is available, it verifies the release's architecture-specific DMGs and Linux
AppImage SHA-256 checksums, updates `Casks/biolaris-media.rb`, and commits the
change.

The updater reads the public upstream release API, so no cross-repository
credentials are required. The tap repository's Actions workflow needs its
standard `contents: write` permission to commit the updated cask.
