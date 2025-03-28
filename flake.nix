{
  description = "Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
      };
    in {
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [
          (
            python3.withPackages (python-pkgs:
              with python-pkgs; [
                ruff
                flask-cors
                flask
                pytest
              ])
          )
        ];

        shellHook = ''
          # Create bin directory for scripts
          mkdir -p ./.direnv/bin

          # Create run-server script
          cat > ./.direnv/bin/run-server <<'EOF'
          #!/usr/bin/env bash
          FLASK_APP=inventory.py FLASK_ENV=development python inventory.py
          EOF

          # Create test script
          cat > ./.direnv/bin/test <<'EOF'
          #!/usr/bin/env bash
          python -m pytest test_inventory.py -v
          EOF

          # Make scripts executable
          chmod +x ./.direnv/bin/run-server
          chmod +x ./.direnv/bin/test

          # Add scripts to PATH
          export PATH="$(pwd)/.direnv/bin:$PATH"

          echo "Python development environment activated!"
          echo "Commands available:"
          echo "  run-server - Start the Flask application"
          echo "  test       - Run the test suite"
        '';
      };
    });
}
