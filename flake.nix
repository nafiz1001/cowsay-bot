{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    utils.url = "github:numtide/flake-utils";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, utils, ... }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
        {
          devShell = with pkgs; mkShell {
            buildInputs = [
	            pkgs.bashInteractive
              (python311.withPackages (p: with p; [ pip virtualenv ])) nodePackages.pyright # python
            ];
          };
        });
}
