# Build docker image for `rknn-toolkit-lite` and `eKuiper`

## Build image(Cross Platform)
Cross build
```
docker buildx build --platform=linux/arm/v7 . -t rv1126-rknn_toolkit_lite1.7.1-ekuiper1.8.0
```

## Test image
Docker run
```
docker run -it --rm --name rv1126-ekuiper rv1126-rknn_toolkit_lite1.7.1-ekuiper1.8.0 /bin/bash
```

### Check `rknn-toolkit-lite` installation
Run commline in docker container, no errors.

```
root@05fc51c319d9:/opt/build# python3 -c "from rknnlite.api import RKNNLite; rknn_lite = RKNNLite(); print(rknn_lite.list_devices())"
*************************
None devices connected.
*************************
([], [])

```
### Check `eKuiper` installation
Run `kuiperd` in container, listenning port `9081`
```
root@05fc51c319d9:/opt/build# kuiperd
Serving kuiper (version - 1.8.0) on port 20498, and restful api on http://0.0.0.0:9081. 

```
