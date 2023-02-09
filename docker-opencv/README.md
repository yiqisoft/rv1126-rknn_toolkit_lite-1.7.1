# Build base environment `Debian10 + python3.7.3 + opencv3.4.3` from source
## Cross build

The `OPENCV_VERSION` should be `3.4.3`, if you use `MacBook M1 Max` it takeks more than 30min depends on your host machine.
```
docker buildx build --platform=linux/arm/v7 --build-arg OPENCV_VERSION=3.4.3 . -t debian10-python3.7-opencv3.4.3
```
if you should to use `PROXY` in build command, add `--build-arg http_proxy=http://1.1.1.1:7890`
```
docker buildx build --platform=linux/arm/v7 --build-arg OPENCV_VERSION=3.4.3 --build-arg http_proxy=http://1.1.1.1:7890 . -t debian10-python3.7-opencv3.4.3
```

confirm built docker image
```
docker images
```

## Test image
start docker container
```
docker run -it --rm debian10-python3.7-opencv3.4.3 /bin/bash
```
check opencv version in python
```
root@05fc51c319d9:/opt/build# python3 -c "import cv2; print(cv2.__version__)"
3.4.3
```