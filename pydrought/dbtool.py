from sqlalchemy.engine import URL
from sqlalchemy import create_engine

from pangres import upsert

import pandas as pd
import pandas.io.sql as sqlio
from multiprocessing import Lock

from pydrought.procedure_management import stream_log
from pydrought.drought_db_management import Info4img, GrdDataManager4ora
from pydrought.models import (
    DbCredentials,
    RasterDataMatrix,
    DataIngestionConstants,
    UpsertIfRowExists,
)


class DbTool:
    def __init__(self, db_secrets: DbCredentials, debug: bool = False):
        self.db_str = URL.create(**db_secrets.dict())
        self.engine = create_engine(self.db_str, echo=debug)

    def set_info_adapted(self, gdmngr: GrdDataManager4ora, info: Info4img):
        self.gdmngr = gdmngr
        self.info = info
        self.info_adapted = gdmngr.info.match(info)

    def extract_grid_df(self) -> pd.DataFrame:
        grid_sql = f"SELECT ID, XCOL, YROW FROM {self.gdmngr.master_tbl_name} WHERE "
        grid_sql += f"xcol BETWEEN {self.info_adapted.range_cols[0]} AND {self.info_adapted.range_cols[1]} "
        grid_sql += f"AND yrow BETWEEN {self.info_adapted.range_rows[0]} AND {self.info_adapted.range_rows[1]}"
        return sqlio.read_sql_query(grid_sql, self.engine)

    def create_mtrxs_df(self, mtrxs: list[RasterDataMatrix]) -> pd.DataFrame:
        data_var_names = [m.var_name for m in mtrxs]
        data = {"xcol": [], "yrow": [], **{var_name: [] for var_name in data_var_names}}

        rows, cols = mtrxs[0].array.shape

        for row in range(rows):
            yrow = row + self.info_adapted.range_rows[0]
            for col in range(cols):
                xcol = col + self.info_adapted.range_cols[0]
                for mtrx in mtrxs:
                    data[mtrx.var_name].append(mtrx.array[row][col])
                data["xcol"].append(xcol)
                data["yrow"].append(yrow)
        return pd.DataFrame(data)

    def merge_grid_and_mtrxs_df(
        self,
        grid_df: pd.DataFrame,
        mtrxs_df: pd.DataFrame,
        constants: DataIngestionConstants,
        on_vars: list[str] = ["xcol", "yrow"],
    ) -> pd.DataFrame:
        colnames = {
            "id": self.gdmngr.fkey.lower(),
            **{vmap.variable_name: vmap.column_name for vmap in constants.vars_mapping},
        }
        df = (
            mtrxs_df.merge(grid_df, on=on_vars)
            .drop(on_vars, axis=1)
            .rename(columns=colnames)
        )
        index_cols = [self.gdmngr.fkey.lower()]
        for const in constants.regex_constants:
            df[const.variable_name] = const.value
            index_cols.append(const.variable_name)
        return df.set_index(index_cols)

    def upsert_copy_update(
        self,
        df: pd.DataFrame,
        if_row_exists: UpsertIfRowExists = UpsertIfRowExists.update.value,
        chunksize: int = 100000,
    ):
        upsert(
            con=self.engine,
            df=df,
            table_name=self.gdmngr.tabs2use.name.lower(),
            if_row_exists=if_row_exists,
            chunksize=chunksize,
        )

    def process_raster_data(
        self,
        info: Info4img,
        gdmngr: GrdDataManager4ora,
        mtrxs: list[RasterDataMatrix],
        constants: DataIngestionConstants,
        lock: Lock
    ):
        stream_log(f"Processing raster data with constants {constants.dict()}")
        self.set_info_adapted(info=info, gdmngr=gdmngr)
        grid_df = self.extract_grid_df()
        mtrxs_df = self.create_mtrxs_df(mtrxs=mtrxs)
        merged_df = self.merge_grid_and_mtrxs_df(
            grid_df=grid_df, mtrxs_df=mtrxs_df, constants=constants
        )
        self.upsert_copy_update(df=merged_df)
