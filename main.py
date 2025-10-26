import typer , subprocess , os , shutil
from rich.console import Console

console = Console()
script = typer.Typer(name="FCache")

def checkIfRoot():
    return os.geteuid() == 0

def checkAurHelper():
    for posHelper in ["yay" , "paru" , "trizen"]:
        if shutil.which(posHelper):
            return posHelper
    return None

def getFolderSize(path):
    folderSize = 0
    for file in os.scandir(path):
        if file.is_dir():
            folderSize += getFolderSize(file.path)
        else:
            folderSize += os.stat(file.path).st_size
    return folderSize

@script.command(name="clean")
def clean(maxVers: int = 3 , dryRun:bool = False , deepClean: bool = False):
    if not checkIfRoot():
        console.print("[bold][FCache][/bold] [bold red]This script requires root access to execute. Please re-run with 'sudo'.[/bold red]")
        return
    
    if deepClean:
        maxVers = 1

    if deepClean and dryRun:
        console.print("[bold]FCache[/bold] [bold red]Cant use both 'deepclean' and 'dryrun'![/bold red]")
        return

    if maxVers <= 0:
        console.print("[bold][FCache][/bold] [bold red]'maxVers' argument cant be negative or 0.[/bold red]")
        return 

    aurHelper = checkAurHelper()
    
    if not aurHelper:
        console.print("[bold]FCache[/bold] [bold yellow]No known AUR helper found. Skipping...[/bold yellow]")

    if dryRun:
        print(subprocess.run(["sudo" , "paccache" , "-d" , "-k" , f"{maxVers}"] , capture_output=True , text=True).stdout.strip("\n") + " [PACMAN]")
        print(f"==> {getFolderSize(os.environ.get('XDG_CACHE_HOME' , f'/home/{os.environ.get('SUDO_USER')}/.cache/') + aurHelper) / (1024 ** 3):.2f} GiB [AUR]")
    
    console.print("[bold]FCache[/bold] [bold white]Cleaning pacman...[/bold white]")
    subprocess.run(["sudo" , "paccache" , "-k" , f"{maxVers}" , "-r"])
    if aurHelper:
        console.print("[bold]FCache[/bold] [bold white]Cleaning AUR helper...[/bold white]")
        subprocess.run([aurHelper , f"-Sc{'s' if deepClean else ''}"])
        subprocess.run([aurHelper , "-Ycc"])

if __name__ == "__main__":
    script()
