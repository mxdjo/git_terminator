"""
Terminator plugin to find git repo.

License: GPLv2
"""
import inspect, os, shlex, subprocess
import gtk
from terminatorlib.util import err, dbg
from terminatorlib import plugin
from terminatorlib import config

AVAILABLE = ['GitPlugin']

class GitPlugin(plugin.MenuItem):
    """ Process URLs returned by commands. """
    capabilities = ['terminal_menu']

    def __init__(self):
        plugin.MenuItem.__init__(self)
        self.plugin_name = self.__class__.__name__
        self.current_path = None
        
    def get_cwd(self):
        """ Return current working directory. """
        # HACK: Because the current working directory is not available to plugins,
        # we need to use the inspect module to climb up the stack to the Terminal
        # object and call get_cwd() from there.
        for frameinfo in inspect.stack():
            frameobj = frameinfo[0].f_locals.get('self')
            if frameobj and frameobj.__class__.__name__ == 'Terminal':
                return frameobj.get_cwd()
        return None        

    def callback(self, menuitems, menu, terminal):
        filepath = self.get_cwd()
        gitpath = filepath + '/.git/'
        #BUG si ls -l /etc/ suis encore dans home :( filepath pas bon !!
        print 'mon dossier: ' + gitpath
        
        if os.path.exists(gitpath):
            item = gtk.MenuItem('Git')
            menuitems.append(item)
            ##menuitems.connect("activate", self._execute, terminal)
            item.connect("activate", self._execute, {'terminal' : terminal, 'command' : 'git status' })
            dbg('Menu items git appended')
        else:
            dbg('Menu items git remove')
            
    def _execute(self, _widget, data):
        command = data['command']+"\n"
        terminal = data['terminal']
        print 'execution ? de ' + command
        terminal.feed(command)
        return command