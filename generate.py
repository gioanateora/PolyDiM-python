import litgen

headers = [
    "PolyDiM/gedim/GeDiM/src/Geometry/GeometryUtilities.hpp",
]

opts = litgen.LitgenOptions()
litgen.write_generated_code_for_files(
    options=opts,
    input_cpp_header_files=headers,
    output_cpp_pydef_file="bindings.cpp",
    output_stub_pyi_file="binding.pyi",
)
