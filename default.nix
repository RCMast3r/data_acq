{ lib, python311Packages, mcap_support_pkg }:

python311Packages.buildPythonApplication {
  pname = "py_data_acq";
  version = "1.0";


  propagatedBuildInputs = [ python311Packages.cantools python311Packages.protobuf mcap_support_pkg ];

  src = ./py_data_acq;
}