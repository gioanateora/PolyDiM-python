import litgen

opts = litgen.LitgenOptions()
opts.fn_template_options.add_specialization("Parse", ["std::vector<unsigned int>", "std::vector<double>", "std::set<unsigned int>", "std::vector<int>", "bool", "std::string", "double", "float", "char", "int"], add_suffix_to_function_name=True)
# opts.fn_template_options.add_specialization("Timer", ["std::chrono::milliseconds"], add_suffix_to_function_name=True)

opts.class_template_options.add_ignore("GeometryUtilities")
opts.type_replacements.add_replacement("Type", "int")

# Stampa a console:
# gen = litgen.generate_code_for_file(options=opts, filename="src/test.hpp")
litgen.write_generated_code_for_files(
    options=opts,
    input_cpp_header_files=["PolyDiM/gedim/GeDiM/src/IO/StringsUtilities.hpp", 
                            "PolyDiM/gedim/GeDiM/src/Geometry/GeometryUtilities.hpp"],
    output_cpp_pydef_file="bindings.cpp",
    output_stub_pyi_file="bindings.pyi",
)