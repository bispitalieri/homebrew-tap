cask "biolaris-media" do
  on_macos do
    arch arm: "aarch64", intel: "x86_64"

    version "0.1.2"
    sha256 arm:   "821fbae6402b5137367688e9c6972adeee67ba2bc2ff6fcba03954844321682d",
           intel: "bb137e0bd3a695eef12d9a2de727ab9c43ed8106ad692b526815c8e3d4b4f090"

    url "https://github.com/bispitalieri/biolaris-media/releases/download/v#{version}/Biolaris-Media_#{version}_darwin-#{arch}.dmg"
    name "Biolaris Media"
    desc "Desktop media conversion and compression tools"
    homepage "https://github.com/bispitalieri/biolaris-media"

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
    version "0.1.2"
    sha256 "ac64103b592caa70fc596109c945a8fa505657dac19235da2f7295d9753ddf9f"

    url "https://github.com/bispitalieri/biolaris-media/releases/download/v#{version}/Biolaris-Media_#{version}_linux-x86_64.AppImage"
    name "Biolaris Media"
    desc "Desktop media conversion and compression tools"
    homepage "https://github.com/bispitalieri/biolaris-media"

    depends_on arch: :x86_64

    app_image "Biolaris-Media_#{version}_linux-x86_64.AppImage", target: "Biolaris-Media.AppImage"
  end
end
