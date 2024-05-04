{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "react-create-vite-extended-template-shell";
  buildInputs = with pkgs; [
    (import ./default.nix { inherit pkgs; }).buildInputs
    # rubyPackages.rspec
  ];
}
