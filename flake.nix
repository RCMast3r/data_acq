{
  description = "python data aquisition package";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    utils.url = "github:numtide/flake-utils";
    mcap-protobuf.url = "github:RCMast3r/mcap-protobuf-support-flake";
    mcap.url = "github:RCMast3r/py_mcap_nix";
    foxglove-websocket.url = "github:RCMast3r/py_foxglove_webserver_nix";
    asyncudp.url = "github:RCMast3r/asyncudp_nix";
  };
  outputs = { self, nixpkgs, utils, mcap-protobuf, mcap, foxglove-websocket, asyncudp }:
    let
      py_data_acq_overlay = final: prev: {
        py_data_acq_pkg = final.callPackage ./default.nix { };
      };
      py_dbc_proto_gen_overlay = final: prev: {
        py_dbc_proto_gen_pkg = final.callPackage ./dbc_proto_gen.nix { };
      };
      my_overlays = [ py_dbc_proto_gen_overlay py_data_acq_overlay mcap-protobuf.overlays.default mcap.overlays.default asyncudp.overlays.default foxglove-websocket.overlays.default ];
      pkgs = import nixpkgs {
        system = "x86_64-linux";
        overlays = [ self.overlays.default ];
      };
    in
    {
      overlays.default = nixpkgs.lib.composeManyExtensions my_overlays;
      packages.x86_64-linux =
        rec {
          py_data_acq_pkg = pkgs.py_data_acq_pkg;
          py_dbc_proto_gen_pkg = pkgs.py_dbc_proto_gen_pkg;
          default = py_data_acq_pkg;
        };
      devShells.x86_64-linux.default =
        pkgs.mkShell rec {
          # Update the name to something that suites your project.
          name = "nix-devshell";
          packages = with pkgs; [
            # Development Tools
            py_dbc_proto_gen_pkg
            cmake
          ];
          # Setting up the environment variables you need during
          # development.
          shellHook =
            let
              icon = "f121";
            in
            ''
              export PS1="$(echo -e '\u${icon}') {\[$(tput sgr0)\]\[\033[38;5;228m\]\w\[$(tput sgr0)\]\[\033[38;5;15m\]} (${name}) \\$ \[$(tput sgr0)\]"
            '';
        };

    };
}