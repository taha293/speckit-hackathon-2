import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from .service import TodoService, TaskNotFoundError

console = Console()

class TodoCLI:
    def __init__(self):
        self._service = TodoService()

    def run(self):
        console.print("[bold blue]Evolution of Todo - Phase 1 CLI[/bold blue]")
        console.print("Type 'help' for commands or 'exit' to quit.")

        while True:
            try:
                command = Prompt.ask("\n[bold]Command[/bold]").strip().lower()

                if command == "exit":
                    console.print("[yellow]Exiting application. Goodbye![/yellow]")
                    sys.exit(0)
                elif command == "add":
                    self.handle_add()
                elif command == "list":
                    self.handle_list()
                elif command == "complete":
                    self.handle_complete()
                elif command == "update":
                    self.handle_update()
                elif command == "delete":
                    self.handle_delete()
                elif command == "help":
                    self.show_help()
                else:
                    console.print(f"[red]Unknown command: '{command}'. Type 'help' for a list of commands.[/red]")
            except EOFError:
                break
            except Exception as e:
                console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

    def handle_add(self):
        title = Prompt.ask("Task Title").strip()
        if not title:
            console.print("[red]Title is required.[/red]")
            return
        description = Prompt.ask("Description (optional)", default="").strip() or None
        task = self._service.add(title, description)
        console.print(f"[green]Task added successfully! (ID: {task.id})[/green]")

    def handle_list(self):
        tasks = self._service.list_tasks()
        if not tasks:
            console.print("[yellow]No tasks found.[/yellow]")
            return

        table = Table(title="Your Todo List")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Status", justify="center")
        table.add_column("Title", style="magenta")
        table.add_column("Description")

        for task in tasks:
            status = "[green]✓ Complete[/green]" if task.completed else "[red]○ Incomplete[/red]"
            table.add_row(str(task.id), status, task.title, task.description or "")

        console.print(table)

    def handle_complete(self):
        try:
            task_id = IntPrompt.ask("Enter Task ID")
            # Logic for US2: Explicit status tagging
            is_complete = Confirm.ask("Mark as complete?")
            self._service.set_status(task_id, is_complete)
            status_text = "complete" if is_complete else "incomplete"
            console.print(f"[green]Task {task_id} marked as {status_text}.[/green]")
        except TaskNotFoundError as e:
            console.print(f"[red]{e}[/red]")
        except ValueError:
             console.print("[red]Invalid Task ID.[/red]")

    def handle_update(self):
        try:
            task_id = IntPrompt.ask("Enter Task ID")
            task = self._service.get_task(task_id)

            console.print(f"Current Title: {task.title}")
            new_title = Prompt.ask("New Title (leave blank to keep current)", default=task.title)

            console.print(f"Current Description: {task.description or 'N/A'}")
            new_desc = Prompt.ask("New Description (leave blank to keep current)", default=task.description or "")

            self._service.update(task_id, title=new_title, description=new_desc or None)
            console.print(f"[green]Task {task_id} updated successfully.[/green]")
        except TaskNotFoundError as e:
            console.print(f"[red]{e}[/red]")

    def handle_delete(self):
        try:
            task_id = IntPrompt.ask("Enter Task ID")
            if Confirm.ask(f"Are you sure you want to delete Task {task_id}?"):
                self._service.delete(task_id)
                console.print(f"[green]Task {task_id} deleted.[/green]")
        except TaskNotFoundError as e:
            console.print(f"[red]{e}[/red]")

    def show_help(self):
        console.print("\n[bold]Available Commands:[/bold]")
        console.print("  [cyan]add[/cyan]      - Create a new task")
        console.print("  [cyan]list[/cyan]     - Show all tasks")
        console.print("  [cyan]complete[/cyan] - Update task status (complete/incomplete)")
        console.print("  [cyan]update[/cyan]   - Edit task title/description")
        console.print("  [cyan]delete[/cyan]   - Remove a task")
        console.print("  [cyan]exit[/cyan]     - Quit the application")

def main():
    cli = TodoCLI()
    cli.run()

if __name__ == "__main__":
    main()
