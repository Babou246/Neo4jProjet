FROM python:3.9-alpine

# ARG USER_ID
# ARG GROUP_ID

# RUN groupadd -f -g $GROUP_ID user
# RUN useradd -u $USER_ID -g $GROUP_ID user
# USER user


ADD . /data
WORKDIR /data
RUN pip install -r requirements.txt
RUN pip install neo4j
RUN python -m pip install --upgrade pip
CMD [ "python", "app.py" ]
