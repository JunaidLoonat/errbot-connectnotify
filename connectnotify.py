from errbot import BotPlugin, botcmd

class ConnectNotify(BotPlugin):
    """Notify the configured users/channels whenever the bot connects to the server"""

    def activate(self):
        super(ConnectNotify, self).activate()
        if 'VERSION' not in self:
            self['VERSION'] = 1
            self['NOTIFY'] = {}
            self['MESSAGE'] = "I'm online and ready to roll!"

    def callback_connect(self):
        for dstid in self['NOTIFY'].keys():
            self.send(
                self.build_identifier(dstid),
                self['MESSAGE'],
            )

    @botcmd(admin_only=True)
    def connectnotify(self, msg, args):
        """ display the current ConnectNotify recipient list
        """
        if len(self['NOTIFY']):
            yield 'ConnectNotify Recipient(s):'
            for dstid in sorted(self['NOTIFY'].keys()):
                yield ' * %s' % dstid
        else:
            return 'The ConnectNotify list is empty'

    @botcmd(admin_only=True, split_args_with=None)
    def connectnotify_add(self, msg, args):
        """ add a new recipient to the ConnectNotify list
        !connectnotify add <recipient>
        """
        if len(args) < 1:
            return 'Please specify a recipient: !connectnotify add <recipient>'
        identifier = args[0]
        with self.mutable('NOTIFY') as notifylist:
            if identifier in notifylist:
                return 'The recipient already exists on the ConnectNotify list: %s ' % identifier
            else:
                try:
                    self.build_identifier(identifier)
                    notifylist[identifier] = 1
                    resp = 'New recipient added to the ConnectNotify list: %s' % identifier
                    self.log.info(resp)
                    return resp
                except:
                    return 'The recipient does not appear to be valid: %s' % identifier

    @botcmd(admin_only=True)
    def connectnotify_clear(self, msg, args):
        """ clear all recipients from the ConnectNotify list
        """
        self['NOTIFY'] = {}
        resp = 'The ConnectNotify list has been cleared'
        self.log.info(resp)
        return resp

    @botcmd(admin_only=True, split_args_with=None)
    def connectnotify_remove(self, msg, args):
        """ remove an existing recipient from the ConnectNotify list
        !connectnotify remove <recipient>
        """
        if len(args) < 1:
            return 'Please specify a recipient: !connectnotify remove <recipient>'
        identifier = args[0]
        with self.mutable('NOTIFY') as notifylist:
            if identifier in notifylist:
                del notifylist[identifier]
                resp = 'The recipient was removed from the ConnectNotify list: %s' % identifier
                self.log.info(resp)
                return resp
            else:
                return 'The recipient not found on the ConnectNotify list: %s' % identifier
