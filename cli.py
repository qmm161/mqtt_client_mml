from cmd2 import Cmd
from cmd2 import Cmd2ArgumentParser, with_argparser
import threading
import paho.mqtt.client as mqtt


class MqttCli(Cmd):
    prompt = "mqtt>"

    def __init__(self, client):
        super().__init__()
        self.client = client

    userparser = Cmd2ArgumentParser()
    userparser.add_argument('-u', '--user', required=True, help='account')
    userparser.add_argument('-p', '--pwd', default='', help='password')

    @with_argparser(userparser)
    def do_user(self, args):
        print("set user: " + args.user + " with password: " + args.pwd)

    connectparser = Cmd2ArgumentParser()
    connectparser.add_argument('-s',
                               '--server',
                               required=True,
                               help="mqtt server address")
    connectparser.add_argument('-p',
                               '--port',
                               type=int,
                               default=1883,
                               help='mqtt server port')
    connectparser.add_argument('-k',
                               '--keep',
                               type=int,
                               default=60,
                               help='keep alive')
    connectparser.add_argument('-b',
                               '--bind',
                               default='',
                               help='bind local address')

    @with_argparser(connectparser)
    def do_connect(self, args):
        print("connect to " + args.server + " on port " + str(args.port) +
              ' with keep-alive ' + str(args.keep) + ', bind local ip: ' +
              args.bind)
        self._mqtt_connect(args.server, args.port, args.keep, args.bind)

    subparser = Cmd2ArgumentParser()
    subparser.add_argument('-t', '--topic', required=True, help='topic')
    subparser.add_argument('-q',
                           '--qos',
                           choices=[0, 1, 2],
                           default=0,
                           help='qos')

    @with_argparser(subparser)
    def do_sub(self, args):
        print('subscribe topic: ' + args.topic + ' with qos: ' + str(args.qos))
        self.client.subscribe(args.topic, args.qos)

    pubparser = Cmd2ArgumentParser()
    pubparser.add_argument('-t', '--topic', required=True, help='topic')
    pubparser.add_argument('-j', '--json', default='{}', help='json payload')
    pubparser.add_argument('-q',
                           '--qos',
                           choices=[0, 1, 2],
                           default=0,
                           help='qos')
    pubparser.add_argument('-r',
                           '--retain',
                           type=bool,
                           default=False,
                           help='is need retain')

    @with_argparser(pubparser)
    def do_pub(self, args):
        print('publish topic: ' + args.topic + ' msg: ' + args.json +
              ' with qos: ' + str(args.qos))
        self.client.publish(args.topic, args.json, args.qos, args.retain)

    def emptyline(self):
        pass

    def do_exit(self, inp):
        self.client.loop_stop(True)
        return True

    def _mqtt_connect(self, server, port, keep, bind):
        self.client.connect(server, port, keep, bind)
        self.client.loop_start()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    MqttCli(client).cmdloop()