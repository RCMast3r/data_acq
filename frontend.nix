appBuild = pkgs.stdenv.mkDerivation {
          name = "frontend";
          version = "0.1.0";
          src = gitignore.lib.gitignoreSource ./.; # uses the gitignore in the repo to only copy files git would see
          buildInputs = [ nodejs ];
          # https://nixos.org/manual/nixpkgs/stable/#sec-stdenv-phases
          buildPhase = ''
            # each phase has pre/postHooks. When you make your own phase be sure to still call the hooks
            runHook preBuild
            npm ci
            npm run build
            runHook postBuild
          '';
          installPhase = ''
            runHook preInstall
            cp -r node_modules $out/node_modules
            cp package.json $out/package.json
            cp -r dist $out/dist
            runHook postInstall
          '';
        };
