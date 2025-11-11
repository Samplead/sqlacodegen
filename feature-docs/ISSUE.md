I run the tests in `test_str_enum_flag.py`. Except from `test_without_use_str_enums_flag`, all the other tests failed. Here is the pytest output:

```
FAILED tests/test_str_enum_flag.py::test_single_enum_column[generator0] - assert "from enum im...'pending'))\n" == 'from enum im...umn(String)\n'
FAILED tests/test_str_enum_flag.py::test_multiple_enum_columns_same_table[generator0] - assert "from enum im...inactive'))\n" == 'from enum im...umn(String)\n'
FAILED tests/test_str_enum_flag.py::test_shared_enum_across_tables[generator0] - assert "from enum im...'pending'))\n" == 'from enum im...umn(String)\n'
FAILED tests/test_str_enum_flag.py::test_nullable_enum_column[generator0] - assert "from enum im...inactive'))\n" == 'from enum im...umn(String)\n'
```