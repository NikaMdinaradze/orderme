import os

import typer

from db import get_pool
from utils import read_file

app = typer.Typer()
pool = get_pool()


@app.command()
def migrate():
    migrations_folder = "src/migrations"

    if not os.path.exists(migrations_folder):
        typer.echo(f"Error: Migrations folder not found at {migrations_folder}")
        return

    sql_files = [f for f in os.listdir(migrations_folder) if f.endswith(".sql")]

    if not sql_files:
        typer.echo(f"No SQL files found in {migrations_folder}")
        return

    for sql_file in sql_files:
        sql_path = os.path.join(migrations_folder, sql_file)
        sql_content = read_file(sql_path)
        typer.echo(f"Running {sql_path}...")
        try:
            with pool.connection() as conn:
                conn.execute(sql_content)
        except Exception as e:
            typer.echo(e)

    typer.echo("Migrations Completed For All SQL Files")


if __name__ == "__main__":
    app()
