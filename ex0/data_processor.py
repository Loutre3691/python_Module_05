from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.data = []
        self.rank = 0

    def output(self) -> tuple[int, str]:
        value = self.data.pop(0)
        rank = self.rank
        self.rank += 1

        return rank, value

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass
    

class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, int | float):
            return True
        
        elif isinstance(data, list):
            return all(isinstance(i, (int, float)) for i in data)
        
        else:
            return False

    def ingest(self, data: int | float | list) -> None:
        
      

# class TextProcessor(DataProcessor):

#     def validate(self, data: Any) -> bool:
#         return

#     def ingest(self, str, list):
#         output()


# class LogProcessor(DataProcessor):

#     def validate(self, data: Any) -> bool:
#         return

#     def ingest(self, dict , list) -> str:
#         output()


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    proc = NumericProcessor()
    print(proc.validate(42))
    print(proc.validate('Hello'))







# objectif :
# démontrez comment différents types de données peuvent partager des
# interfaces de traitement communes tout en conservant leurs
# caractéristiques uniques.
#
# mettre en place:
# - classe abstraite DataProcessor qui herite d'ABC
# - 3 classe speciales: NumericProcessor, TextProcessor, and LogProcessor
# qui herit de la classe Dataprocessos
#  - 2 methode abstraite dans dataprocessor:
#        - validate (qui vérifie si les données d'entrée
#                     sont appropriées pour le processeur de données actuelles)
#        - ingest (qui traite les donnees d'entrees)
#  - 1 method standar dans DataProcessor -> output qui renvoi les ingested data
#
#  Contraintes:
#   - la methode validater envoie une valeur booléenne indiquant si les données 
#      fournies peuvent être ingérées par ce processeur de données.
#   - la method ingest ( Si l'utilisateur ne valide pas les données avant d'appeler 
#          ingest` et fournit des données invalides, une exception devra être levée
#
# La méthode de sortie extrait les données les plus anciennes stockées en interne dans le processeur de données, 
# ainsi que leur rang de traitement associé. Ces données sont ensuite supprimées du processeur.
#
# architecture:
# - creer des instance pour chaque class specialise
# - Tester les données valides et invalides pour chaque classe à l'aide de la méthode validate.
# - teste au moin une donne invalid grace a la methode ingest, et leve une exception.
# un avertissement mypy devra etre intentionnellement present
# - 