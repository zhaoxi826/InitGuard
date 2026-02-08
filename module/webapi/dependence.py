from fastapi import Request

def dependence_pg(request:Request):
    return request.app.state.pg_instance
def dependence_redis(request:Request):
    return request.app.state.redis_instance