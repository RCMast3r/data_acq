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
        runHook preBuild
        export HOME=$TMP
        
        ln -s ${generated.nodeDependencies}/lib/node_modules ./node_modules
        export PATH="${generated.nodeDependencies}/bin:$PATH"
        npm run build
        runHook postBuild
      '';
      installPhase = ''
        runHook preInstall
            
        mkdir -p $out/bin
        # copy only whats needed for running the built app
        cp package.json $out/package.json
        cp -r dist $out/dist
        ln -sf ${generated.nodeDependencies}/lib/node_modules $out/node_modules
        # copy entry point, in this case our index.ts has the node shebang
        # nix will patch the shebang to be the node version specified in buildInputs
        # you could also copy in a script that is basically `npm run start`
        cp dist/index.js $out/bin/frontend
        chmod a+x $out/bin/frontend
        runHook postInstall
      '';
    };
}
