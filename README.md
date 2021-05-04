# Asterisk FastAGI Integration of Google (Hangouts) Chat
... and with "Google (Hangouts) Chat" I mean the new one (which tries to copy Slack).

... using a simple webhook to send messages to a Hangout-Chat-Channel
in an asynchronous fashion, so it does not block the Asterisk diaplan.
Since calling the webhook can take up to a couple of seconds on an
embedded device, it makes sense to offload this to a FastAGI
service while continuing the dial plan.

## Creating a chatroom with webhook in Google chat
See the [official google documentation](https://developers.google.com/hangouts/chat/how-tos/webhooks).




## Installation
This service was developed with the aim of running in docker.
It will also work without docker, but docker is the recommended way.

### Using docker
The latest docker-image can be found on  [DockerHub](https://hub.docker.com/r/vkettenbach/asterisk-fastagi-googlechat).

Use [docker-compose.example.yml](docker-compose.example.yml) to run your container.

Running in docker, the configuration of the service is done in envrionment variables
as shown below:

```
version: "3.7"

services:
  asterisk-fastagi-googlechat:
    image: vkettenbach/asterisk-fastagi-googlechat:latest
    container_name: asterisk-fastagi-googlechat
    restart: unless-stopped
    network_mode: host
    environment:
      WEBHOOK: "<webhook url for the chatroom you want to send to>"
      HOST: "0.0.0.0"   # Listen on all interfaces
      PORT: 4573  # Listen on asterisk agi port
      TIMEOUT: 2  # Timeout
```



### Not using docker
If not all of the four environment variables are supplied, the service will
fall back to read the file "config.yaml" - see [config.example.yaml](config.example.yaml).

So if you want to checkout the code from git an run it using python
you need to create a virtual env to run the code. The service was
developed sing Python 3.9. It will probaly work down to 3.7. It won't
work with Python 2.


Here is an example of how this is done - somewhat:

```
git pull https://github.com/kettenbach-it/asterisk-fastagi-googlechat
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.example.yaml config.yaml
# now edit config.yaml accoring to your needs
python3 googlechat.agi.py
```


## Usage in Asterisk
Here's an example how you can use this FastAGI service in Asterisk
(in a Macro) assuming you deployed it to the same host Asterisk is running
at. You can deploy it to any other docker host having internet access
reachable by your asterisk host - just adjust the hostname accordingly.

```
exten => s,n,AGI(agi://localhost/,<users/all> Call from ${CALLERID(name)} to ${EXTEN} )
```


## References

### Source Code
Can be found on [GitHub](https://github.com/kettenbach-it/asterisk-fastagi-googlechat)

### Docker Container Image
Can be found on  [DockerHub](https://hub.docker.com/r/vkettenbach/asterisk-fastagi-googlechat).


### Google Chat Webhook Documentation
Can be found [here](https://developers.google.com/hangouts/chat/how-tos/webhooks)
and [the source here](https://github.com/googleapis/google-api-python-client).


## License
GNU AGPL v3

Fore more, see [LICENSE](LICENSE)
