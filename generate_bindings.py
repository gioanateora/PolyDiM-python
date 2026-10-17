import litgen
import re, pathlib


definitions: dict[str, bool] = {"pybind": True}


def preprocess_cpp(code: str) -> str:
    """
    Rimuove:
    - la riga '#if pybind == 1'
    - la riga '#else'
    - la riga '#endif'
    - tutto ciò che è tra #else e #endif
    lasciando solo il blocco di codice valido sotto #if PYBIND == 1.
    """
    lines = code.splitlines(keepends=True)
    output_lines = []

    inside_if_block = False
    inside_else_block = False
    nesting_level = 0

    for line in lines:
        stripped = line.strip()

        if definitions["pybind"]:
            # Inizio blocco condizionale specifico
            if re.match(r"#\s*if\s+PYBIND\s*==\s*1", stripped):
                inside_if_block = True
                nesting_level += 1
                continue  # rimuove la riga #if pybind == 1

            # Rileva #else nel blocco che ci interessa
            if re.match(r"#\s*else\b", stripped) and inside_if_block and nesting_level == 1:
                inside_else_block = True
                continue  # rimuove la riga #else

            # Rileva #endif
            if re.match(r"#\s*endif\b", stripped) and inside_else_block:
                if inside_if_block and nesting_level == 1:
                    inside_if_block = False
                    inside_else_block = False
                nesting_level -= 1
                continue  # rimuove la riga #endif

            # Se siamo dentro il blocco else, salta le righe
            if inside_else_block:
                continue
        else:

            if re.match(r"#\s*if\s+PYBIND\s*==\s*1", stripped):
                inside_if_block = True
                continue  # rimuove la riga #if pybind == 1

            if inside_if_block and not re.match(r"#\s*else\b", stripped):
                continue

            # Rileva #else
            if re.match(r"#\s*else\b", stripped) and inside_if_block:
                inside_if_block = False
                inside_else_block = True
                continue  # rimuove la riga #endif

            # Rileva #else nel blocco che ci interessa
            if re.match(r"#\s*endif\b", stripped) and inside_else_block:
                inside_else_block = False
                continue  # rimuove la riga #else

        output_lines.append(line)

    return "".join(output_lines)


def remove_imesh(code: str) -> str:
    """
    Rimuove:
    - la riga '#if pybind == 1'
    - la riga '#else'
    - la riga '#endif'
    - tutto ciò che è tra #else e #endif
    lasciando solo il blocco di codice valido sotto #if PYBIND == 1.
    """
    lines = code.splitlines(keepends=True)
    output_lines = []

    pattern = r"\bGedim::IMeshDAO\b"
    replacement = "Gedim::MeshMatricesDAO"

    pattern1 = r"\bIMeshDAO.hpp\b"
    replacement1 = "MeshMatricesDAO.hpp"

    for line in lines:

        line = re.sub(pattern, replacement, line)
        line = re.sub(pattern1, replacement1, line)

        output_lines.append(line)

    #g = "".join(output_lines)

    #print(g)

    return "".join(output_lines)

def preprocess(code: str) -> str:
    code_1 = preprocess_cpp(code)
    #code_2 = remove_imesh(code_1)

    return code_1



opts = litgen.LitgenOptions()

opts.srcmlcpp_options.header_filter_preprocessor_regions = True

opts.class_exclude_by_name__regex = r"^I_VEM_PCC_2D_ReferenceElement$"
opts.srcmlcpp_options.named_number_macros["UINT_MAX"] = 2147483647

opts.class_override_virtual_methods_in_python__regex = "^IMeshDAO$|^MeshMatricesDAO$"

opts.fn_template_options.add_specialization("ComputePolynomialsValues", ["Polydim::Utilities::Monomials_2D", "Polydim::Utilities::Monomials_3D"], add_suffix_to_function_name=False)
opts.fn_template_options.add_specialization("ComputePolynomialsDerivativeValues", ["Polydim::Utilities::Monomials_2D", "Polydim::Utilities::Monomials_3D"], add_suffix_to_function_name=False)
opts.fn_template_options.add_specialization("ComputePolynomialsLaplacianValues", ["Polydim::Utilities::Monomials_2D", "Polydim::Utilities::Monomials_3D"], add_suffix_to_function_name=False)

