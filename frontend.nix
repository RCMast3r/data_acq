{ pkgs, stdenv, system, callPackage, nodejs, nodePackages, writeShellScriptBin }:
let
  # Import & invoke the generated files from node2nix
  generated = callPackage ./frontend/nix { inherit pkgs system nodejs; };

  # node2nix wrapper to update nix files on npm changes
  node2nix = writeShellScriptBin "node2nix" ''
    ${nodePackages.node2nix}/bin/node2nix \
      --development \
      -l package-lock.json \
      -c ./frontend/nix/default.nix \
      -o ./frontend/nix/node-packages.nix \
      -e ./frontend/nix/node-env.nix
  '';

in
{
  inherit (generated) nodeDependencies;
  frontend = pkgs.stdenv.mkDerivation
    {
      name = "frontend";
      version = "0.1.0";
      src = ./frontend; #gitignore.lib.gitignoreSource ./.; # uses the gitignore in the repo to only copy files git would see
      buildInputs = [ pkgs.nodejs ];
      buildPhase = ''
        export HOME=$TMP
        
        ln -s ${generated.nodeDependencies}/lib/node_modules ./node_modules
        export PATH="${generated.nodeDependencies}/bin:$PATH"
        npm run build
      '';
      installPhase = ''
        ls
        cp -r build $out/
      '';
    };
}
