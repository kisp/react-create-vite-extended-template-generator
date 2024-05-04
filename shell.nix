{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "react-create-vite-extended-template-shell";
  buildInputs = with pkgs; [
    (import ./default.nix { inherit pkgs; }).buildInputs
    pkgs.yamllint
    pkgs.emacs-nox
    pkgs.emacsPackages.yaml-mode
    pkgs.emacsPackages.whitespace-cleanup-mode
    pkgs.emacsPackages.flycheck
    pkgs.emacsPackages.flycheck-yamllint
    pkgs.emacsPackages.nix-mode
    pkgs.emacsPackages.modus-themes
  ];
}
