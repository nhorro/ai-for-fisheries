docker build \
--build-arg user_id=${user_id} \
--build-arg group_id=${group_id}  \
--build-arg user_name=${user_name} \
-t ${docker_image_name}:${docker_image_version} .
