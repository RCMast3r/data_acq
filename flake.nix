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
    ht_can_pkg_flake.url = "github:hytech-racing/ht_can";
    nix-proto = { url = "github:notalltim/nix-proto"; };
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils, mcap-protobuf, mcap, foxglove-websocket
    , asyncudp, nix-proto, ht_can_pkg_flake, flake-utils, ... } @inputs:
    flake-utils.lib.eachSystem ["aarch64-darwin" "aarch64-linux" "x86_64-linux" "x86_64-darwin"] (system:
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
      frontend_overlay = final: prev: {
        frontend_pkg = final.callPackage ./frontend.nix { };
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
        frontend_overlay
        ht_can_pkg_flake.overlays.default
        mcap-protobuf.overlays.default
        mcap.overlays.default
        asyncudp.overlays.default
        foxglove-websocket.overlays.default
      ] ++ nix-proto.lib.overlayToList nix_protos_overlays;

      pkgs = import nixpkgs {
        inherit system;
        config = {
          #allowUnsupportedSystem = true;
        };
        overlays = my_overlays;
      };


      shared_shell = pkgs.mkShell {
        name = "nix-devshell";
        buildInputs = with pkgs; [
          jq
          py_data_acq_pkg
          py_dbc_proto_gen_pkg
          proto_gen_pkg
          frontend_pkg
          ht_can_pkg
          cmake
          can-utils
        ];
        shellHook = let icon = "f121";  name = "nix-devshell";
        in ''
          path=${pkgs.proto_gen_pkg}
          bin_path=$path"/bin"
          dbc_path=${pkgs.ht_can_pkg}
          export BIN_PATH=$bin_path
          export DBC_PATH=$dbc_path

          echo -e "PYTHONPATH=$PYTHONPATH\nBIN_PATH=$bin_path\nDBC_PATH=$dbc_path\n" > .env
          export PS1="$(echo -e '\u${icon}') {\[$(tput sgr0)\]\[\033[38;5;228m\]\w\[$(tput sgr0)\]\[\033[38;5;15m\]} (${name}) \\$ \[$(tput sgr0)\]"
        '';
      };
      
    in {
      overlays.default = nixpkgs.lib.composeManyExtensions my_overlays;
      
      devShells = {
        default = shared_shell;
      };
      

    });
}
