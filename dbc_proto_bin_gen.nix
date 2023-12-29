{pkgs, py_dbc_proto_gen_pkg}:

pkgs.stdenv.mkDerivation rec {
  name = "ht-proto-gen";
  
  src = builtins.filterSource (path: type: false) ./.;
  
  buildInputs = [ py_dbc_proto_gen_pkg ]; # Python as a build dependency
  
  # Define the build phase to execute the scripts
  buildPhase = ''
    # Run the Python script
    ht_dbc_proto_creator.py
  '';

  # Specify the output of the build process
  # In this case, it will be the generated file
  installPhase = ''
    mkdir -p $out
    cp hytech.proto $out
  '';
}