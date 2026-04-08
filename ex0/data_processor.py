from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.storage = []
        self.rank = 0

    def output(self) -> tuple[int, str]:
        value = str(self.storage.pop(0))
        rank = self.rank
        self.rank += 1

        return rank, value

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def append_all(self, data: Any) -> None:
        if isinstance(data, list):
            for d in data:
                self.storage.append(d)
        else:
            self.storage.append(data)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, int | float):
            return True

        if isinstance(data, list):
            return all(isinstance(i, (int, float)) for i in data)

        return False

    def ingest(self, data: int | float | list) -> None:
        if self.validate(data):
            self.append_all(data)

        else:
            raise TypeError("Improper numeric data")


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(isinstance(i, str) for i in data)

        return False

    def ingest(self, data: str | list) -> None:
        if self.validate(data):
            self.append_all(data)

        else:
            raise TypeError("Improper Text data")


class LogProcessor(DataProcessor):
    def __check_dict(self, data: Any) -> bool:
        if isinstance(data, dict):
            for d in data.items():
                if not (isinstance(d[0], str) and isinstance(d[1], str)):
                    return False
            return True
        return False

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            if self.__check_dict(data):
                return True

        elif isinstance(data, list):
            for d in data:
                if not self.__check_dict(d):
                    return False
            return True
        return False

    def ingest(self, data: list | dict) -> None:
        if self.validate(data):
            if isinstance(data, dict):
                self.storage.append(": ".join(data.values()))
            elif isinstance(data, list):
                for d in data:
                    self.storage.append(": ".join(d.values()))
        else:
            raise TypeError("Improper Log data")


if __name__ == "__main__":
    print("\033[1;35m\n=== Code Nexus - Data Processor ===\033[0m\n")

    print("\033[1;34mTesting Numeric Processor...\033[0m")
    num = NumericProcessor()
    print(f" Trying to validate input '42': {num.validate(42)}")
    print(f" Trying to validate input 'Hello': {num.validate('Hello')}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")

    try:
        num.ingest('foo')  # type: ignore

    except Exception as e:
        print(f" Got exception: {e}")

    print(" Processing data: [1, 2, 3, 4, 5]")
    num.ingest([1, 2, 3, 4, 5])

    print(" Extracting 3 values...")
    for _ in range(3):
        output = num.output()
        print(f" Numeric value {output[0]}: {output[1]}")

    text = TextProcessor()
    print("\n\033[1;36mTesting Text Processor...\033[0m")
    print(f" Trying to validate input '42': {text.validate(42)}")

    print(" Processing data: ['Hello', 'Nexus', 'World']")
    text.ingest(['Hello', 'Nexus', 'World'])

    print(" Extracting 1 value...")
    output = text.output()
    print(f" Text value {output[0]}: {output[1]}")

    print("\n\033[1;34mTesting Log Processor...\033[0m")
    log = LogProcessor()
    print(f" Trying to validate input 'Hello': {log.validate("Hello")}")
    print(" Processing data: [{'log_level': 'NOTICE', 'log_message': 'Connecti"
          "on to server'}, {'log_level': 'ERROR', 'log_message': 'Unauthorized"
          " access!!'}]")

    log.ingest([{'log_level': 'NOTICE', 'log_message': 'Connection to server'},
                {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
                ])
    print(" Extracting 2 values...")

    for _ in range(2):
        output = log.output()
        print(f" Log entry {output[0]}: {output[1]}")
