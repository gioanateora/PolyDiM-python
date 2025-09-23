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
            "PolyDiM/gedim/GeDiM/src/Geometry/MapTriangle.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/ConformerMeshPolygon.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/ConformerMeshSegment.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/ConformMeshUtilities.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/IMeshDAO.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/IntersectorMesh2DSegment.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/IntersectorMesh3DSegment.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/MeshDAOExporterToCsv.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/MeshDAOImporterFromCsv.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/MeshFromCsvUtilities.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/MeshMatrices.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/MeshMatricesDAO.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/MeshUtilities.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/ObjectFileFormatInterface.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/OpenVolumeMeshInterface.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/PlatonicSolid.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/RefinementUtilities.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/SphereMeshUtilities.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/TetgenInterface.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/TriangleInterface.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/UnionMeshSegment.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/VoroInterface.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/VtkMeshInterface.hpp"
            ]

# Stampa a console:
litgen.write_generated_code_for_files(
    options=opts,
    input_cpp_header_files=headers,
    output_cpp_pydef_file="bindings.cpp",
    output_stub_pyi_file="bindings.pyi",
)