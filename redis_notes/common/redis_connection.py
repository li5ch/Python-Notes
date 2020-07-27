import redis

from redis_notes.common.log import log_info


def _set_up_redis_instance():

    instance = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)

    return instance

redis_pool = None

try:
    redis_pool = _set_up_redis_instance()
    print str(redis_pool)+"wwwwww"
    print redis_pool.ping()
    response = redis_pool.client_list()
    log_info('sbsb' + str(response))
    log_info(redis_pool)
except:
    print "fail initiating redis instance"
try:
    conn = redis.Redis(host='localhost', port=6379, decode_responses=True)
    response = conn.client_list()
    log_info('hbhb'+str(response))
except redis.ConnectionError:
    log_info('connection sbsbsb')