
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKeyConstraint,
    Integer,
    MetaData,
    String,
    Table,
    BLOB,
    Text,
    func,
    null,
    or_,
    select,
    UniqueConstraint,
)

# Taken from https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions
# Defining constraint naming conventions
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
sql_metadata = MetaData(naming_convention=convention)


buy = Table(
    "buy",
    sql_metadata,
    Column("property_id", String(255), primary_key=True, index=True),
    Column("beds", Float),
    Column("baths", Float),
    Column("lot_size", Float),
    Column("price", Float),
    Column("address_1", String(255)),
    Column("address_2", String(255)),
    Column("url", String(255)),
    Column("images", BLOB)
)