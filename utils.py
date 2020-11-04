from enum import Enum


class PaymentStatus(Enum):
    NOT_CHARGED = 'NOT_CHARGED'
    PENDING = 'PENDING'
    CHARGED = 'CHARGED'
    REFUNDED = 'REFUNDED'
    REFUSED = 'REFUSED'
    CANCELLED = 'CANCELLED'
