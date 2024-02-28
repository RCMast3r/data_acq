# 🍳 cookin 👩‍🍳
{
  description = "python data aquisition flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    utils.url = "github:numtide/flake-utils";
    mcap-protobuf.url = "github:RCMast3r/mcap-protobuf-support-flake";
    mcap.url = "github:RCMast3r/py_mcap_nix";
    foxglove-websocket.url = "github:RCMast3r/py_foxglove_webserver_nix";
    asyncudp.url = "github:RCMast3r/asyncudp_nix";
    ht_can_pkg_flake.url = "github:hytech-racing/ht_can/TPMS_add";
    nix-proto = { url = "github:notalltim/nix-proto"; };
  };

  outputs = { self, nixpkgs, utils, mcap-protobuf, mcap, foxglove-websocket
    , asyncudp, nix-proto, ht_can_pkg_flake, ... }@inputs:
    let
      makePackageSet = pkgs: {
        py_data_acq_pkg = pkgs.py_data_acq_pkg;
        py_dbc_proto_gen_pkg = pkgs.py_dbc_proto_gen_pkg;
        proto_gen_pkg = pkgs.proto_gen_pkg;
        hytech_np = pkgs.hytech_np;
        hytech_np_proto_py = pkgs.hytech_np_proto_py;
        default = pkgs.py_data_acq_pkg;
      };

      py_data_acq_overlay = final: prev: {
        py_data_acq_pkg = final.callPackage ./default.nix { };
      };
      py_dbc_proto_gen_overlay = final: prev: {
        py_dbc_proto_gen_pkg = final.callPackage ./dbc_proto_gen_script.nix { };
      };
      proto_gen_overlay = final: prev: {
        proto_gen_pkg = final.callPackage ./dbc_proto_bin_gen.nix { };
      };

      nix_protos_overlays = nix-proto.generateOverlays' {
        hytech_np = { proto_gen_pkg }:
          nix-proto.mkProtoDerivation {
            name = "hytech_np";
            buildInputs = [ proto_gen_pkg ];
            src = proto_gen_pkg.out + "/proto";
            version = "1.0.0";
          };
      };
      my_overlays = [
        py_dbc_proto_gen_overlay
        py_data_acq_overlay
        proto_gen_overlay
        ht_can_pkg_flake.overlays.default
        mcap-protobuf.overlays.default
        mcap.overlays.default
        asyncudp.overlays.default
        foxglove-websocket.overlays.default
      ] ++ nix-proto.lib.overlayToList nix_protos_overlays;
      system = builtins.currentSystem;
      x86_pkgs = import nixpkgs {
        system = "x86_64-linux";
        # inherit system;
        # system = builtins.currentSystem;
        overlays = [ self.overlays.default ]
          ++ nix-proto.lib.overlayToList nix_protos_overlays;
      };

      arm_pkgs = import nixpkgs {
        system = "aarch64-linux";
        # inherit system;
        # system = builtins.currentSystem;
        overlays = [ self.overlays.default ]
          ++ nix-proto.lib.overlayToList nix_protos_overlays;
      };

      packageSets = {
        "x86_64-linux" = makePackageSet x86_pkgs;
        "aarch64-linux" = makePackageSet arm_pkgs;
        # Add more systems as needed
      };
    in {

      overlays.default = nixpkgs.lib.composeManyExtensions my_overlays;

      packages = packageSets;

      devShells.x86_64-linux.default = x86_pkgs.mkShell rec {
        # Update the name to something that suites your project.
        name = "nix-devshell";
        packages = with x86_pkgs; [
          jq
          py_data_acq_pkg
          py_dbc_proto_gen_pkg
          proto_gen_pkg
          ht_can_pkg
          cmake
          can-utils
        ];
        # Setting up the environment variables you need during
        # development.
        shellHook = let icon = "f121";
        in ''
          path=${x86_pkgs.proto_gen_pkg}
          bin_path=$path"/bin"
          dbc_path=${x86_pkgs.ht_can_pkg}
          export BIN_PATH=$bin_path
          export DBC_PATH=$dbc_path

          echo -e "PYTHONPATH=$PYTHONPATH\nBIN_PATH=$bin_path\nDBC_PATH=$dbc_path\n" > .env
          export PS1="$(echo -e '\u${icon}') {\[$(tput sgr0)\]\[\033[38;5;228m\]\w\[$(tput sgr0)\]\[\033[38;5;15m\]} (${name}) \\$ \[$(tput sgr0)\]"
        '';
      };
      devShells.x86_64-linux.ci = x86_pkgs.mkShell rec {
        # Update the name to something that suites your project.
        name = "nix-devshell";
        packages = with x86_pkgs; [
          # Development Tools
          py_dbc_proto_gen_pkg
          proto_gen_pkg
          ht_can_pkg
          protobuf
        ];
        shellHook =
        ''
          path=${x86_pkgs.proto_gen_pkg}
          bin_path=$path"/bin"
          dbc_path=${x86_pkgs.ht_can_pkg}
          export BIN_PATH=$bin_path
          export DBC_PATH=$dbc_path
        '';

      };

    };
}
