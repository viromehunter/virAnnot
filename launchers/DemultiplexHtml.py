import os.path
import logging
from subprocess import call
import logging as log

class DemultiplexHtml:
    def __init__ (self, args):
        self.check_args(args)
        self.cmd = []
        self._create_cmd()


    def _create_cmd(self):
        cmd = 'demultiplex_html.py'
        keys = sorted(self.lib)
        for lib_name in keys:
            cmd += ' -i ' + lib_name + ' -c ' + self.lib[lib_name]
        cmd += ' -o ' + self.out
        log.debug(cmd)
        self.cmd.append(cmd)


    def launch (self):
        if not self.sge:
            for el in self.cmd:
                os.system (el)
        else:
            fw =  open(self.cmd_file, mode='w')
            for el in self.cmd:
                fw.write(el + "\n")
            fw.close()
            qsub_call =   "qsub -wd " + self.wd + " -V -N " 'demultiplexHtml' + ' ' + self.cmd_file
            log.debug(qsub_call)
            os.system(qsub_call)


    def check_args(self,args):
        self.wd = os.getcwd()
        self.cmd_file = self.wd + '/' + 'demultiplexHtml_cmd.txt'
        if 'out' in args:
            self.out = args['out']
        if 'sge' in args:
            self.sge = bool(args['sge'])
        else:
            self.sge = False
        if 'iter' in args:
            if args['iter'] == 'global':
                self.iter = 'global'
                self.lib = {}
                for s_id in args['args']:
                    self.lib[args['args'][s_id]['id']] = args['args'][s_id]['csv']
            else:
                log.critical('iter parameter mus be global.')
        else:
            log.critical('No iter parameters.')