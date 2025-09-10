"""Align users/tasks to models (add created_at, ensure FK)"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "XXXXXXXX_align_users_tasks"
down_revision: Union[str, None] = "6e691e6e1984"  # or None if this is first
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # --- USERS: add created_at if missing ---
    if "users" in insp.get_table_names():
        user_cols = {c["name"] for c in insp.get_columns("users")}
        if "created_at" not in user_cols:
            op.add_column(
                "users",
                sa.Column(
                    "created_at",
                    sa.DateTime(timezone=True),
                    server_default=sa.text("CURRENT_TIMESTAMP"),
                    nullable=False,
                ),
            )
    else:
        # Create table if it doesn't exist (rare on your path, but safe)
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("full_name", sa.String(length=255), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
            sa.UniqueConstraint("email", name="uq_users_email"),
        )
        op.create_index("ix_users_email", "users", ["email"])

    # --- TASKS: add created_at if missing; ensure FK to users ---
    if "tasks" in insp.get_table_names():
        task_cols = {c["name"] for c in insp.get_columns("tasks")}
        if "created_at" not in task_cols:
            op.add_column(
                "tasks",
                sa.Column(
                    "created_at",
                    sa.DateTime(timezone=True),
                    server_default=sa.text("CURRENT_TIMESTAMP"),
                    nullable=False,
                ),
            )

        # ensure FK exists (name it explicitly for stability)
        fks = insp.get_foreign_keys("tasks")
        has_user_fk = any(
            fk.get("referred_table") == "users"
            and fk.get("constrained_columns") == ["user_id"]
            and fk.get("referred_columns") == ["id"]
            for fk in fks
        )
        if not has_user_fk:
            op.create_foreign_key(
                "fk_tasks_user",
                source_table="tasks",
                referent_table="users",
                local_cols=["user_id"],
                remote_cols=["id"],
            )

        # ensure index on user_id
        idx_names = {idx["name"] for idx in insp.get_indexes("tasks")}
        if "ix_tasks_user_id" not in idx_names:
            op.create_index("ix_tasks_user_id", "tasks", ["user_id"])
    else:
        # Create table if it doesn't exist
        op.create_table(
            "tasks",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column("user_id", sa.Integer(), nullable=False, index=True),
            sa.Column("title", sa.String(length=255), nullable=False),
            sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.text("0")),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_tasks_user"),
        )
        op.create_index("ix_tasks_user_id", "tasks", ["user_id"])


def downgrade() -> None:
    # Only reverse additive bits; leave tables intact
    bind = op.get_bind()
    insp = sa.inspect(bind)

    if "tasks" in insp.get_table_names():
        task_cols = {c["name"] for c in insp.get_columns("tasks")}
        if "created_at" in task_cols:
            op.drop_column("tasks", "created_at")
        # drop FK/index only if you really want a stricter downgrade; usually not needed
        # op.drop_constraint("fk_tasks_user", "tasks", type_="foreignkey")
        # op.drop_index("ix_tasks_user_id", table_name="tasks")

    if "users" in insp.get_table_names():
        user_cols = {c["name"] for c in insp.get_columns("users")}
        if "created_at" in user_cols:
            op.drop_column("users", "created_at")
        # op.drop_index("ix_users_email", table_name="users")
        # op.drop_constraint("uq_users_email", "users", type_="unique")
