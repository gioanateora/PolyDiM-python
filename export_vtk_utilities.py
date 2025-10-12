import numpy as np
from pypolydim import gedim
from typing import Dict, Optional, List
import numpy.typing as npt
from pypolydim.vtk_utilities import VTPProperty, VTKUtilities


class ExportVTKUtilities:

    @staticmethod
    def export_points(path_file: str, coordinates: np.ndarray,
                      point_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        properties: List[VTPProperty] = []
        for (key, value) in point_data.items():
            property = VTPProperty()
            property.label = key
            property.data = value
            property.size = len(value)
            property.format = VTPProperty.Formats.Cells
            properties.append(property)

        vtk_utils = VTKUtilities()
        vtk_utils.add_points(coordinates, properties)
        vtk_utils.export(path_file)

    def export_cells0_d(self, path_file: str, mesh: gedim.MeshMatricesDAO,
                        point_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        coordinates = mesh.cell0_ds_coordinates()
        self.export_points(path_file, coordinates, point_data)

    @staticmethod
    def export_segments(path_file: str, coordinates: npt.NDArray[np.dtype[np.float64]],
                        segments: npt.NDArray[np.dtype[np.int64]],
                        point_data: Optional[Dict[str, np.ndarray]] = None,
                        cell_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        properties: List[VTPProperty] = []
        for (key, value) in point_data.items():
            property = VTPProperty()
            property.label = key
            property.data = value
            property.size = len(value)
            property.format = VTPProperty.Formats.Points
            properties.append(property)

        for (key, value) in cell_data.items():
            property = VTPProperty()
            property.label = key
            property.data = value
            property.size = len(value)
            property.format = VTPProperty.Formats.Cells
            properties.append(property)

        vtk_utils = VTKUtilities()
        vtk_utils.add_segments(coordinates, segments, properties)
        vtk_utils.export(path_file)

    def export_cells1_d(self, path_file: str, mesh: gedim.MeshMatricesDAO,
                        point_data: Optional[Dict[str, np.ndarray]] = None,
                        cell_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        coordinates = mesh.cell0_ds_coordinates()
        segments = mesh.cell1_ds_extremes()

        self.export_segments(path_file, coordinates, segments, point_data, cell_data)

    def export_polygons(self, path_file: str, coordinates: npt.NDArray[np.dtype[np.float64]],
                        polygons: List[List[int]],
                        point_data: Optional[Dict[str, np.ndarray]] = None,
                        cell_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        properties: List[VTPProperty] = []
        for (key, value) in point_data.items():
            property = VTPProperty()
            property.label = key
            property.data = value
            property.size = len(value)
            property.format = VTPProperty.Formats.Points
            properties.append(property)

        for (key, value) in cell_data.items():
            property = VTPProperty()
            property.label = key
            property.data = value
            property.size = len(value)
            property.format = VTPProperty.Formats.Cells
            properties.append(property)

        vtk_utils = VTKUtilities()
        vtk_utils.add_polygons(coordinates, polygons, properties)
        vtk_utils.export(path_file)

    def export_cells2_d(self, path_file: str, mesh: gedim.MeshMatricesDAO,
                        point_data: Optional[Dict[str, np.ndarray]] = None,
                        cell_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        coordinates = mesh.cell0_ds_coordinates()
        polygons = mesh.cell2_ds_vertices()

        self.export_polygons(path_file, coordinates, polygons, point_data, cell_data)

    @staticmethod
    def export_polyhedrons(path_file: str, coordinates: npt.NDArray[np.dtype[np.float64]],
                           polyhedrons_faces: List[List[List[int]]],
                           point_data: Optional[Dict[str, np.ndarray]] = None,
                           cell_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        properties: List[VTPProperty] = []
        for (key, value) in point_data.items():
            property = VTPProperty()
            property.label = key
            property.data = value
            property.size = len(value)
            property.format = VTPProperty.Formats.Points
            properties.append(property)

        for (key, value) in cell_data.items():
            property = VTPProperty()
            property.label = key
            property.data = value
            property.size = len(value)
            property.format = VTPProperty.Formats.Cells
            properties.append(property)

        vtk_utils = VTKUtilities()
        vtk_utils.add_polyhedrons(coordinates, polyhedrons_faces, properties)
        vtk_utils.export(path_file)

    def export_cells3_d(self, path_file: str, mesh: gedim.MeshMatricesDAO,
                        point_data: Optional[Dict[str, np.ndarray]] = None,
                        cell_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        coordinates = mesh.cell0_ds_coordinates()
        polyhedrons_faces = mesh.cell3_ds_faces_vertices()

        self.export_polyhedrons(path_file, coordinates, polyhedrons_faces, point_data, cell_data)

    def export_mesh(self, path_file: str,
                    mesh: gedim.MeshMatricesDAO) -> None:

        dimension = mesh.dimension()

        pt = np.arange(mesh.cell0_d_total_number(), dtype=np.int64)
        mt = np.array(mesh.cell0_ds_marker(), dtype=np.int64)
        act = np.array(mesh.cell0_ds_state(), dtype=np.int64)
        point_data = {"Id": pt, "Marker": mt, "Active": act}

        self.export_cells0_d(path_file + "/Cells0D.vtu", mesh, point_data)

        if dimension >= 1:
            pt = np.arange(mesh.cell1_d_total_number(), dtype=np.int64)
            mt = np.array(mesh.cell1_ds_marker(), dtype=np.int64)
            act = np.array(mesh.cell1_ds_state(), dtype=np.int64)
            edge_data = {"Id": pt, "Marker": mt, "Active": act}
            self.export_cells1_d(path_file + "/Cells1D.vtu", mesh, point_data, edge_data)

        if dimension >= 2:
            pt = np.arange(mesh.cell2_d_total_number(), dtype=np.int64)
            mt = np.array(mesh.cell2_ds_marker(), dtype=np.int64)
            act = np.array(mesh.cell2_ds_state(), dtype=np.int64)
            cell_data = {"Id": pt, "Marker": mt, "Active": act}
            self.export_cells2_d(path_file + "/Cells2D.vtu", mesh, point_data, cell_data)

        if dimension == 3:
            pt = np.arange(mesh.cell3_d_total_number(), dtype=np.int64)
            mt = np.array(mesh.cell3_ds_marker(), dtype=np.int64)
            act = np.array(mesh.cell3_ds_state(), dtype=np.int64)
            cell_data = {"Id": pt, "Marker": mt, "Active": act}
            self.export_cells3_d(path_file + "/Cells3D.vtu", mesh, point_data, cell_data)

        if dimension > 3:
            raise ValueError("not valid dimension")

    def export_solution_2(self,
                          path_file: str,
                          mesh: gedim.MeshMatricesDAO,
                          cell0_d_numeric_solution: np.ndarray,
                          cell0_d_exact_solution: Optional[np.ndarray] = None,
                          cell2_ds_error_l2: Optional[np.ndarray] = None,
                          cell2_ds_error_h1: Optional[np.ndarray] = None) -> None:

        if cell0_d_exact_solution is None:
            point_data = {"Numeric": cell0_d_numeric_solution}
            cell_data = {}
        else:
            point_data = {"Numeric": cell0_d_numeric_solution, "Exact": cell0_d_exact_solution}
            cell_data = {"Error L2": cell2_ds_error_l2, "Error H1": cell2_ds_error_h1}

        self.export_cells2_d(path_file + ".vtu", mesh, point_data, cell_data)

    def export_solution_3(self,
                          path_file: str,
                          mesh: gedim.MeshMatricesDAO,
                          cell0_d_numeric_solution: np.ndarray,
                          cell0_d_exact_solution: Optional[np.ndarray] = None,
                          cell3_ds_error_l2: Optional[np.ndarray] = None,
                          cell3_ds_error_h1: Optional[np.ndarray] = None) -> None:

        if cell0_d_exact_solution is None:
            point_data = {"Numeric": cell0_d_numeric_solution}
            cell_data = {}
        else:
            point_data = {"Numeric": cell0_d_numeric_solution, "Exact": cell0_d_exact_solution}
            cell_data = {"Error L2": cell3_ds_error_l2, "Error H1": cell3_ds_error_h1}

        self.export_cells3_d(path_file + ".vtu", mesh, point_data, cell_data)

