import numpy as np
from scipy.sparse import coo_array
from typing import List, Optional
from pypolydim import polydim

class assembler_utilities:

    class SparseMatrix:

        def __init__(self):
            self.row: List[int] = []
            self.col: List[int] = []
            self.data: List[float] = []

        def create(self, num_rows, num_cols) -> coo_array:
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_array.html#scipy.sparse.coo_array
            # https://caam37830.github.io/book/02_linear_algebra/sparse_linalg.html
            return coo_array((self.data, (self.row, self.col)), shape=(num_rows, num_cols))

    class LocalMatrixToGlobalMatrixDOFsData:

        def __init__(self) -> None:
            self.do_fs_data: List[polydim.pde_tools.do_fs.DOFsManager.DOFsData]
            self.local_offsets: List[int] = []
            self.global_offsets_do_fs: List[int] = []
            self.global_offsets_strongs: List[int] = []

    class CountDOFsData:

        def __init__(self) -> None:
            self.num_total_boundary_do_fs: int = 0
            self.num_total_do_fs: int = 0
            self.num_total_strongs: int = 0
            self.offset_do_fs: List[int] = []
            self.offset_strongs: List[int] = []

    class LocalCountDOFsData:

        def __init__(self) -> None:
            self.num_total_do_fs: int = 0
            self.offset_do_fs: List[int] = []

    def count_do_fs(self, do_fs_data: List[polydim.pde_tools.do_fs.DOFsManager.DOFsData]) -> CountDOFsData:

        data = self.CountDOFsData()
        data.num_total_do_fs = do_fs_data[0].number_do_fs
        data.num_total_strongs = do_fs_data[0].number_strongs
        data.num_total_boundary_do_fs = do_fs_data[0].number_boundary_do_fs

        num_dof_handler = len(do_fs_data)
        data.offset_do_fs.append(0)
        data.offset_strongs.append(0)

        for h in range(num_dof_handler - 1):
            data.num_total_do_fs += do_fs_data[h + 1].number_do_fs
            data.num_total_strongs += do_fs_data[h + 1].number_strongs
            data.num_total_boundary_do_fs += do_fs_data[h + 1].number_boundary_do_fs

            data.offset_do_fs.append(data.offset_do_fs[h] + do_fs_data[h].number_do_fs)
            data.offset_strongs.append(data.offset_strongs[h] + do_fs_data[h].number_strongs)

        return data

    def local_count_do_fs(self, dimension: int, cell_index: int,
                          do_fs_data: List[polydim.pde_tools.do_fs.DOFsManager.DOFsData]) -> LocalCountDOFsData:

        data = self.LocalCountDOFsData()
        data.num_total_do_fs = len(do_fs_data[0].cells_global_do_fs[dimension][cell_index])

        num_dof_handler = len(do_fs_data)
        data.offset_do_fs.append(0)

        for h in range(num_dof_handler - 1):
            data.num_total_do_fs += len(do_fs_data[h + 1].cells_global_do_fs[dimension][cell_index])
            data.offset_do_fs.append(
                data.offset_do_fs[h] + len(do_fs_data[h].cells_global_do_fs[dimension][cell_index]))

        return data

    @staticmethod
    def global_solution_to_local_solution(dimension: int,
                                          cell_index: int,
                                          do_fs_data: List[polydim.pde_tools.do_fs.DOFsManager.DOFsData],
                                          count_do_fs: CountDOFsData,
                                          local_count_do_fs: LocalCountDOFsData,
                                          global_solution_do_fs: np.ndarray,
                                          global_solution_strongs: np.ndarray) -> np.ndarray:

        local_solution_do_fs = np.zeros(local_count_do_fs.num_total_do_fs)

        num_dof_handler = len(do_fs_data)
        for h in range(num_dof_handler):

            do_fs = do_fs_data[h]
            global_dof = do_fs.cells_global_do_fs[dimension][cell_index]

            for loc_i in range(len(global_dof)):

                global_dof_i = global_dof[loc_i]
                local_dof_i = do_fs.cells_do_fs[global_dof_i.dimension][global_dof_i.cell_index][
                    global_dof_i.dof_index]

                match local_dof_i.type:
                    case polydim.pde_tools.do_fs.DOFsManager.DOFsData.DOF.Types.strong:
                        local_solution_do_fs[loc_i + local_count_do_fs.offset_do_fs[h]] = \
                        global_solution_strongs[local_dof_i.global_index + count_do_fs.offset_strongs[h]]
                    case polydim.pde_tools.do_fs.DOFsManager.DOFsData.DOF.Types.dof:
                        local_solution_do_fs[loc_i + local_count_do_fs.offset_do_fs[h]] = global_solution_do_fs[
                            local_dof_i.global_index + count_do_fs.offset_do_fs[h]]
                    case _:
                        raise ValueError("unknown DOF type")

        return local_solution_do_fs

    @staticmethod
    def assemble_local_matrix_to_global_matrix(dimension: int,
                                               cell_index: int,
                                               test_functions_do_fs_data: LocalMatrixToGlobalMatrixDOFsData,
                                               trial_functions_do_fs_data: LocalMatrixToGlobalMatrixDOFsData,
                                               local_lhs: np.ndarray,
                                               global_lhs_do_fs: SparseMatrix,
                                               global_lhs_strongs: SparseMatrix,
                                               local_rhs: Optional[np.ndarray] = None,
                                               global_rhs: Optional[np.ndarray] = None) -> None:

        for test_f in range(len(test_functions_do_fs_data.do_fs_data)):

            test_do_fs_data = test_functions_do_fs_data.do_fs_data[test_f]
            test_global_do_fs = test_do_fs_data.cells_global_do_fs[dimension][cell_index]
            test_global_offset_do_fs = test_functions_do_fs_data.global_offsets_do_fs[test_f]
            test_local_offset = test_functions_do_fs_data.local_offsets[test_f]

            for test_loc_i in range(len(test_global_do_fs)):

                global_dof_i = test_global_do_fs[test_loc_i]
                local_dof_i = test_do_fs_data.cells_do_fs[global_dof_i.dimension][global_dof_i.cell_index][global_dof_i.dof_index]

                match local_dof_i.type:
                    case polydim.pde_tools.do_fs.DOFsManager.DOFsData.DOF.Types.strong:
                        continue
                    case polydim.pde_tools.do_fs.DOFsManager.DOFsData.DOF.Types.dof:
                        pass
                    case _:
                        raise ValueError("Unknown DOF Type")

                global_index_i = local_dof_i.global_index + test_global_offset_do_fs

                if local_rhs is not None and global_rhs is not None:
                    global_rhs[global_index_i] = local_rhs[test_loc_i + test_local_offset]

                for trial_f in range(len(trial_functions_do_fs_data.do_fs_data)):
                    trial_do_fs_data = trial_functions_do_fs_data.do_fs_data[trial_f]
                    trial_global_do_fs = trial_do_fs_data.cells_global_do_fs[dimension][cell_index]
                    trial_global_offset_do_fs = trial_functions_do_fs_data.global_offsets_do_fs[trial_f]
                    trial_local_offset = trial_functions_do_fs_data.local_offsets[trial_f]
                    trial_global_offset_strongs = trial_functions_do_fs_data.global_offsets_strongs[trial_f]

                    for trial_loc_j in range(len(trial_global_do_fs)):
                        global_dof_j = trial_global_do_fs[trial_loc_j]
                        local_dof_j = \
                        trial_do_fs_data.cells_do_fs[global_dof_j.dimension][global_dof_j.cell_index][
                            global_dof_j.dof_index]

                        global_index_j = local_dof_j.global_index
                        loc_a_element = local_lhs[
                            test_loc_i + test_local_offset, trial_loc_j + trial_local_offset]

                        match local_dof_j.type:
                            case polydim.pde_tools.do_fs.DOFsManager.DOFsData.DOF.Types.strong:
                                global_lhs_strongs.row.append(global_index_i)
                                global_lhs_strongs.col.append(global_index_j + trial_global_offset_strongs)
                                global_lhs_strongs.data.append(loc_a_element)
                                pass
                            case polydim.pde_tools.do_fs.DOFsManager.DOFsData.DOF.Types.dof:
                                global_lhs_do_fs.row.append(global_index_i)
                                global_lhs_do_fs.col.append(global_index_j + trial_global_offset_do_fs)
                                global_lhs_do_fs.data.append(loc_a_element)
                                pass
                            case _:
                                raise ValueError("Unknown DOF Type")