from git import Repo
from pathlib import Path
from .logger import setup_logger

logger = setup_logger()

class GitManager:
    def __init__(self, project_path: Path):
        self.path = project_path
        self._init_repo()

    def _init_repo(self):
        """Inicia um repo git se não existir."""
        try:
            if not (self.path / ".git").exists():
                Repo.init(self.path)
                logger.info(f"Repositório Git iniciado em {self.path}")
        except Exception as e:
            logger.error(f"Erro ao iniciar Git: {e}")

    def checkpoint(self, message: str):
        """Adiciona todos os arquivos e faz commit."""
        try:
            repo = Repo(self.path)
            # Adiciona tudo (git add .)
            repo.git.add(A=True)
            
            # Verifica se há mudanças antes de commitar
            if repo.is_dirty(untracked_files=True):
                repo.index.commit(message)
                logger.info(f"Checkpoint salvo: '{message}'")
            else:
                logger.info("Nenhuma alteração para salvar.")
        except Exception as e:
            logger.error(f"Erro ao criar checkpoint Git: {e}")