opts.fn_template_options.add_specialization("Create_Constant_DOFsInfo_0D", ["Polydim::PDETools::Mesh::MeshMatricesDAO_mesh_connectivity_data"], add_suffix_to_function_name=False)
opts.fn_template_options.add_specialization("Create_Constant_DOFsInfo_1D", ["Polydim::PDETools::Mesh::MeshMatricesDAO_mesh_connectivity_data"], add_suffix_to_function_name=False)
opts.fn_template_options.add_specialization("Create_Constant_DOFsInfo_2D", ["Polydim::PDETools::Mesh::MeshMatricesDAO_mesh_connectivity_data"], add_suffix_to_function_name=False)
opts.fn_template_options.add_specialization("Create_Constant_DOFsInfo_3D", ["Polydim::PDETools::Mesh::MeshMatricesDAO_mesh_connectivity_data"], add_suffix_to_function_name=False)

opts.fn_template_options.add_specialization("CreateDOFs_1D", ["Polydim::PDETools::Mesh::MeshMatricesDAO_mesh_connectivity_data"], add_suffix_to_function_name=False)
opts.fn_template_options.add_specialization("CreateDOFs_2D", ["Polydim::PDETools::Mesh::MeshMatricesDAO_mesh_connectivity_data"], add_suffix_to_function_name=False)
opts.fn_template_options.add_specialization("CreateDOFs_3D", ["Polydim::PDETools::Mesh::MeshMatricesDAO_mesh_connectivity_data"], add_suffix_to_function_name=False)

opts.class_template_options.add_specialization(
    name_regex=r"^UCDProperty$",
    cpp_types_list_str=["double"]
)

opts.srcmlcpp_options.ignored_warning_parts.append("Ignoring template function")

opts.srcmlcpp_options.code_preprocess_function = preprocess
litgen.generate_code_for_file(options=opts, filename="PolyDiM/PolyDiM-core/src/VEM/PCC/VEM_PCC_Utilities.hpp")
litgen.generate_code_for_file(options=opts, filename="PolyDiM/PolyDiM-core/src/VEM/DF_PCC/VEM_DF_PCC_Utilities.hpp")
litgen.generate_code_for_file(options=opts, filename="PolyDiM/PolyDiM-core/src/PDETools/DOFs/DOFsManager.hpp")

