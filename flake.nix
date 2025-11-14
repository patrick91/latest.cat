{
  description = "latest.cat development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            nodejs_22
            pnpm

            python314
            uv
          ];

          shellHook = ''
            echo "latest.cat development environment"
            echo "Node.js version: $(node --version)"
            echo "pnpm version: $(pnpm --version)"
            echo "Python version: $(python --version)"
            echo "uv version: $(uv --version)"
          '';
        };
      }
    );
}
