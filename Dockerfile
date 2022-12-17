FROM mambaorg/micromamba:1-focal
LABEL authors="Sadegh Shahmohammadi,Bachtijar Ashari"
LABEL desc="Install conda and pip dependencies for the SBB streamlit app"
ARG MAMBA_DOCKERFILE_ACTIVATE=1
WORKDIR /app
COPY ${PWD}/environment.yml environment.yml
# Use multiple threads to speed up environment build
RUN micromamba config set download_threads 4
RUN micromamba config set extract_threads 4
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes
# Copy the appcode
COPY ${PWD}/SBB_App.py /app/SBB_App.py
# Copy the streamlit config
COPY ${PWD}/.streamlit /home/mambauser/.streamlit
# Hint that server is on port 80
EXPOSE 8000
# Include the built in micromamba entrypoint to activate the conda environment
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "streamlit", "run"]
CMD ["SBB_App.py"]