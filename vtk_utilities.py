import numpy as np
from pyevtk.hl import pointsToVTK, unstructuredGridToVTK
from pyevtk.vtk import VtkPolygon, VtkLine
from pypolydim import gedim
from typing import Dict, Optional, List
import numpy.typing as npt


class VTKUtilities:

    @staticmethod
    def export_cells0_d(path_file: str, mesh: gedim.MeshMatricesDAO, point_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        coordinates = mesh.cell0_ds_coordinates()
        x = np.ascontiguousarray(coordinates[0, :])
        y = np.ascontiguousarray(coordinates[1, :])
        z = np.ascontiguousarray(coordinates[2, :])

        pointsToVTK(path_file, x, y, z, data=point_data)

    @staticmethod
    def export_points(path_file: str, coordinates: np.ndarray, point_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        x = coordinates[0, :]
        y = coordinates[1, :]
        z = coordinates[2, :]

        pointsToVTK(path_file, x, y, z, data=point_data)

    @staticmethod
    def export_cells1_d(path_file: str, mesh: gedim.MeshMatricesDAO, point_data: Optional[Dict[str, np.ndarray]] = None, cell_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        coordinates = mesh.cell0_ds_coordinates()
        x = np.ascontiguousarray(coordinates[0, :])
        y = np.ascontiguousarray(coordinates[1, :])
        z = np.ascontiguousarray(coordinates[2, :])

        # number of 2D cells
        num_cells_1: int = mesh.cell1_d_total_number()

        # Define connectivity or vertices that belongs to each element
        conn: List[int] = []
        # Define offset of last vertex of each element
        offset = np.arange(2, 2 * (num_cells_1 + 1), 2)
        # Define cell types
        cell_type = np.zeros(num_cells_1)

        for e in range(num_cells_1):
            conn.append(mesh.cell1_d_origin(e))
            conn.append(mesh.cell1_d_end(e))
            cell_type[e] = VtkLine.tid

        unstructuredGridToVTK(path_file, x, y, z, connectivity=np.array(conn), offsets=offset,
                              cell_types=cell_type, cellData=cell_data, pointData=point_data)

    @staticmethod
    def export_segments(path_file: str, coordinates: npt.NDArray[np.dtype[np.float64]],
                        segments: npt.NDArray[np.dtype[np.int64]],
                        point_data: Optional[Dict[str, np.ndarray]] = None,
                        cell_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        """
        - segments: 2 x num_segments: first row: origin, second row: end
        """

        x = np.ascontiguousarray(coordinates[0, :])
        y = np.ascontiguousarray(coordinates[1, :])
        z = np.ascontiguousarray(coordinates[2, :])

        # number of 2D cells
        num_cells_1: int = segments.shape[1]

        # Define connectivity or vertices that belongs to each element
        conn: List[int] = []
        # Define offset of last vertex of each element
        offset = np.arange(2, 2 * (num_cells_1 + 1), 2)
        # Define cell types
        cell_type = np.zeros(num_cells_1)

        for e in range(num_cells_1):
            conn.append(int(segments[0, e]))
            conn.append(int(segments[1, e]))
            cell_type[e] = VtkLine.tid

        unstructuredGridToVTK(path_file, x, y, z, connectivity=np.array(conn), offsets=offset,
                              cell_types=cell_type, cellData=cell_data, pointData=point_data)


    @staticmethod
    def export_cells2_d(path_file: str, mesh: gedim.MeshMatricesDAO,
                       point_data: Optional[Dict[str, np.ndarray]] = None,
                       cell_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        coordinates = mesh.cell0_ds_coordinates()
        x = np.ascontiguousarray(coordinates[0, :])
        y = np.ascontiguousarray(coordinates[1, :])
        z = np.ascontiguousarray(coordinates[2, :])

        # number of 2D cells
        num_cells_2: int = mesh.cell2_d_total_number()

        # Define connectivity or vertices that belongs to each element
        conn: List[int] = []
        # Define offset of last vertex of each element
        offset = np.zeros(num_cells_2)
        # Define cell types
        cell_type = np.zeros(num_cells_2)

        count: int = 0
        for c in range(num_cells_2):
            for v in range(mesh.cell2_d_number_vertices(c)):
                conn.append(mesh.cell2_d_vertex(c, v))
            count += mesh.cell2_d_number_vertices(c)
            offset[c] = count
            cell_type[c] = VtkPolygon.tid

        unstructuredGridToVTK(path_file, x, y, z, connectivity=np.array(conn), offsets=offset,
                              cell_types=cell_type, cellData=cell_data, pointData=point_data)


    def export_mesh(self, path_file: str,
                    mesh: gedim.MeshMatricesDAO) -> None:

        dimension = mesh.dimension()


        pt = np.arange(mesh.cell0_d_total_number(), dtype=np.int64)
        mt = np.array(mesh.cell0_ds_marker())
        point_data = {"Id": pt, "Marker": mt}

        self.export_cells0_d(path_file + "/Cells0D", mesh, point_data)

        if dimension >= 1:

            pt = np.arange(mesh.cell1_d_total_number(), dtype=np.int64)
            mt = np.array(mesh.cell1_ds_marker())
            edge_data = {"Id": pt, "Marker": mt}
            self.export_cells1_d(path_file + "/Cells1D", mesh, point_data, edge_data)

        if dimension >= 2:
            pt = np.arange(mesh.cell2_d_total_number(), dtype=np.int64)
            mt = np.array(mesh.cell2_ds_marker())
            cell_data = {"Id": pt, "Marker": mt}
            self.export_cells2_d(path_file + "/Cells2D", mesh, point_data, cell_data)

        if dimension >= 3:
            raise ValueError("not valid dimension")



    def export_solution(self,
                        path_file: str,
                        mesh: gedim.MeshMatricesDAO,
                        cell0_d_numeric_solution: np.ndarray,
                        cell0_d_exact_solution: Optional[np.ndarray] = None,
                        cell_data: Optional[Dict[str, np.ndarray]] = None) -> None:

        if cell0_d_exact_solution is None:
            point_data = {"Numeric": cell0_d_numeric_solution}
        else:
            point_data = {"Numeric": cell0_d_numeric_solution, "Exact": cell0_d_exact_solution}

        self.export_cells2_d(path_file, mesh, point_data, cell_data)

