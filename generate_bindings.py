import litgen

opts = litgen.LitgenOptions()
# opts.python_expose_enum_class = True
# opts.classes_expose_nested = True
# opts.enum_remove_scope = False
# opts.class_remove_scope = False


opts.srcmlcpp_options.header_filter_preprocessor_regions = True

opts.fn_template_options.add_specialization("Parse", ["std::vector<unsigned int>", "std::vector<double>", "std::set<unsigned int>", "std::vector<int>", "bool", "std::string", "double", "float", "char", "int"], add_suffix_to_function_name=True)

opts.type_replacements.add_replacement("Gedim::IMeshDAO", "Gedim::MeshMatricesDAO")

# opts.fn_template_options.add_specialization("Timer", ["std::chrono::milliseconds"], add_suffix_to_function_name=True)

headers = ["PolyDiM/gedim/GeDiM/src/IO/StringsUtilities.hpp",
           "PolyDiM/gedim/GeDiM/src/Geometry/GeometryUtilities.hpp",
           "PolyDiM/gedim/GeDiM/src/Geometry/MapParallelepiped.hpp",
           "PolyDiM/gedim/GeDiM/src/Geometry/MapHexahedron.hpp",
           "PolyDiM/gedim/GeDiM/src/Geometry/MapTriangle.hpp",
           "PolyDiM/gedim/GeDiM/src/Geometry/MapParallelogram.hpp",
           "PolyDiM/gedim/GeDiM/src/Geometry/MapTetrahedron.hpp",
           "PolyDiM/gedim/GeDiM/src/Geometry/MapQuadrilateral.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/ConformerMeshPolygon.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/ConformerMeshSegment.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/ConformMeshUtilities.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/IntersectorMesh2DSegment.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/IntersectorMesh3DSegment.hpp",
            "PolyDiM/gedim/GeDiM/src/Mesh/MeshDAOExporterToCsv.hpp",
            "PolyDiM/gedim/GeDiM/src/Mesh/MeshDAOImporterFromCsv.hpp",
            "PolyDiM/gedim/GeDiM/src/Mesh/MeshFromCsvUtilities.hpp",
            "PolyDiM/gedim/GeDiM/src/Mesh/MeshMatrices.hpp",
            "PolyDiM/gedim/GeDiM/src/Mesh/MeshMatricesDAO.hpp",
            "PolyDiM/gedim/GeDiM/src/Mesh/MeshUtilities.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/ObjectFileFormatInterface.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/OpenVolumeMeshInterface.hpp",
            "PolyDiM/gedim/GeDiM/src/Mesh/PlatonicSolid.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/RefinementUtilities.hpp",
            "PolyDiM/gedim/GeDiM/src/Mesh/SphereMeshUtilities.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/TetgenInterface.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/TriangleInterface.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/UnionMeshSegment.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/VoroInterface.hpp",
            #"PolyDiM/gedim/GeDiM/src/Mesh/VtkMeshInterface.hpp",
            "PolyDiM/gedim/GeDiM/src/Quadrature/Quadrature_Gauss2D_Triangle.hpp",
            "PolyDiM/gedim/GeDiM/src/Quadrature/Quadrature_Gauss2D_Square.hpp",
            "PolyDiM/gedim/GeDiM/src/Quadrature/Quadrature_Gauss3D_Hexahedron.hpp",
            "PolyDiM/gedim/GeDiM/src/Quadrature/Quadrature_GaussLobatto1D.hpp",
            "PolyDiM/gedim/GeDiM/src/Quadrature/Quadrature_Gauss1D.hpp",
            "PolyDiM/gedim/GeDiM/src/Quadrature/QuadratureData.hpp",
            "PolyDiM/gedim/GeDiM/src/Quadrature/Quadrature_Gauss3D_Tetrahedron_PositiveWeights.hpp",
            "PolyDiM/gedim/GeDiM/src/Quadrature/Quadrature_Gauss3D_Tetrahedron.hpp",
            "PolyDiM/PolyDiM/src/Interpolation/lagrange_1D.hpp",
            "PolyDiM/PolyDiM/src/VEM/Quadrature/VEM_Quadrature_2D.hpp",
            "PolyDiM/PolyDiM/src/VEM/Quadrature/VEM_Quadrature_3D.hpp",
            #"PolyDiM/PolyDiM/src/VEM/Utilities/VEM_GBasis_2D.hpp",
            #"PolyDiM/PolyDiM/src/VEM/Utilities/VEM_GBasis_3D.hpp",
            #"PolyDiM/PolyDiM/src/VEM/Utilities/VEM_GBasis_Data.hpp",
            #"PolyDiM/PolyDiM/src/VEM/Utilities/VEM_Monomials_1D.hpp",
            #"PolyDiM/PolyDiM/src/VEM/Utilities/VEM_Monomials_2D.hpp",
            #"PolyDiM/PolyDiM/src/VEM/Utilities/VEM_Monomials_3D.hpp",
            #"PolyDiM/PolyDiM/src/VEM/Utilities/VEM_Monomials_Data.hpp",
            #"PolyDiM/PolyDiM/src/VEM/Utilities/VEM_Monomials_Utilities.hpp",
            #"PolyDiM/PolyDiM/src/VEM/Utilities/VEM_Inertia_Utilities.hpp"
            ]

# Stampa a console:
litgen.write_generated_code_for_files(
    options=opts,
    input_cpp_header_files=headers,
    output_cpp_pydef_file="bindings.cpp",
    output_stub_pyi_file="bindings.pyi",
)