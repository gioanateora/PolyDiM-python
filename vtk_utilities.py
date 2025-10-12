import numpy as np
import vtk
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkCellArray
from typing import List
from enum import Enum
from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkPoints
)
from vtkmodules.vtkCommonDataModel import (
    VTK_POLYHEDRON,
    vtkUnstructuredGrid
)
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter


class VTPPoints:

    def __init__(self, points: np.ndarray):
        self.points = points


class VTPSegments:

    def __init__(self, vertices: np.ndarray, edges: np.ndarray):
        self.vertices = vertices
        self.edges = edges


class VTPPolygons:

    def __init__(self, vertices: np.ndarray, polygons: List[List[int]]):
        self.vertices = vertices
        self.polygons = polygons


class VTPPolyhedrons:

    def __init__(self, vertices: np.ndarray, polyhedrons_faces: List[List[List[int]]]):
        self.vertices = vertices
        self.polyhedrons_faces = polyhedrons_faces


class VTPProperty:
    class Formats(Enum):
        Points = 0
        Cells = 1
        PointsArray = 2
        CellsArray = 3
        PointsArray2 = 4

    label: str
    format: Formats
    size: int
    data: np.ndarray


class GeometryToPolyData:

    def __init__(self, geometry, properties: List[VTPProperty]):
        self.geometry = geometry
        self.properties = properties

    @staticmethod
    def add_points(points: np.ndarray):
        vtk_points = vtk.vtkPoints()
        vtk_points.Allocate(points.shape[1])
        for p in range(points.shape[1]):
            vtk_points.InsertNextPoint(float(points[0, p]), float(points[1, p]), float(points[2, p]))

        return vtk_points

    @staticmethod
    def add_vertices(points_id: List[int]):
        vtk_cells = vtk.vtkCellArray()
        vtk_cells.Allocate(len(points_id))
        for pid in points_id:
            vtk_cells.InsertNextCell(1)
            vtk_cells.InsertCellPoint(pid)

        return vtk_cells

    @staticmethod
    def add_lines(edges: np.ndarray):

        lines = vtk.vtkCellArray()
        num_edges = edges.shape[1]
        lines.Allocate(num_edges)

        for l in range(num_edges):
            lines.InsertNextCell(2)
            lines.InsertCellPoint(int(edges[0, l]))
            lines.InsertCellPoint(int(edges[1, l]))

        return lines

    @staticmethod
    def add_polygons(faces_vertices_ids: List[List[int]]):
        faces = vtkCellArray()
        faces.Allocate(len(faces_vertices_ids))
        for f in range(len(faces_vertices_ids)):
            faces.InsertNextCell(len(faces_vertices_ids[f]))

            for v in faces_vertices_ids[f]:
                faces.InsertCellPoint(v)

        return faces

    def append_solution(self, poly_data: vtk.vtkDataSet):

        for s in range(len(self.properties)):

            vtk_solution = vtkDoubleArray()
            vtk_solution.SetName(self.properties[s].label)

            match self.properties[s].format:
                case VTPProperty.Formats.Points:
                    poly_data.GetPointData().AddArray(vtk_solution)

                    if s == 0:
                        poly_data.GetPointData().SetActiveScalars(self.properties[s].label)

                    vtk_solution.SetNumberOfValues(self.properties[s].size)

                    for p in range(self.properties[s].size):
                        vtk_solution.SetValue(p, self.properties[s].data[p])

                    pass
                case VTPProperty.Formats.Cells:
                    poly_data.GetCellData().AddArray(vtk_solution)

                    if s == 0:
                        poly_data.GetCellData().SetActiveScalars(self.properties[s].label)

                    vtk_solution.SetNumberOfValues(self.properties[s].size)

                    for p in range(self.properties[s].size):
                        vtk_solution.SetValue(p, self.properties[s].data[p])

                    pass
                case VTPProperty.Formats.PointsArray2:
                    poly_data.GetPointData().AddArray(vtk_solution)

                    vtk_solution.SetNumberOfComponents(2)

                    if s == 0:
                        poly_data.GetPointData().SetActiveScalars(self.properties[s].label)

                    num_tuples = self.properties[s].size / 2
                    vtk_solution.SetNumberOfTuples(num_tuples)
                    for p in range(num_tuples):
                        vtk_solution.SetTuple2(p, self.properties[s].data[3 * p],
                                               self.properties[s].data[3 * p + 1])

                    pass
                case VTPProperty.Formats.PointsArray:
                    poly_data.GetPointData().AddArray(vtk_solution)

                    vtk_solution.SetNumberOfComponents(3)

                    if s == 0:
                        poly_data.GetPointData().SetActiveScalars(self.properties[s].label)

                    num_tuples = self.properties[s].size / 3
                    vtk_solution.SetNumberOfTuples(num_tuples)
                    for p in range(num_tuples):
                        vtk_solution.SetTuple3(p, self.properties[s].data[3 * p],
                                               self.properties[s].data[3 * p + 1],
                                               self.properties[s].data[3 * p + 2])

                    pass
                case VTPProperty.Formats.CellsArray:
                    poly_data.GetCellData().AddArray(vtk_solution)

                    vtk_solution.SetNumberOfComponents(3)

                    if s == 0:
                        poly_data.GetCellData().SetActiveScalars(self.properties[s].label)

                    num_tuples = self.properties[s].size / 3
                    vtk_solution.SetNumberOfTuples(num_tuples)
                    for p in range(num_tuples):
                        vtk_solution.SetTuple3(p, self.properties[s].data[3 * p], self.properties[s].data[3 * p + 1],
                                               self.properties[s].data[3 * p + 2])

                    pass
                case _:
                    raise ValueError("Solution format not supported")

    def convert_points(self):

        export_data = vtk.vtkAppendFilter()

        num_total_points: int = self.geometry.points.shape[1]

        points = self.add_points(self.geometry.points)
        vertices = self.add_vertices(np.arange(0, num_total_points).tolist())

        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(points)
        poly_data.SetVerts(vertices)

        self.append_solution(poly_data)

        export_data.AddInputData(poly_data)

        return export_data, poly_data

    def convert_segments(self):

        export_data = vtk.vtkAppendFilter()

        points = self.add_points(self.geometry.vertices)
        lines = self.add_lines(self.geometry.edges)

        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(points)
        poly_data.SetLines(lines)

        self.append_solution(poly_data)

        export_data.AddInputData(poly_data)

        return export_data, poly_data

    def convert_polygons(self):

        export_data = vtk.vtkAppendFilter()

        points = self.add_points(self.geometry.vertices)
        faces = self.add_polygons(self.geometry.polygons)

        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(points)
        poly_data.SetPolys(faces)

        self.append_solution(poly_data)

        export_data.AddInputData(poly_data)

        return export_data, poly_data

    def convert_polyhedrons(self):

        export_data = vtk.vtkAppendFilter()

        ugrid = vtkUnstructuredGrid()
        points = self.add_points(self.geometry.vertices)

        ugrid.SetPoints(points)

        for p in range(len(self.geometry.polyhedrons_faces)):
            faces = self.geometry.polyhedrons_faces[p]
            faceId = vtkIdList()
            faceId.InsertNextId(len(faces))
            for face in faces:
                faceId.InsertNextId(len(face))  # The number of points in the face.
                [faceId.InsertNextId(i) for i in face]

            ugrid.InsertNextCell(VTK_POLYHEDRON, faceId)

        self.append_solution(ugrid)
        export_data.AddInputData(ugrid)

        return export_data, ugrid


