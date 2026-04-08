from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.storage: list[Any] = []
        self.rank = 0
        self.count = 0

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
                self.count += 1
                self.storage.append(d)

        else:
            self.storage.append(data)
            self.count += 1


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
                self.count += 1
                self.storage.append(": ".join(data.values()))
            elif isinstance(data, list):
                for d in data:
                    self.count += 1
                    self.storage.append(": ".join(d.values()))
        else:
            raise TypeError("Improper Log data")


class DataStream():
    def __init__(self) -> None:
        self.proc_list: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, DataProcessor):
            self.proc_list.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            found = False
            for proc in self.proc_list:
                if proc.validate(item):
                    proc.ingest(item)
                    found = True
            if not found:
                print("DataStream error - Can't process element in stream:",
                      item)

    def print_processors_stats(self) -> None:
        print("\033[1;34m=== DataStream statistics... ===\033[0m")
        if len(self.proc_list) < 1:
            print("No processor found, no data")
            return
        for proc in self.proc_list:
            name = proc.__class__.__name__
            result = ""
            for char in name:
                if char.isupper() and result != "":
                    result += " "
                result += char
            print(f"{result}: total {proc.count} items "
                  f"processed, remaining {len(proc.storage)} on processor")


if __name__ == "__main__":
    print("\033[1;35m\n=== Code Nexus - Data Stream ===\033[0m\n")

    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor\n")
    num = NumericProcessor()

    stream.register_processor(num)

    stream_list = [
         'Hello world',
         [3.14, -1, 2.71],
         [
            {'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh'
             'instead'},
            {'log_level': 'INFO', 'log_message': 'User wil is connected'}
         ],
         42,
         ['Hi', 'five']
        ]

    print(f"Send first batch of data on stream: {stream_list}")

    stream.process_stream(stream_list)
    stream.print_processors_stats()

    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)
    print("\nRegistering other data processors")

    stream.process_stream(stream_list)
    print("Send the same batch again")
    stream.print_processors_stats()

    print("\nConsume some elements from the data processors: Numeric 3,"
          " Text 2, Log 1")
    for _ in range(3):
        num.output()
    for _ in range(2):
        text.output()
    log.output()
    stream.print_processors_stats()
