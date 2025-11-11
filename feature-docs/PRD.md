I want to implement the following feature in the `sqlacodegen` package. You should implement it in a way that I be able later to open a PR to the `sqlacodegen` package.

<feature>
# Feature: Generate ENUM fields as python `StrEnum types

## Feature description
Today, enum fields are generated as str columns. I'd like bind them to generated native python `StrEnum`. For avoiding over complications, I want to add this option only to the `declerative` generator.

## Example
When set `use_str_enums = True`, this is how the output should look like:
```python
from sqlalchemy import String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from enum import StrEnum


class RoleType(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"
    SUPER_ADMIN = "SUPER_ADMIN"


class ActivisionStatus(StrEnum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DEACTIVATED = "DEACTIVATED"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'User'

    user_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, server_default=text('gen_random_uuid()')
    )
    role: Mapped[RoleType] = mapped_column(
        server_default=text('\'USER\'::"RoleType"')
    )
    status: Mapped[ActivisionStatus] = mapped_column(
        server_default=text('\'ACTIVE\'::"ActivisionStatus"')
    )
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(precision=3), server_default=text('CURRENT_TIMESTAMP')
    )


class Company(Base):
    __tablename__ = 'Company'

    company_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, server_default=text('gen_random_uuid()')
    )
    status: Mapped[ActivisionStatus] = mapped_column(
        server_default=text('\'ACTIVE\'::"ActivisionStatus"')
    )
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(precision=3), server_default=text('CURRENT_TIMESTAMP')
    )
```
</feature>


# Implementation Notes
1. This feature is only relevant for the `declerative` generator. This should simplify the solution, as it doesn't necessarily need to be compatible to the other generators. This means that you don't need to understand, or to be worried about the other generators (i.e. the `tables`, `dataclasses`, `sqlmodels` generators are not relevant for this feature).
2. When implementing the solution, DO NOT generate unnecessary documentation or any markdown files unless you has been explicitly asked to.
3. IMPORTANT: Your implementation should be natively integrated into the existing codebase of the `sqlacodegen` package, and not to be some kind of wrapper around the existing code.
4. Difference between python's `Enum` and `StrEnum`: When using `StrEnum`, you can directly compare between the enum values to strings, without having to use the `value` attribute (i.e. `RoleType.USER == RoleType.USER.value == 'USER' is True).

# Instructions
1. Understand the codebase: Research the codebase and understand how it works.
2. Map relevant places in the codebase: Identify all the places in the codebase that should be changed to implement the feature. DO NOT suggest any solutions yet, just create a list of pointers to the relevant places in the codebase, and why they are relevant. You should format the pointers as permalinks (i.e. `https://github.com/agronholm/sqlacodegen/blob/master/path/to/file.py#L100`). NOTE: When mapping the relevant places, RECALL IS MORE IMPORTANT THAN PRECISION!. This list should be as comprehensive as possible (it's ok if we will understand later that some of the places are not relevant, but you should prevent from missing any relevant places).
3. Write tests: Create a dedicated test file names `tests/test_str_enum_flag.py` with 2-3 test cases that cover the feature. The over format and structure of the test file should follow the conventions of the existing `tests/test_generator_declarative.py` file.
4. Create a detailed implementation plan: Write the plan as a bite-sized checklist of tasks that need to be completed in order to implement the feature.
5. Run the tests to make sure that the code is working as expected. If not, iterate through steps 5.1. -> 5.3. until all the tests pass.
    5.1. Understand if the problem is in the implementation or in the tests.
    5.2. Fix the problem.
    5.3. Run the tests again.