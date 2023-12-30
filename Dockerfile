# Base image: Python 3.9
FROM python:3.9

# Copy Python requirements (not yet mapped in during execution of this script)
COPY common/requirements.txt /controller/common/
COPY database/requirements.txt /controller/database/
COPY hardware/requirements.txt /controller/hardware/
COPY logic/requirements.txt /controller/logic/
COPY server/requirements.txt /controller/server/

# Install Python requirements (and ignore warnings lol)
RUN pip install -r /controller/common/requirements.txt --disable-pip-version-check --root-user-action=ignore
RUN pip install -r /controller/database/requirements.txt --disable-pip-version-check --root-user-action=ignore
RUN pip install -r /controller/hardware/requirements.txt --disable-pip-version-check --root-user-action=ignore
RUN pip install -r /controller/logic/requirements.txt --disable-pip-version-check --root-user-action=ignore
RUN pip install -r /controller/server/requirements.txt --disable-pip-version-check --root-user-action=ignore

# Change working directory & start
WORKDIR /controller
CMD ["python", "main.py"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8577"]  # to run server