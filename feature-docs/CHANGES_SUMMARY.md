# Summary of Changes for StrEnum Feature

## Files Modified

### 1. `src/sqlacodegen/generators.py`
- **10 patches/modifications** to the `DeclarativeGenerator` class
- **5 new methods** added
- **3 methods overridden** from parent class
- **~184 lines of code added** (1733 lines total vs 1549 original)

## Files Created/Modified

### 2. `tests/test_str_enum_flag.py`
- **5 test cases** covering:
  - Single enum column
  - Multiple enums in same table
  - Shared enums across tables
  - Nullable enums
  - Behavior without the flag
- **3 test cases modified** to add explicit `nullable=False` to Column definitions

## Detailed Changes to `generators.py`

### PATCH 1: Added "use_str_enums" to valid_options (Line 765)
- Added `"use_str_enums"` to the `valid_options` set in `DeclarativeGenerator` class

### PATCH 2: Added str_enums dictionary (Line 786-789)
```python
self.str_enums: dict[str, tuple[str, list[str]]] = {}
```
- Maps enum signatures to (class_name, values) tuples
- Populated during model generation via `_extract_enum_info()`
- Used during code rendering to identify str_enum columns

### PATCH 3: Added 5 new helper methods (Lines 801-895)

#### 1. `_get_enum_signature(enum_values)` (Lines 806-808)
- Creates unique signature for enum based on sorted values
- Used for deduplication of identical enums across tables

#### 2. `_generate_str_enum_name(table_name, column_name, existing_names)` (Lines 810-829)
- Generates PascalCase names for StrEnum classes
- Logic: If `table_name` is empty (shared enum), use column name only
- Otherwise, use TableColumn format (e.g., `UsersStatus`)
- Ensures uniqueness using `find_free_name()`

#### 3. `_extract_enum_info()` (Lines 831-871)
- Scans all tables in metadata for Enum-type columns
- Builds `signature_info` dict to track enum values and their sources
- Preserves original enum value order (not alphabetically sorted)
- Generates appropriate names based on whether enum is shared across tables
- Populates `self.str_enums` dictionary

#### 4. `_render_str_enum_class(class_name, values)` (Lines 873-883)
- Renders a single StrEnum class definition
- Converts enum values to valid Python identifiers (uppercase, replace special chars)
- Handles edge cases like values starting with digits

#### 5. `_render_str_enums()` (Lines 885-895)
- Renders all StrEnum class definitions
- Sorts by class name for consistent output
- Returns classes separated by blank lines

### PATCH 4: Modified collect_imports() (Lines 900-909)
- Added call to parent's `collect_imports()`
- Adds `Mapped` and `mapped_column` imports for ModelClass instances
- Adds `StrEnum` import from `enum` module when:
  - `use_str_enums` option is enabled AND
  - At least one str_enum exists in `self.str_enums`

### PATCH 5: Extract enum information before collecting imports (Line 998)
- Added call to `self._extract_enum_info()` in `generate_models()`
- Called BEFORE `collect_imports()` to ensure str_enums dict is populated

### PATCH 6: Modified render_models() (Lines 1263-1276)
- Overridden to render StrEnum definitions BEFORE model classes
- Calls `_render_str_enums()` and adds result to rendered sections
- Maintains original logic for rendering models

### PATCH 7: Modified render_column_python_type() (Lines 1376-1423)
- Added nested function `render_python_type()` that checks if column type is Enum
- When `use_str_enums` is enabled and column matches a str_enum signature:
  - Returns the StrEnum class name instead of built-in type
  - Used in `Mapped[StrEnumClass]` type annotations

### PATCH 8: Override render_column() (Lines 1425-1447)
- Overrides parent's `render_column()` method
- Removes redundant `nullable=False` parameter for str_enum columns
- Only applies when:
  - Not rendering table (i.e., rendering declarative model)
  - Column is not nullable and not a primary key
  - `use_str_enums` option is enabled
  - Column type is Enum and matches a str_enum signature
- Keeps `nullable=False` for other column types (e.g., ForeignKey)

### PATCH 9: Override collect_imports_for_column() (Lines 918-931)
- Overrides parent's method to skip Enum import for str_enum columns
- When column is an Enum type matching a str_enum signature:
  - Does NOT import `Enum` type from SQLAlchemy
  - Still handles special cases like ARRAY
- Otherwise delegates to parent implementation

### PATCH 10: Override render_column_type() (Lines 1449-1461)
- Overrides parent's method to render String instead of Enum for str_enum columns
- When `use_str_enums` is enabled and column matches a str_enum signature:
  - Returns `"String"` literal
  - Adds String import
- Otherwise delegates to parent implementation
- Used in `mapped_column(String)` instead of `mapped_column(Enum(...))`

## Implementation Flow

1. User runs sqlacodegen with `--options use_str_enums`
2. Database metadata is reflected (existing code)
3. `TablesGenerator.fix_column_types()` converts CHECK constraints to Enum types (existing code)
4. `DeclarativeGenerator.generate_models()` is called
5. **NEW**: `_extract_enum_info()` scans all tables for Enum columns and builds str_enums dict
   - Groups identical enums by signature
   - Generates appropriate names (shared vs table-specific)
   - Preserves original value order
6. Imports are collected:
   - **NEW**: Skips Enum import for str_enum columns (`collect_imports_for_column`)
   - **NEW**: Adds StrEnum import if str_enums exist (`collect_imports`)
7. **NEW**: `render_models()` renders StrEnum class definitions first
8. Model classes are rendered:
   - **NEW**: `render_column_python_type()` returns StrEnum class name in type annotations
   - **NEW**: `render_column_type()` returns String instead of Enum(...) in mapped_column
   - **NEW**: `render_column()` removes redundant nullable=False for str_enum columns

## Key Design Decisions

### Enum Naming Strategy
- **Single table usage**: `TableNameColumnName` (e.g., `UsersStatus`)
- **Multi-table usage**: `ColumnName` only (e.g., `Status`)
- Ensures clarity and avoids name collisions

### Value Ordering
- Preserves original order from CHECK constraint
- Does not sort alphabetically for better readability

### Nullable Handling
- Respects explicit `nullable=False` in Column definitions
- Does not add redundant `nullable=False` to `mapped_column()` for str_enums
- Nullability expressed through `Optional[]` in type annotations

### Import Optimization
- Only imports StrEnum when actually needed
- Skips SQLAlchemy Enum import when using str_enums
- Keeps String import for the mapped_column type

## Backwards Compatibility

- Feature is opt-in via `use_str_enums` option
- Without the option, behavior is identical to current implementation
- Only affects `declarative` generator (not `tables`, `dataclasses`, or `sqlmodels`)
- Does not modify database interaction, only code generation
- All existing tests pass (48 declarative generator tests)

## Testing Strategy

All 5 tests in `test_str_enum_flag.py` pass:
- ✓ Basic functionality (single enum column)
- ✓ Multiple enums per table (different values)
- ✓ Shared enums across tables (same values, deduplicated)
- ✓ Nullable enum columns (with Optional[] annotation)
- ✓ Behavior without flag enabled (falls back to standard Enum)

No regressions in existing test suite:
- ✓ All tests in the `tests/` directory pass.