import asyncio

from utils import PaymentStatus


class DummyDatabase:
    queue = asyncio.Queue()

    payments = [
        {'id': '1', 'amount': 10, 'status': PaymentStatus.CHARGED.value, 'creditCard': '5500 0000 0000 0004'},
        {'id': '2', 'amount': 30, 'status': PaymentStatus.PENDING.value, 'creditCard': '5500 0000 0000 3214'},
        {'id': '3', 'amount': 15, 'status': PaymentStatus.PENDING.value, 'creditCard': '5500 0000 0000 9874'},
        {'id': '4', 'amount': 50, 'status': PaymentStatus.REFUSED.value, 'creditCard': '5500 0000 0000 7654'},
        {'id': '5', 'amount': 100, 'status': PaymentStatus.CHARGED.value, 'creditCard': '5500 0000 0000 1124'},
    ]

    def setup_queue(self):
        for payment in self.payments:
            self.queue.put_nowait(payment)

    def get_payment_by_id(self, id):
        try:
            return next((payment for payment in self.payments if payment['id'] == id))
        except StopIteration:
            return None

    def get_payments(self):
        return self.payments

    def get_payments_by_status(self, status):
        return [payment for payment in self.payments if payment['status'] == status]

    def generate_payment_id(self):
        return len(self.payments) + 1

    def create_payment(self, payload):
        payload['id'] = self.generate_payment_id()
        self.payments.append(payload)
        self.queue.put_nowait(payload)
        return payload


db = DummyDatabase()
db.setup_queue()
