{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation rec {
  name = "react-create-vite-extended-template";

  src = ./.;

  buildInputs = [
    pkgs.ansible
    pkgs.nodejs
  ];

  nativeBuildInputs = [ pkgs.makeWrapper ];

  installPhase = ''
    mkdir -p $out/bin
    mkdir -p $out/lib
    cp exe/app.rb $out/bin
    cp lib/*.rb $out/lib
  '';

  postFixup = ''
  wrapProgram $out/bin/app.rb \
    --set RUBYLIB $RUBYLIB
'';
}
