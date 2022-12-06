FROM mambaorg/micromamba:1-focal
LABEL desc="Install conda and pip dependencies for the SBB streamlit app"
USER root
# Install build python wheel build dependencies for the case when a package has no wheel
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-dev gcc libc-dev g++ pkg-config cmake && \
    apt-get clean
USER mambauser
ARG MAMBA_DOCKERFILE_ACTIVATE=1
COPY --chown=$MAMBA_USER:$MAMBA_USER ${PWD}/.streamlit /home/mambauser/.streamlit
COPY --chown=$MAMBA_USER:$MAMBA_USER ${PWD} /app/
WORKDIR /app
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "streamlit", "run"]
CMD ["SBB_App.py", "--server.port=8501", "--server.address=0.0.0.0"]