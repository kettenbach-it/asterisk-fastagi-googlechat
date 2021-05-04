# Asterisk FastAGI Integration of Google (Hangouts) Chat
... and with "Google (Hangouts) Chat" I mean the new one (which tries to copy Slack).

... using a simple webhook to send messages to a Hangout-Chat-Channel
in an asynchronous fashion (so it does not block the Asterisk diaplan).


## Installation
This service was developed with the aim of running in docker.
It will also work without docker, but docker is the recommended way.

### Using docker


### Not using docker



## Usage in Asterisk
Here's an example how you can use this FastAGI service in Asterisk
(in a Macro) assuming you deployed it to the same host Asterisk is running
at. You can deploy it to any other docker host having internet access
reachable by your asterisk host - just adjust the hostname accordingly.


## References

### Source Code
Can be found on [GitHub]()

### Docker Container Image
Can be found on  [DockerHub]().


### Google Chat Webhook Documentation
Can be found [here](https://developers.google.com/hangouts/chat/how-tos/webhooks)
and [the source here](https://github.com/googleapis/google-api-python-client).
