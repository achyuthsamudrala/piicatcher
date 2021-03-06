import json
import sys
from argparse import Namespace

from piicatcher.catalog.file import FileStore
from tests.test_models import MockExplorer


def test_file(tmp_path):
    tmp_file = tmp_path / "schema.json"
    explorer = MockExplorer(Namespace(catalog={
        'file': tmp_file,
        'format': 'json'
    },
                                      include_schema=(),
                                      exclude_schema=(),
                                      include_table=(),
                                      exclude_table=()
                                      ))

    explorer._load_catalog()
    FileStore.save_schemas(explorer)
    obj = None
    with open(tmp_file, 'r') as fh:
        obj = json.load(fh)
    assert len(obj) > 0
    assert obj[0]['name'] == 'test_store'
    assert len(obj[0]['tables']) == 3


def test_stdout(capsys):
    explorer = MockExplorer(Namespace(catalog={
        'file': None,
        'format': 'json'
    },
                                      include_schema=(),
                                      exclude_schema=(),
                                      include_table=(),
                                      exclude_table=()
                                      ))

    explorer._load_catalog()

    FileStore.save_schemas(explorer)
    out, err = capsys.readouterr()

    obj = json.loads(out)
    assert len(obj) > 0
    assert obj[0]['name'] == 'test_store'
    assert len(obj[0]['tables']) == 3

