# isort: dont-add-import: from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Union, cast

import fsspec

from daft.api_annotations import PublicAPI
from daft.context import get_context
from daft.dataframe import DataFrame
from daft.datasources import ParquetSourceInfo
from daft.datatype import DataType
from daft.io.common import _get_files_scan_rustplan, _get_tabular_files_scan
from daft.logical.logical_plan import LogicalPlan

if TYPE_CHECKING:
    from daft.io import IOConfig


@PublicAPI
def read_parquet(
    path: Union[str, List[str]],
    schema_hints: Optional[Dict[str, DataType]] = None,
    fs: Optional[fsspec.AbstractFileSystem] = None,
    io_config: Optional["IOConfig"] = None,
    use_native_downloader: bool = False,
) -> DataFrame:
    """Creates a DataFrame from Parquet file(s)

    Example:
        >>> df = daft.read_parquet("/path/to/file.parquet")
        >>> df = daft.read_parquet("/path/to/directory")
        >>> df = daft.read_parquet("/path/to/files-*.parquet")
        >>> df = daft.read_parquet("s3://path/to/files-*.parquet")

    Args:
        path (str): Path to Parquet file (allows for wildcards)
        schema_hints (dict[str, DataType]): A mapping between column names and datatypes - passing this option will
            disable all schema inference on data being read, and throw an error if data being read is incompatible.
        fs (fsspec.AbstractFileSystem): fsspec FileSystem to use for reading data.
            By default, Daft will automatically construct a FileSystem instance internally.
        io_config (IOConfig): Config to be used with the native downloader
        use_native_downloader: Whether to use the native downloader instead of PyArrow for reading Parquet. This
            is currently experimental.

    returns:
        DataFrame: parsed DataFrame
    """

    if isinstance(path, list) and len(path) == 0:
        raise ValueError(f"Cannot read DataFrame from from empty list of Parquet filepaths")

    context = get_context()

    if context.use_rust_planner:
        plan = cast(
            LogicalPlan,
            _get_files_scan_rustplan(
                path,
                schema_hints,
                ParquetSourceInfo(
                    io_config=io_config,
                    use_native_downloader=use_native_downloader,
                ),
                fs,
            ),
        )  # Cast for temporary type checking.
    else:
        plan = _get_tabular_files_scan(
            path,
            schema_hints,
            ParquetSourceInfo(
                io_config=io_config,
                use_native_downloader=use_native_downloader,
            ),
            fs,
        )

    return DataFrame(plan)
