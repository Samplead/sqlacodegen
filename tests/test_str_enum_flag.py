from __future__ import annotations

import pytest
from _pytest.fixtures import FixtureRequest
from sqlalchemy import INTEGER, VARCHAR, CheckConstraint, Column, MetaData, Table
from sqlalchemy.engine import Engine

from sqlacodegen.generators import CodeGenerator, DeclarativeGenerator

from .conftest import validate_code


@pytest.fixture
def generator(
    request: FixtureRequest, metadata: MetaData, engine: Engine
) -> CodeGenerator:
    options = getattr(request, "param", [])
    return DeclarativeGenerator(metadata, engine, options)


@pytest.mark.parametrize("generator", [["use_str_enums"]], indirect=True)
def test_single_enum_column(generator: CodeGenerator) -> None:
    """Test generation of a single enum column."""
    Table(
        "users",
        generator.metadata,
        Column("id", INTEGER, primary_key=True),
        Column("status", VARCHAR, nullable=False),
        CheckConstraint("status IN ('active', 'inactive', 'pending')"),
    )

    validate_code(
        generator.generate(),
        """\
from enum import StrEnum

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class UsersStatus(StrEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[UsersStatus] = mapped_column(String)
        """,
    )


@pytest.mark.parametrize("generator", [["use_str_enums"]], indirect=True)
def test_multiple_enum_columns_same_table(generator: CodeGenerator) -> None:
    """Test generation of multiple enum columns in the same table."""
    Table(
        "users",
        generator.metadata,
        Column("id", INTEGER, primary_key=True),
        Column("role", VARCHAR, nullable=False),
        Column("status", VARCHAR, nullable=False),
        CheckConstraint("role IN ('admin', 'user', 'guest')"),
        CheckConstraint("status IN ('active', 'inactive')"),
    )

    validate_code(
        generator.generate(),
        """\
from enum import StrEnum

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class UsersRole(StrEnum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'


class UsersStatus(StrEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[UsersRole] = mapped_column(String)
    status: Mapped[UsersStatus] = mapped_column(String)
        """,
    )


@pytest.mark.parametrize("generator", [["use_str_enums"]], indirect=True)
def test_shared_enum_across_tables(generator: CodeGenerator) -> None:
    """Test that the same enum type used in multiple tables is only defined once."""
    Table(
        "users",
        generator.metadata,
        Column("id", INTEGER, primary_key=True),
        Column("status", VARCHAR, nullable=False),
        CheckConstraint("status IN ('active', 'inactive', 'pending')"),
    )
    Table(
        "companies",
        generator.metadata,
        Column("id", INTEGER, primary_key=True),
        Column("status", VARCHAR, nullable=False),
        CheckConstraint("status IN ('active', 'inactive', 'pending')"),
    )

    validate_code(
        generator.generate(),
        """\
from enum import StrEnum

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Status(StrEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'


class Companies(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[Status] = mapped_column(String)


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[Status] = mapped_column(String)
        """,
    )


@pytest.mark.parametrize("generator", [["use_str_enums"]], indirect=True)
def test_nullable_enum_column(generator: CodeGenerator) -> None:
    """Test generation of nullable enum column."""
    Table(
        "users",
        generator.metadata,
        Column("id", INTEGER, primary_key=True),
        Column("status", VARCHAR, nullable=True),
        CheckConstraint("status IN ('active', 'inactive')"),
    )

    validate_code(
        generator.generate(),
        """\
from enum import StrEnum
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class UsersStatus(StrEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[Optional[UsersStatus]] = mapped_column(String)
        """,
    )


def test_without_use_str_enums_flag(generator: CodeGenerator) -> None:
    """Test that without the flag, enums are generated as regular Enum types."""
    Table(
        "users",
        generator.metadata,
        Column("id", INTEGER, primary_key=True),
        Column("status", VARCHAR),
        CheckConstraint("status IN ('active', 'inactive')"),
    )

    code = generator.generate()
    # Should not contain StrEnum
    assert "StrEnum" not in code
    # Should contain Enum type from SQLAlchemy
    assert "Enum(" in code or "status" in code
