from .executor import ExecutorBase
import warnings
from ..utils import SmallBatchWarning
from typing import Callable


class SingleExecutor(ExecutorBase):
    def load_producer(self, producer: Callable, **producer_kwargs) -> None:
        self.producer = producer
        self.producer_kwargs = producer_kwargs

    def load_consumer(self, consumer: Callable, **consumer_kwargs) -> None:
        self.consumer = consumer
        self.consumer_kwargs = consumer_kwargs

    def __call__(self, **kwargs):
        ships = self.producer(**self.producer_kwargs)
        if len(ships) < 10:
            warnings.warn(
                "The small batch of input files is deprecated",
                SmallBatchWarning,
                **kwargs
            )

        self.consumer(ships, **self.consumer_kwargs)
