FROM debian10-python3-opencv3.4.3

COPY ./rknn_toolkit_lite-1.7.1-cp37-cp37m-linux_armv7l.whl /tmp
COPY ./lib/* /usr/lib

RUN /usr/bin/python3 -m pip install --upgrade pip \
    && pip3 install /tmp/rknn_toolkit_lite-1.7.1-cp37-cp37m-linux_armv7l.whl \
    && rm -rf /tmp/rknn_toolkit_lite-1.7.1-cp37-cp37m-linux_armv7l.whl
    
