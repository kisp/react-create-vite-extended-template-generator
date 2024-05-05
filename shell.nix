{ pkgs ? import <nixpkgs> {} }:

let
  # How to install and use tree-sitter grammars? · Issue #341 · nix-community/emacs-overlay
  # https://github.com/nix-community/emacs-overlay/issues/341
  myEmacs = (pkgs.emacsPackagesFor pkgs.emacs-nox).emacsWithPackages (epkgs: with epkgs; [
    vterm
    treesit-grammars.with-all-grammars
  ]);

in

pkgs.mkShell {
  name = "react-create-vite-extended-template-shell";
  buildInputs = with pkgs; [
    (import ./default.nix { inherit pkgs; }).buildInputs
    pkgs.yamllint
    myEmacs
    pkgs.emacsPackages.magit
    pkgs.emacsPackages.yaml-mode
    pkgs.emacsPackages.whitespace-cleanup-mode
    pkgs.emacsPackages.flycheck
    pkgs.emacsPackages.flycheck-yamllint
    pkgs.emacsPackages.nix-mode
    pkgs.emacsPackages.modus-themes
  ];
}
