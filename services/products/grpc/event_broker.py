"""Broker en memoria para distribuir eventos de productos a clientes gRPC."""

from __future__ import annotations

from queue import Queue
from threading import Lock
from typing import Any


class ProductEventBroker:
    """Mantiene una cola independiente por cada cliente suscrito."""

    def __init__(self) -> None:
        self._subscribers: set[Queue] = set()
        self._lock = Lock()

    def subscribe(self) -> Queue:
        """Registra un nuevo consumidor y retorna su cola de eventos."""
        subscriber: Queue = Queue()
        with self._lock:
            self._subscribers.add(subscriber)
        return subscriber

    def unsubscribe(self, subscriber: Queue) -> None:
        """Elimina un consumidor del broker."""
        with self._lock:
            self._subscribers.discard(subscriber)

    def publish(self, event: Any) -> None:
        """Envía un evento a todos los clientes actualmente conectados."""
        with self._lock:
            subscribers = tuple(self._subscribers)

        for subscriber in subscribers:
            subscriber.put(event)


product_event_broker = ProductEventBroker()
