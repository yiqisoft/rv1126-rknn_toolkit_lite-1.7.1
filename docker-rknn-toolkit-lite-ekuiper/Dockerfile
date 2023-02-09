FROM debian10-python3.7-opencv3.4.3

# Copy rknn-toolkit-lite and lib files
COPY ./rknn_toolkit_lite-1.7.1-cp37-cp37m-linux_armv7l.whl  ./kuiper-1.8.0-linux-arm.zip /tmp/
COPY ./lib/* /usr/lib

# Update pip
RUN /usr/bin/python3 -m pip install --upgrade pip

# Setup piwheel source
RUN (echo "[global]"; echo "extra-index-url=https://www.piwheels.org/simple";) >> /etc/pip.conf

# Install rknn-toolkit-lite package
RUN pip3 install /tmp/rknn_toolkit_lite-1.7.1-cp37-cp37m-linux_armv7l.whl 

# Install tflite_runtime and ekuiper
RUN pip3 install \
        sniffio==1.3.0 \ 
        cffi==1.5.1 \
        pillow==9.4.0 \
        pynng==0.7.1 \
        numpy==1.21.4 \
        ekuiper==1.8.0 \
        tflite_runtime==2.11.0 \
    && rm -rf /tmp/*.whl \
    && unzip -d / /tmp/kuiper-1.8.0-linux-arm.zip \
    && rm -rf /tmp/kuiper-1.8.0-linux-arm.zip \
    && mv /kuiper-1.8.0-linux-arm /kuiper \
    && ln -s /usr/bin/python3.7 /usr/bin/python \
    && apt -y autoremove
