{ lib, python311Packages, fetchFromGitHub, fetchgit }: 

python311Packages.buildPythonPackage rec {
  pname = "py_foxglove_protobuf_schemas";
  version = "1.0.0";
  format="pyproject";
  src_repo = fetchgit {
    url = "https://github.com/foxglove/schemas.git";
    rev = "2417be2ba8fdb8174bc69cc7da450f302ac46396";  # Specify the specific commit, tag, or branch
    sha256 = "sha256-P8MH4ICaS40XU8s9TsljCbFr9F98EREo/hrnwRIi9aA=";  # SHA256 hash of the source
  };

  # Extract the specific subdirectory within the repository
  propagatedBuildInputs = [  python311Packages.setuptools ];
  src = src_repo + "/python/foxglove-schemas-protobuf";  # Adjust the path to your desired subdirectory

  meta = with lib; {
    description = "foxglove protobuf schemas";
    license = licenses.mit;
  };
} 