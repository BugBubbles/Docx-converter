from typing import Callable
from .executor import ExecutorBase
import multiprocessing as mp
import time
import warnings


class MultipleExecutor(ExecutorBase):
    """
    Multiple processor based executor.
    """

    def __init__(
        self,
        num_proc: int = 2,
        rate: int = 10,
        max_size: int = 300,
        *producer_pool_args,
        **consumer_pool_kwargs,
    ) -> None:
        """
        ### Arguments
         - `num_proc` : number of `PRODUCER` processors, default is 2.
         - `rate` : the divident rate from number of consumers to number of producers.
         - `max_size` : the maximal number of cache.
         - `producer_pool_args` : the list input arguments for producer pool.
         - `consumer_pool_kwargs` : the dictionary input arguments for consumer pool.
        """
        if num_proc != 2:
            warnings.warn(
                "You are setting the producer's number to 2, which will make more computer resource idle unexpectedly.",
                DeprecationWarning,
            )
        self.quene = mp.Manager().Queue(max_size)
        self.num_producer = num_proc
        self.num_consumer = num_proc * rate
        self.rate = rate
        self.consumer_pool_kwargs = consumer_pool_kwargs
        self.producer_pool_args = producer_pool_args

    def load_producer(self, producer: Callable, **producer_kwargs) -> None:
        """
        Warning !! Producer should not be an iterator!
        """
        self.producer = producer
        self.producer_kwargs = producer_kwargs

    def load_consumer(self, consumer: Callable, **consumer_kwargs) -> None:
        self.consumer = consumer
        self.consumer_kwargs = consumer_kwargs

    def _produce(self, id_proc: int, **producer_kwargs) -> None:
        print(
            f"\n===================== Produce process {id_proc:03d}:{__name__} is now working ====================="
        )
        for ships in self.producer(**producer_kwargs):
            while self.quene.full():
                print(
                    f"\nQuene is full, read process {id_proc:03d}:{__name__} now rests..."
                )
                time.sleep(10)
            self.quene.put(ships)
            print(
                f"\n===================== Produce process {id_proc:03d}:{__name__} is temporarily finished, waiting for next boot ====================="
            )
        i = 0
        while i < self.rate:
            if not self.quene.full():
                self.quene.put("EOF")
                i += 1
        print(
            f"\n*************** Produce process {id_proc:03d}:{__name__} terminates ***************"
        )

    def _consume(self, id_proc: int, **consumer_kwargs) -> None:
        while True:
            try:
                ships = self.quene.get()
            except:
                continue
            if ships == "EOF":
                break
            print(
                f"\n===================== Consume process {id_proc:03d}:{__name__} is now working ====================="
            )
            self.consumer(file_list=ships, id_proc=id_proc, **consumer_kwargs)
            print(
                f"\n================ Consume process {id_proc:03d}:{__name__} finishes, waiting for next boot ================"
            )

        print(
            f"\n*************** Consume process {id_proc:03d}:{__name__} terminates ***************"
        )

    def __call__(self, **kwargs):
        try:
            assert self.producer and self.producer_kwargs
            assert self.consumer and self.consumer_kwargs
        except Exception as exc:
            print(
                exc
                + f"\n You must load producers and consumers functions first, by applying function {__class__}.load_producer and {__class__}load_consumer."
            )
        producer_pool = mp.Pool(processes=self.num_producer, *self.producer_pool_args)
        consumer_pool = mp.Pool(
            processes=self.num_consumer, **self.consumer_pool_kwargs
        )
        for id_proc in range(self.num_producer):
            producer_pool.apply_async(
                func=self._produce,
                kwds=dict(id_proc=id_proc, **self.producer_kwargs),
                **kwargs,
            )
        for id_proc in range(self.num_consumer):
            consumer_pool.apply_async(
                func=self._consume,
                kwds=dict(id_proc=id_proc, **self.consumer_kwargs),
                **kwargs,
            )
        producer_pool.close()
        consumer_pool.close()

        producer_pool.join()
        consumer_pool.join()
        print(
            "------------------------------------>>>>>>>>>>>>>>>>>>>>\n\
            All the processors terminate, exit the main process.\
            Now is {}.\n\
           <<<<<<<<<<<<<<<<<<<<<----------------------------------".format(
                time.strftime("%Y / %m / %d, %H : %M : %S")
            )
        )
