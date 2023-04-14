import os
import openai
import sys
import subprocess

from rich import print as rprint

openai.api_key = os.getenv("OPENAI_API_KEY")


def send_to_gpt(query: str) -> str:
    prompt = f"""
    You are Alfred, a helpful AI assistant running in a ZSH shell.
    You will be given a task to complete, which you will do by
    executing a script. Return just the command(s) to
    execute, as I will take them and write them to a script that will be run.
    No markdown, just executable shell
    commands.

    Task: {query}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=1.0,
    )
    return response["choices"][0]["message"]["content"]


def main():
    query = " ".join(sys.argv[1:])
    command = send_to_gpt(query)
    with open("script.sh", "w") as f:
        f.write(command)
    rprint(f"Do you want to run this command? [bold red]{command}[/bold red]")
    yes = "[bold green]y[/bold green]"
    no = "[bold red]n[/bold red]"
    rprint(f"Press {yes} to run, {no} to cancel.")
    choice = input(">")
    if choice.strip().lower() == "y":
        rprint("[italic green]Running command...[/italic green]")
        subprocess.run(["sh", "script.sh"])
    else:
        rprint("Command cancelled.")


if __name__ == "__main__":
    main()
