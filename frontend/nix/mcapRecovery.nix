{ lib, pkgs, config, ... }:
with lib;
let

  cfg = config.services.mcap_recovery;
in {

    environment.systemPackages = with pkgs; [$ wget https://github.com/foxglove/mcap/releases/download/releases%2Fmcap-cli%2Fv0.0.43/mcap-linux-$(arch) -O mcap]

  config = {
    systemd.services.mcap_recovery = {
      serviceConfig.ExecStart =
        "
        chmod +x mcap;
        mcap recover [mcap file]
        ";
      serviceConfig.ExecStop = "/bin/kill -SIGINT $MAINPID";
      serviceConfig.Restart = "on-failure";
    };
  };
}
