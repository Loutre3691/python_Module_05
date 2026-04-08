from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = []
        for t in data:
            values.append(t[1])
        print("CSV Ouptut:\n " + " , ".join(values) + "")


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        store = []
        for t in data:
            store.append(f'"item_{t[0]}": "{t[1]}"')
        print("JSON Ouptut:\n {" + ", ".join(store) + "}")


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.proc_list:
            collected = []
            for _ in range(nb):
                if proc.storage:
                    collected.append(proc.output())
            plugin.process_output(collected)


if __name__ == "__main__":
    print("\033[1;35m\n=== Code Nexus - Data Pipeline ===\033[0m\n")

    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors\n")
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

    print(f"Send first batch of data on stream: {stream_list}\n")

    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)

    stream.process_stream(stream_list)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")

    csv = CSVExportPlugin()
    jsone = JSONExportPlugin()

    stream.output_pipeline(3, csv)
    print()

    stream.print_processors_stats()
    print()

    second_list = [
        21,
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [{'log_level': 'ERROR', 'log_message': '500 server crash'},
         {'log_level': 'NOTICE', 'log_message': 'Certificate'
          'expires in 10 days'}],
        [32, 42, 64, 84, 128, 168],
        'World hello'
        ]

    print(f"Send another batch of data: {second_list}\n")
    stream.process_stream(second_list)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, jsone)
    print()

    stream.print_processors_stats()
