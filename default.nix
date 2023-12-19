{ lib, python311Packages }:

python311Packages.buildPythonApplication {
  pname = "py_data_acq";
  version = "1.0";

  propagatedBuildInputs = [ python311Packages.cantools ];

  src = ./py_data_acq;
}