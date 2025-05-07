docker volume create --name=n8n_self_host_db_storage
docker volume create --name=n8n_self_host_n8n_storage
docker volume create --name=n8n_self_host_redis_storage
docker volume create --name=traefik_data
# docker image prune
docker image prune
