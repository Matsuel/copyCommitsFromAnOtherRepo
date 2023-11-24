import os
import shutil
import subprocess
from rich import print
from rich.table import Table

def copyCommits():
    commits_list = []
    commits_message = []

    # Chemin du dépôt Git d'origine
    repo_path = "C:/Users/matsu/Documents/challenge-go-23"

    # Chemin du dossier de destination
    dest_path = "C:/Users/matsu/Documents/mesGits/challenge-go-23"

    # Récupération de la liste des commits, triés du plus récent au plus ancien
    commits = subprocess.check_output(["git", "rev-list", "--reverse", "origin/master"], cwd=repo_path).decode().split("\n")

    print(commits)
    # exit()

    # Parcours de la liste des commits
    for commit in commits:
        # Checkout du commit dans le dépôt d'origine
        subprocess.run(["git","checkout",commit], cwd=repo_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Copie du contenu du dépôt d'origine vers le dossier de destination en excluant .git
        copy_without_git(repo_path, dest_path)

        # Ajout des fichiers copiés au dépôt de destination
        subprocess.run(["git", "add", "."], cwd=dest_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Récupération du message du commit d'origine
        commit_info = subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:%s"], cwd=repo_path).decode().strip()

        subprocess.run(["git", "branch", "--unset-upstream", "origin/master"], cwd=dest_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Commit des modifications dans le dépôt de destination avec le message du commit d'origine et la date du commit d'origine
        subprocess.run(["git", "commit", "-m", commit_info], cwd=dest_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        subprocess.run(["git", "push", "--set-upstream", "origin", "main"], cwd=dest_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"Commit {commit} copié")
    
    show_Commits(commits_list, commits_message)


# Fonction pour copier les fichiers et dossiers en excluant .git
def copy_without_git(src, dst):
    for item in os.listdir(src):
        source_item = os.path.join(src, item)
        dest_item = os.path.join(dst, item)
        if item != ".git":
            if os.path.isdir(source_item):
                shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(source_item, dest_item)  # Copy file and preserve metadata

copyCommits()



def show_Commits(commits_list, commits_message):
    table = Table(title="Commits")
    table.add_column("Hash", justify="right", style="cyan", no_wrap=True)
    table.add_column("Message", style="magenta")
    table.add_column("Statut", justify="right", style="green")

    for i in range(len(commits_list)):
        table.add_row(commits_list[i], commits_message[i], "✅")
    
    return table