class VTKUtilities:
    class ExportFormats(Enum):
        Binary = 0
        Ascii = 1
        Appended = 2

    def __init__(self):

        self.export_data = vtk.vtkAppendFilter()
        self.poly_data = vtk.vtkPolyData()

    def add_points(self, points: np.ndarray, properties: List[VTPProperty] = []):
        vtp_points = VTPPoints(points)
        geometry = GeometryToPolyData(vtp_points, properties)

        self.export_data, self.poly_data = geometry.convert_points()

    def add_segments(self, vertices: np.ndarray, edges: np.ndarray, properties: List[VTPProperty] = []):
        vtp_segments = VTPSegments(vertices, edges)
        geometry = GeometryToPolyData(vtp_segments, properties)

        self.export_data, self.poly_data = geometry.convert_segments()

    def add_polygons(self, vertices: np.ndarray, polygons: List[List[int]], properties: List[VTPProperty] = []):
        vtp_polygons = VTPPolygons(vertices, polygons)
        geometry = GeometryToPolyData(vtp_polygons, properties)

        self.export_data, self.poly_data = geometry.convert_polygons()

    def add_polyhedrons(self, vertices: np.ndarray, polyhedrons: List[List[List[int]]],
                        properties: List[VTPProperty] = []):
        vtp_polyhedrons = VTPPolyhedrons(vertices, polyhedrons)
        geometry = GeometryToPolyData(vtp_polyhedrons, properties)

        self.export_data, self.poly_data = geometry.convert_polyhedrons()

    def export(self, filepath: str, mode: ExportFormats = ExportFormats.Binary):

        self.export_data.Update()

        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetFileName(filepath)
        uot = self.export_data.GetOutput()
        writer.SetInputData(self.export_data.GetOutput())

        match mode:
            case self.ExportFormats.Binary:
                writer.SetDataModeToBinary()
            case self.ExportFormats.Ascii:
                writer.SetDataModeToAscii()
            case self.ExportFormats.Appended:
                writer.SetDataModeToAppended()
            case _:
                raise ValueError("Export Format not supported")

        writer.Write()
