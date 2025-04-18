import typer
from api_client import query_model
from part_lookup import SQLiteManager, DB_PATH

app = typer.Typer()
db_manager = SQLiteManager(DB_PATH)

@app.command()
def diagnose(
    issue: str,
    model_url: str = typer.Option("http://localhost:1234/v1", help="LM Studio API endpoint"),
    api_key: str = typer.Option(None, help="Optional API key")
):
    """Diagnose an HVAC issue using the AI model"""
    typer.echo("\nAnalyzing issue...\n")
    response = query_model(
        f"HVAC Technician: Diagnose this issue and provide detailed troubleshooting steps.\n\nIssue: {issue}",
        model_url,
        api_key
    )
    typer.echo(f"Troubleshooting Analysis:\n{response}")

@app.command()
def find_part(oem_number: str):
    """Lookup HVAC parts by OEM number"""
    part = db_manager.search_part(oem_number)
    if part:
        typer.echo("\nPart Found:")
        typer.echo(f"OEM Number: {part['oem_number']}")
        typer.echo(f"Manufacturer: {part['manufacturer']}")
        typer.echo(f"Description: {part['description']}")
        typer.echo(f"Alternates: {', '.join(part['alternate_numbers']) or 'None'}")
        typer.echo(f"Price: ${part['price']:.2f}")
        typer.echo(f"Source: {part['source_url']}")
    else:
        typer.echo(f"No part found with OEM number: {oem_number}")

if __name__ == "__main__":
    app()
