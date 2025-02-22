# isort: dont-add-import: from __future__ import annotations

from typing import Dict, List, Optional, Union

import fsspec

from daft.api_annotations import PublicAPI
from daft.dataframe import DataFrame
from daft.datasources import CSVSourceInfo
from daft.datatype import DataType
from daft.io.common import _get_tabular_files_scan


@PublicAPI
def read_csv(
    path: Union[str, List[str]],
    schema_hints: Optional[Dict[str, DataType]] = None,
    fs: Optional[fsspec.AbstractFileSystem] = None,
    has_headers: bool = True,
    column_names: Optional[List[str]] = None,
    delimiter: str = ",",
) -> DataFrame:
    """Creates a DataFrame from CSV file(s)

    Example:
        >>> df = daft.read_csv("/path/to/file.csv")
        >>> df = daft.read_csv("/path/to/directory")
        >>> df = daft.read_csv("/path/to/files-*.csv")
        >>> df = daft.read_csv("s3://path/to/files-*.csv")

    Args:
        path (str): Path to CSV (allows for wildcards)
        schema_hints (dict[str, DataType]): A mapping between column names and datatypes - passing this option will
            disable all schema inference on data being read, and throw an error if data being read is incompatible.
        fs (fsspec.AbstractFileSystem): fsspec FileSystem to use for reading data.
            By default, Daft will automatically construct a FileSystem instance internally.
        has_headers (bool): Whether the CSV has a header or not, defaults to True
        delimiter (Str): Delimiter used in the CSV, defaults to ","

    returns:
        DataFrame: parsed DataFrame
    """
    if column_names is not None:
        raise NotImplementedError(
            "The `column_names` option has been deprecated. As an alternative, you may specify `has_headers=False` which will have Daft "
            "autogenerate your column names. Then, you can use `df.select` to alias each of the autogenerated columns: "
            "`df.select(*[col(old).alias(new) for old, new in zip(df.column_names, MY_COL_NAMES)])`. Please submit an issue if this is a "
            "blocker for your workflow!"
        )
    if isinstance(path, list) and len(path) == 0:
        raise ValueError(f"Cannot read DataFrame from from empty list of CSV filepaths")

    plan = _get_tabular_files_scan(
        path,
        schema_hints,
        CSVSourceInfo(
            delimiter=delimiter,
            has_headers=has_headers,
        ),
        fs,
    )
    return DataFrame(plan)