headers = ["./PolyDiM/gedim/GeDiM-core/src/Geometry/GeometryUtilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapHexahedron.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapParallelepiped.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapParallelogram.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapQuadrilateral.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapTetrahedron.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapTriangle.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/ConformerMeshPolygon.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/ConformerMeshSegment.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/ConformMeshUtilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/IMeshDAO.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/IntersectorMesh2DSegment.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/IntersectorMesh3DSegment.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshDAOExporterToCsv.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshDAOImporterFromCsv.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshFromCsvUtilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshMatrices.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshMatricesDAO.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshUtilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/ObjectFileFormatInterface.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/OpenVolumeMeshInterface.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/PlatonicSolid.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/RefinementUtilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/SphereMeshUtilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/UnionMeshSegment.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Mesh/WavefrontOBJInterface.hpp",
           #"./PolyDiM/gedim/GeDiM-core/src/IO/IOStream.hpp",
           #"./PolyDiM/gedim/GeDiM-core/src/IO/IOUtilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/IO/MEDIT_Utilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/IO/StringsUtilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/IO/UCDUtilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/MpiTools/GraphUtilities.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss1D.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss2D_Square.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss2D_Triangle.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss3D_Hexahedron.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss3D_Tetrahedron_PositiveWeights.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss3D_Tetrahedron.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_GaussLobatto1D.hpp",
           "./PolyDiM/gedim/GeDiM-core/src/Quadrature/QuadratureData.hpp",
           "./PolyDiM/gedim/3rd_party_libraries/src/MetisInterface/MetisUtilities.hpp",
           "./PolyDiM/gedim/3rd_party_libraries/src/TetgenInterface/CreateMeshWithHoles.hpp",
           "./PolyDiM/gedim/3rd_party_libraries/src/TetgenInterface/TetgenInterface.hpp",
           "./PolyDiM/gedim/3rd_party_libraries/src/TriangleInterface/TriangleInterface.hpp",
           "./PolyDiM/gedim/3rd_party_libraries/src/VoroInterface/VoroInterface.hpp",
           "./PolyDiM/PolyDiM-core/src/Interpolation/lagrange_1D.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/Quadrature/VEM_Quadrature_2D.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/Quadrature/VEM_Quadrature_3D.hpp",
           "./PolyDiM/PolyDiM-core/src/Utilities/Monomials_1D.hpp",
           "./PolyDiM/PolyDiM-core/src/Utilities/Monomials_2D.hpp",
           "./PolyDiM/PolyDiM-core/src/Utilities/Monomials_3D.hpp",
           "./PolyDiM/PolyDiM-core/src/Utilities/Monomials_Data.hpp",
           # "./PolyDiM/PolyDiM-core/src/Utilities/Monomials_Utilities.hpp",
           "./PolyDiM/PolyDiM-core/src/Utilities/GBasis_2D.hpp",
           "./PolyDiM/PolyDiM-core/src/Utilities/GBasis_3D.hpp",
           "./PolyDiM/PolyDiM-core/src/Utilities/GBasis_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/Utilities/Inertia_Utilities.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/1D/FEM_PCC_1D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/1D/FEM_PCC_1D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_PCC_2D_LocalSpace_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_PCC_2D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_PCC_2D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_Quadrilateral_PCC_2D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_Quadrilateral_PCC_2D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_Triangle_PCC_2D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_Triangle_PCC_2D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_Hexahedron_PCC_3D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_Hexahedron_PCC_3D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_PCC_3D_LocalSpace_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_PCC_3D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_PCC_3D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_Tetrahedron_PCC_3D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_Tetrahedron_PCC_3D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/MCC/2D/FEM_MCC_2D_LocalSpace_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/MCC/2D/FEM_MCC_2D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/MCC/2D/FEM_MCC_2D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/MCC/2D/FEM_Triangle_RT_MCC_2D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/FEM/MCC/2D/FEM_Triangle_RT_MCC_2D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Creator.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_LocalSpace_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Pressure_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Reduced_Pressure_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Reduced_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Reduced_Velocity_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Velocity_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Creator.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_LocalSpace_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Pressure_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Reduced_Pressure_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Reduced_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Reduced_Velocity_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Velocity_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/VEM_DF_PCC_Utilities.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Creator.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_EdgeOrtho_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_EdgeOrtho_Velocity_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_LocalSpace_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Ortho_EdgeOrtho_Velocity_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Ortho_Velocity_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Partial_Velocity_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Pressure_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Velocity_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/3D/VEM_MCC_3D_Creator.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/3D/VEM_MCC_3D_LocalSpace_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/3D/VEM_MCC_3D_Pressure_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/3D/VEM_MCC_3D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/3D/VEM_MCC_3D_Velocity_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/MCC/VEM_MCC_Utilities.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_Creator.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_Inertia_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_Ortho_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/I_VEM_PCC_2D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_LocalSpace_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_Creator.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_Inertia_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_Ortho_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_LocalSpace_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/VEM/PCC/VEM_PCC_Utilities.hpp",
           "./PolyDiM/PolyDiM-core/src/ZFEM/PCC/2D/ZFEM_PCC_2D_Creator.hpp",
           "./PolyDiM/PolyDiM-core/src/ZFEM/PCC/2D/ZFEM_PCC_2D_ReferenceElement.hpp",
           "./PolyDiM/PolyDiM-core/src/ZFEM/PCC/2D/ZFEM_PCC_2D_LocalSpace_Data.hpp",
           "./PolyDiM/PolyDiM-core/src/ZFEM/PCC/2D/ZFEM_PCC_2D_LocalSpace.hpp",
           "./PolyDiM/PolyDiM-core/src/ZFEM/PCC/2D/ZFEM_PCC_2D_LocalSpace.cpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/Equations/EllipticEquation.hpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/LocalSpace/LocalSpace_DF_PCC_2D.hpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/LocalSpace/LocalSpace_MCC_2D.hpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/LocalSpace/LocalSpace_PCC_2D.hpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/LocalSpace/LocalSpace_PCC_3D.hpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/Mesh/MeshMatricesDAO_mesh_connectivity_data.hpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/Mesh/PDE_Mesh_Utilities.hpp"
           "./PolyDiM/PolyDiM-core/src/PDETools/DOFs/DOFsManager.hpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/Assembler/assembler_PCC_2D_functions_data.hpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/Assembler/assembler_PCC_2D_functions_utilities.hpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/Assembler/assembler_PCC_2D_functions.hpp",
           "./PolyDiM/PolyDiM-core/src/PDETools/Assembler/Assembler_Utilities.hpp"
            ]

# Stampa a console:
litgen.write_generated_code_for_files(
    options=opts,
    input_cpp_header_files=headers,
    output_cpp_pydef_file="bindings.cpp",
    output_stub_pyi_file="pypolydim.pyi",
)

p = pathlib.Path("./bindings.cpp")   # aggiusta il path
src = p.read_text()

BAD = re.compile(r'(?<!\\)\\(oplus|nabla)')

def fix(line):
    if any(m in line for m in ('\\f$', '@brief', '@param', '@return', 'mathbb', 'mathcal')):
        return BAD.sub(r'\\\\\1', line)
    return line

p.write_text("\n".join(fix(l) for l in src.split("\n")))