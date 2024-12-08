{ pkgs, ... }: {
  # nixpkgs channel
  channel = "stable-23.11";

  packages = [
    pkgs.python3
    pkgs.jdk20
    pkgs.android-studio
    pkgs.android-sdk
    pkgs.flutter
  ];

  # environment variables
  env = {
    VENV_DIR = ".venv";
    MAIN_FILE = "main.py";
    ANDROID_HOME = "${pkgs.android-sdk}";
    JAVA_HOME = "${pkgs.jdk20}";
    PATH = "${pkgs.android-sdk}/bin:${pkgs.android-sdk}/tools:${pkgs.android-sdk}/platform-tools:${JAVA_HOME}/bin:$PATH";
  };

  idx = {
    extensions = [
      "ms-python.python"
      "ms-python.debugpy"
      "dart-code.flutter"
    ];

    workspace = {
      onCreate = {
        create-venv = ''
          python -m venv $VENV_DIR

          if [ ! -f requirements.txt ]; then
            echo "requirements.txt not found. Creating one with flet..."
            echo "flet" > requirements.txt
          fi

          source $VENV_DIR/bin/activate
          pip install -r requirements.txt

          echo "Setting up Android SDK..."
          "${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager" "platform-tools" "platforms;android-33" "build-tools;33.0.0"
          yes | "${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager" --licenses

          echo "Configuring Flutter..."
          flutter config --android-sdk=$ANDROID_HOME
          flutter doctor
        '';

        default.openFiles = [ "README.md" "requirements.txt" "$MAIN_FILE" ];
      };

      onStart = {
        check-venv-existence = ''
          if [ ! -d $VENV_DIR ]; then
            echo "Virtual environment not found. Creating one..."
            python -m venv $VENV_DIR
          fi

          if [ ! -f requirements.txt ]; then
            echo "requirements.txt not found. Creating one with flet..."
            echo "flet" > requirements.txt
          fi

          source $VENV_DIR/bin/activate
          pip install -r requirements.txt

          echo "Verifying Android SDK setup..."
          "${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager" --licenses || true
          flutter doctor || true
        '';
      };
    };

    previews = {
      enable = true;
      previews = {
        web = {
          command = [
            "bash"
            "-c"
            ''
            source $VENV_DIR/bin/activate
            flet run $MAIN_FILE --web --port $PORT
            ''
          ];
          env = { PORT = "$PORT"; };
          manager = "web";
        };
      };
    };
  };
}
