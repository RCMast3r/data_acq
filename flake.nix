{
  description = "python data aquisition package";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    utils.url = "github:numtide/flake-utils";
    mcap-protobuf.url = "github:RCMast3r/mcap-protobuf-support-flake";
    mcap.url = "github:RCMast3r/py_mcap_nix";
    foxglove-websocket.url = "github:RCMast3r/py_foxglove_webserver_nix";
    asyncudp.url = "github:RCMast3r/asyncudp_nix";
    nix-proto = { url = "github:notalltim/nix-proto"; };
  };
  outputs = { self, nixpkgs, utils, mcap-protobuf, mcap, foxglove-websocket
    , asyncudp, nix-proto, ... }@inputs:
    let
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
            src = proto_gen_pkg.out;
            version = "1.0.0";
          };
      };
      my_overlays = [
        py_dbc_proto_gen_overlay
        py_data_acq_overlay
        proto_gen_overlay
        mcap-protobuf.overlays.default
        mcap.overlays.default
        asyncudp.overlays.default
        foxglove-websocket.overlays.default

      ];

      pkgs = import nixpkgs {
        system = "x86_64-linux";
        overlays = [ self.overlays.default ]
          ++ nix-proto.lib.overlayToList nix_protos_overlays;
      };
      # overlay_set = nixpkgs.lib.composeManyExtensions my_overlays;
    in {

      overlays.default = nixpkgs.lib.composeManyExtensions my_overlays;
      packages.x86_64-linux = rec {
        py_data_acq_pkg = pkgs.py_data_acq_pkg;
        py_dbc_proto_gen_pkg = pkgs.py_dbc_proto_gen_pkg;
        proto_gen_pkg = pkgs.proto_gen_pkg;
        test_proto = pkgs.test_proto;
        hytech_np_proto_py = pkgs.hytech_np_proto_py;
        default = py_data_acq_pkg;
      };

      devShells.x86_64-linux.default = pkgs.mkShell rec {
        # Update the name to something that suites your project.
        name = "nix-devshell";
        packages = with pkgs; [ py_data_acq_pkg py_dbc_proto_gen_pkg cmake ];
        # Setting up the environment variables you need during
        # development.
        shellHook = let icon = "f121";
        in ''
          export PS1="$(echo -e '\u${icon}') {\[$(tput sgr0)\]\[\033[38;5;228m\]\w\[$(tput sgr0)\]\[\033[38;5;15m\]} (${name}) \\$ \[$(tput sgr0)\]"
        '';
      };
      devShells.x86_64-linux.ci = pkgs.mkShell rec {
        # Update the name to something that suites your project.
        name = "nix-devshell";
        packages = with pkgs; [
          # Development Tools
          py_dbc_proto_gen_pkg
          protobuf
        ];

      };

    };
}
