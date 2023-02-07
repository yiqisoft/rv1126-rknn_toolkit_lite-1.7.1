FROM debian10-python3-opencv3.4.3

COPY ./rknn_toolkit_lite-1.7.1-cp37-cp37m-linux_armv7l.whl /tmp
COPY ./lib/* /usr/lib

RUN /usr/bin/python3 -m pip install --upgrade pip \
    && pip3 install /tmp/rknn_toolkit_lite-1.7.1-cp37-cp37m-linux_armv7l.whl \
    && rm -rf /tmp/rknn_toolkit_lite-1.7.1-cp37-cp37m-linux_armv7l.whl

RUN pip3 install cffi
RUN pip3 install pynng==0.7.1
RUN apt install libjpeg62-turbo-dev -y
RUN pip3 install pillow
RUN pip3 install ekuiper==1.7.1
RUN pip3 install tflite_runtime

COPY ./kuiper-1.7.1-linux-arm.deb /tmp
RUN dpkg -i /tmp/kuiper-1.7.1-linux-arm.deb \
    && rm -rf /tmp/kuiper-1.7.1-linux-arm.deb

RUN apt autoremove