# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    git \
    build-essential \
    libgl1-mesa-glx \
    libegl1-mesa \
    libxrandr2 \
    libxss1 \
    libxcursor1 \
    libxcomposite1 \
    libasound2 \
    libxi6 \
    libxtst6 \
    curl

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

# Add conda to PATH
ENV PATH /opt/conda/bin:$PATH

# Create the conda environment and activate it
RUN conda create -y -n netica python=3.9 && \
    echo "source activate netica" > ~/.bashrc

# Copy Probflo directory
COPY Probflo /Probflo

# Clone the NeticaPy3 repository inside Probflo/Modules
RUN git clone https://github.com/PineApple-Logic/NeticaPy3.git /Probflo/Modules/NeticaPy3

# Install Cython in the netica environment
RUN /bin/bash -c "source activate netica && conda install -y cython==0.29.21"

# Compile NeticaPy3
RUN cd /Probflo/Modules/NeticaPy3 && \
    /bin/bash -c "source activate netica && ./compile_linux.sh /opt/conda/envs/netica/include/python3.9"

# Install NeticaPy3 in editable mode
RUN cd /Probflo/Modules/NeticaPy3 && /bin/bash -c "source activate netica && pip install -e ."

# Install requirements for Probflo
RUN /bin/bash -c "source activate netica && pip install -r /Probflo/requirements.txt"

# Set the working directory
WORKDIR /Probflo

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit application
CMD ["/bin/bash", "-c", "source activate netica && streamlit run main.py"]
