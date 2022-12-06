# SBB
StreamLit app that calculates similarities between different professions.

## Getting started
To run this using docker:

```
docker build -t sbb_streamlit:latest .
docker run -p 8000:80 sbb_streamlit:latest
```

Above code will build a Docker image, using the `SBB_App.py` code in this folder at build-time.
If at run-time you want to change the `SBB_App.py` code you can start the container and mount the python file (instead of relying on the file in the container itself):

```
docker run -p 8000:80 -v ${PWD}/SBB_App.py:/app/SBB_App.py sbb_streamlit:latest
```

Now, any changes made to the code will be picked up by the streamlit app in the container.
Similarly you can mount other files/folders (e.g. the `./streamli/config.toml` file) if you want to be able to change them without having to rebuild the Docker image.