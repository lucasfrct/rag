import sys

from src.librarian import librarian as Librarian
from src.routines import migrate as Migrate
from src.agent.agent import Agent

sys.dont_write_bytecode = True


# execuçao principal
def run():
    paths = Librarian.register("./bookcase")
    if len(paths) == 0:
        print("Nehum novo livro encontrado")
    else:
        print("Lista de livros adcionados: ", paths)

    agent = Agent()
    agent.txt_to_PDF("./lexicon")
    agent.welcome()
    for line in sys.stdin:
        agent.question(line)


if __name__ == "__main__":
    Migrate.tables()
    run()
