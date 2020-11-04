import asyncio

from ariadne import QueryType, load_schema_from_path, make_executable_schema, SubscriptionType, MutationType
from ariadne.asgi import GraphQL
from fastapi import FastAPI

from database import db

schema = load_schema_from_path('schema.graphql')

query = QueryType()

mutation = MutationType()

subscription = SubscriptionType()


@query.field('payment')
def resolve_payment(_, info, id):
    return db.get_payment_by_id(id)


@query.field('payments')
def resolve_payments(_, info, status=None):
    if status is not None:
        return db.get_payments_by_status(status)
    return db.get_payments()


@subscription.source("payments")
async def payments_generator(obj, info):
    while True:
        queue = db.queue
        payment = await queue.get()
        await asyncio.sleep(1)
        queue.task_done()
        yield payment


@subscription.field("payments")
def payment_resolver(payment):
    return payment


@mutation.field("createPayment")
def resolve_create_payment(_, info, input):
    clean_input = {
        "amount": input['amount'],
        "creditCard": input['creditCard'],
        "status": input['status']
    }
    payment = db.create_payment(clean_input)
    return {'payment': payment, 'status': True}


schema = make_executable_schema(schema, query, subscription, mutation)
graphql_server = GraphQL(schema, debug=True)

app = FastAPI(debug=True)
app.add_route("/graphql", graphql_server)
app.add_websocket_route("/graphql", graphql_server)
