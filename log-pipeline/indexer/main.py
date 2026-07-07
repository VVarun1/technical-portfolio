import redis
# Consumes logs from Redis Stream and indexes into Elasticsearch
def index_logs():
    r = redis.Redis()
    while True:
        logs = r.xread({"logs_stream": "0"})
        # bulk_index_to_elasticsearch(logs)
