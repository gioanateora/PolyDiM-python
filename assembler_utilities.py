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
            self.do_fs_data_indices: List[polydim.pde_tools.do_fs.DOFsManager.CellsDOFsIndicesData]
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

        lengths = np.array([len(d.cells_global_do_fs[dimension][cell_index]) for d in do_fs_data])
        cum_sum = np.cumsum(lengths)
        data.num_total_do_fs = cum_sum[-1]
        data.offset_do_fs = np.concatenate(([0], cum_sum[:-1])).tolist()

        return data

    @staticmethod
    def global_solution_to_local_solution(dimension: int,
                                          cell_index: int,
                                          do_fs_data_indices: List[polydim.pde_tools.do_fs.DOFsManager.CellsDOFsIndicesData],
                                          count_do_fs: CountDOFsData,
                                          local_count_do_fs: LocalCountDOFsData,
                                          global_solution_do_fs: np.ndarray,
                                          global_solution_strongs: np.ndarray) -> np.ndarray:

        local_solution_do_fs = np.zeros(local_count_do_fs.num_total_do_fs)


        num_dof_handler = len(do_fs_data_indices)
        for h in range(num_dof_handler):

            local_dof_i = np.array(do_fs_data_indices[h].cells_do_fs_local_index[cell_index]) + local_count_do_fs.offset_do_fs[h]
            local_strong_i = np.array(do_fs_data_indices[h].cells_strongs_local_index[cell_index]) + local_count_do_fs.offset_do_fs[h]

            global_dof_i = np.array(do_fs_data_indices[h].cells_do_fs_global_index[cell_index]) + count_do_fs.offset_do_fs[h]
            global_strong_i = np.array(do_fs_data_indices[h].cells_strongs_global_index[cell_index]) + count_do_fs.offset_strongs[h]

            local_solution_do_fs[local_dof_i.tolist()] = global_solution_do_fs[global_dof_i.tolist()]
            local_solution_do_fs[local_strong_i.tolist()] = global_solution_strongs[global_strong_i.tolist()]

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

        for test_f in range(len(test_functions_do_fs_data.do_fs_data_indices)):

            # data
            test_do_fs_data = test_functions_do_fs_data.do_fs_data_indices[test_f]

            # offset
            test_global_offset_do_fs = test_functions_do_fs_data.global_offsets_do_fs[test_f]
            test_local_offset = test_functions_do_fs_data.local_offsets[test_f]

            for trial_f in range(len(trial_functions_do_fs_data.do_fs_data_indices)):

                # data
                trial_do_fs_data = trial_functions_do_fs_data.do_fs_data_indices[trial_f]

                # offset
                trial_global_offset_do_fs = trial_functions_do_fs_data.global_offsets_do_fs[trial_f]
                trial_local_offset = trial_functions_do_fs_data.local_offsets[trial_f]
                trial_global_offset_strongs = trial_functions_do_fs_data.global_offsets_strongs[trial_f]

                # Test slicing indices
                global_dof_i = np.array(test_do_fs_data.cells_do_fs_global_index[cell_index], dtype=np.int64) + test_global_offset_do_fs
                local_dof_i = np.array(test_do_fs_data.cells_do_fs_local_index[cell_index], dtype=np.int64) + test_local_offset

                if local_rhs is not None and global_rhs is not None:
                    global_rhs[global_dof_i] += local_rhs[local_dof_i]

                # Trial slicing indices
                global_dof_j = np.array(trial_do_fs_data.cells_do_fs_global_index[cell_index], dtype=np.int64) + trial_global_offset_do_fs
                local_dof_j = np.array(trial_do_fs_data.cells_do_fs_local_index[cell_index], dtype=np.int64) + trial_local_offset

                global_strong_j = np.array(trial_do_fs_data.cells_strongs_global_index[cell_index], dtype=np.int64) + trial_global_offset_strongs
                local_strong_j = np.array(trial_do_fs_data.cells_strongs_local_index[cell_index], dtype=np.int64) + trial_local_offset

                loc_a_dof_dof = local_lhs[np.ix_(local_dof_i, local_dof_j)].ravel(order='C').tolist()
                global_dof_dof_i = np.repeat(global_dof_i, len(global_dof_j)).tolist()
                global_dof_dof_j = np.tile(global_dof_j, len(global_dof_i)).tolist()

                global_lhs_do_fs.row.extend(global_dof_dof_i)
                global_lhs_do_fs.col.extend(global_dof_dof_j)
                global_lhs_do_fs.data.extend(loc_a_dof_dof)

                if len(local_strong_j) > 0:

                    loc_a_dof_strong = local_lhs[np.ix_(local_dof_i, local_strong_j)].ravel(order='C').tolist()

                    global_dof_strong_i = np.repeat(global_dof_i, len(global_strong_j)).tolist()
                    global_dof_strong_j = np.tile(global_strong_j, len(global_dof_i)).tolist()

                    global_lhs_strongs.row.extend(global_dof_strong_i)
                    global_lhs_strongs.col.extend(global_dof_strong_j)
                    global_lhs_strongs.data.extend(loc_a_dof_strong)

