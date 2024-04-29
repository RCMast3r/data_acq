{pkgs}:
pkgs.stdenv.mkDerivation rec {
  name = "frontend_config";
  
  src = ./frontend_config;
  installPhase = ''
    mkdir -p $out
    cp *.json $out
  '';
}