{pkgs, py_dbc_proto_gen_pkg, ht_can_pkg, protobuf}:

pkgs.stdenv.mkDerivation rec {
  name = "ht-proto-gen";
  
  src = builtins.filterSource (path: type: false) ./.;
  
  buildInputs = [ py_dbc_proto_gen_pkg ht_can_pkg protobuf ]; # Python as a build dependency
  
  # Define the build phase to execute the scripts
  buildPhase = ''
    # Run the Python script
    echo ${ht_can_pkg}
    dbc_to_proto.py ${ht_can_pkg}
    protoc --include_imports --descriptor_set_out=hytech.bin hytech.proto
  '';

  # Specify the output of the build process
  # In this case, it will be the generated file
  installPhase = ''
    mkdir -p $out/proto
    mkdir -p $out/bin
    cp hytech.proto $out/proto
    cp hytech.bin $out/bin
  '';
}