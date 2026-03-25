from ..protocols import Broker


__all__ = [
    'broker_nats',
]


def broker_nats() -> Broker:
    from ._nats import BrokerNats
    return BrokerNats()
