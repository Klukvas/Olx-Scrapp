import logging

class Logger:
    def custom_logger(self):
        
        logging.addLevelName(102, 'successfully')
        logging.addLevelName(101, 'start')

        log = logging.getLogger('Olx_logger')
        log.setLevel(logging.INFO)
        file = logging.FileHandler(filename='olx.log', mode='a')
        console = logging.StreamHandler()

        file.setLevel(logging.WARNING)
        console.setLevel(logging.INFO)

        file.setFormatter(logging.Formatter('%(levelname)s: %(asctime)s: %(message)s', datefmt='%d/%m  %H:%M:%S'))
        console.setFormatter(logging.Formatter('%(levelname)s: %(asctime)s: %(message)s', datefmt='%H:%M:%S'))

        log.addHandler(file)
        log.addHandler(console)
        def start(self, message, *args, **kws):
            if self.isEnabledFor(101):
            # Yes, logger takes its '*args' as 'args'.
                self._log(101, message, args, **kws) 
        logging.Logger.start = start

        def successfully(self, message, *args, **kws):
            if self.isEnabledFor(102):
            # Yes, logger takes its '*args' as 'args'.
                self._log(102, message, args, **kws) 
        logging.Logger.successfully = successfully

        return log
