from cmd2 import Cmd
from cmd2 import Cmd2ArgumentParser, with_argparser

class MqttCli(Cmd) :
    prompt = "mqtt>"


    userparser = Cmd2ArgumentParser()
    userparser.add_argument('-u', '--user', required=True, help='account')
    userparser.add_argument('-p', '--pwd', default='', help='password')

    @with_argparser(userparser)
    def do_user(self, args) :
        print("set user: " + args.user + " with password: " + args.pwd)

    connectparser = Cmd2ArgumentParser()
    connectparser.add_argument('-s', '--server', required=True, help="mqtt server address")
    connectparser.add_argument('-p', '--port', type=int, default=1883, help='mqtt server port')
    connectparser.add_argument('-k', '--keep', type=int, default=60, help='keep alive')
    connectparser.add_argument('-b', '--bind', default='', help='bind local address')

    @with_argparser(connectparser)
    def do_connect(self, args) :
        print("connect to " + args.server + " on port " + str(args.port) + ' with keep-alive ' + str(args.keep) + ', bind local ip: ' + args.bind)

    def emptyline(self) :
        pass

    def do_exit(slef, inp) :
        return True


if __name__ == "__main__" :
    MqttCli().cmdloop()