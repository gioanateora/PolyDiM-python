import litgen

opts = litgen.LitgenOptions()
# opts.python_expose_enum_class = True
# opts.classes_expose_nested = True
# opts.enum_remove_scope = False
# opts.class_remove_scope = False

# Eigen support (important!)
opts.srcmlcpp_options.fn_args_resolve_eigen_matrix_to_numpy = True
opts.srcmlcpp_options.header_filter_preprocessor_regions = True

# opts.fn_template_options.add_specialization("Parse", ["std::vector<unsigned int>", "std::vector<double>", "std::set<unsigned int>", "std::vector<int>", "bool", "std::string", "double", "float", "char", "int"], add_suffix_to_function_name=True)
# opts.fn_template_options.add_specialization("Timer", ["std::chrono::milliseconds"], add_suffix_to_function_name=True)

headers = ["PolyDiM/gedim/GeDiM/src/Geometry/GeometryUtilities.hpp",
           "PolyDiM/gedim/GeDiM/src/Geometry/MapParallelepiped.hpp",
            "PolyDiM/gedim/GeDiM/src/Geometry/MapHexahedron.hpp",
            "PolyDiM/gedim/GeDiM/src/Geometry/MapParallelogram.hpp",
            "PolyDiM/gedim/GeDiM/src/Geometry/MapQuadrilateral.hpp",
            "PolyDiM/gedim/GeDiM/src/Geometry/MapTetrahedron.hpp",
            "PolyDiM/gedim/GeDiM/src/Geometry/MapTriangle.hpp"]

# Stampa a console:
litgen.write_generated_code_for_files(
    options=opts,
    input_cpp_header_files=headers,
    output_cpp_pydef_file="bindings.cpp",
    output_stub_pyi_file="bindings.pyi",
)