#!/usr/bin/python



"""
Forked from https://github.com/wez3.
Changes: 
* Possibility of using an IP or dns as a target;
* Report export path;
* New web-oriented/dedicated  modules.

"""


import logging, time, json, argparse, fileinput, re
from os import listdir, system, path, makedirs
from sys import exit

def loadConfig(currentPath):
    """
    Loads configuration file(s)
    """
    try:
        with open(currentPath + '/config') as f:
            return json.load(f)
    except Exception as e:
        log.error("\033[0;31m\033[1m[!]\033[0m Cannot load configuration\nException: {}\n".format(str(e)))
        exit(1)


def validateModuleConfig(modules, modulesconfig, config, currentPath):
    """
    Validates the config module
    """
    modulesfolder = "{}/{}".format(currentPath, config.get('modulesfolder'))
    missing = []
    for module in modules:
        modulename = module.split("/")[-1]
        if (not path.isfile(path.join(modulesfolder, modulename))):
            missing.append(modulename)
    if missing:
        log.warning("Module(s) are missing: {}".format(", ".join(missing)))


def generateRcs(targets, threads, projectName, config, currentPath, logsfolder):
    """
   Compiles all the configuration modules into an RC file
    """
    modulesfolder = "{}/{}".format(currentPath, config.get('modulesfolder'))
    postmodule = "spool off\n\n"
    premodule = "spool {}/".format(logsfolder)
    modules = config.get('modules')
    modulesconfig = [f for f in listdir(modulesfolder) if path.isfile(path.join(modulesfolder, f))]

    validateModuleConfig(modules, modulesconfig, config, currentPath)

    if threads == None:
        threads = str(config.get('defaultthreads'))

    rcfile = ""
    for target in targets:
        for module in modules:
            modulename = module.split("/")[-1]
            settings = config.get('settings')
            try:
                run = True
                customSettings = True
                for key, value in settings[module].iteritems():
                    if value == "CHANGEME":
                        run = False
                if run == True:
                    log.info("Module settings have been customized {}".format(module))
                else:
                    log.warning("No customizations have been defined for the module  {}".format(module))
            except:
                run = True
                customSettings = False
            if run == True:
                if (path.isfile(path.join(modulesfolder,modulename))):
                    rcfile += "{}{}/{}.log\n".format(premodule, projectName, modulename)
                    rcfile += "use {}\n".format(module)
                    rcfile += "setg threads {}\n".format(str(threads))
                    if customSettings == True:
                        for key, value in settings[module].iteritems():
                            rcfile += "set {} {}\n".format(key, value)
                    rcfile += open(path.join(modulesfolder,modulename),'r').read().replace("%IP%", target)
                    rcfile += postmodule
    rcfile += "exit -y\n"
    rcoutput = open("{}/{}/file.rc".format(logsfolder, projectName), 'w')
    rcoutput.write(rcfile)
    rcoutput.close()

def runRcs(projectName, config, logsfolder):
    """
    Run metasploit commands print output
    """
    log.critical('\n→→→→→→→→→→ Starting msfconsole ←←←←←←←←←←')
    
    system('msfconsole -r {}/{}/file.rc'.format(logsfolder, projectName))
    log.info('\n→→→→→→→→→→ MFS Completed ←←←←←←←←←←\n')


def getSuccessful(projectName, config, logsfolder):
    """
    Prints all [+] entries in the log context.
    """
    log.critical('\n→→→→→→→→→→ Summary of findings ←←←←←←←←←←\n')
    for f in listdir("{}/{}".format(logsfolder, projectName)):

        if f.endswith(".log"):
            log.warning('- Module: {}'.format(f.rsplit('.', 1)[0]))
            result = system('grep [+] {}/{}/{}'.format(logsfolder, projectName, f))

            if result == 256: # Sem Resultados terminas aos 256
                log.debug("No Results")
            elif result == 0: # All results printed end in 0
                pass
            else:
                log.critical(re.sub(r"\[\+]", "\033[0;32m\033[1m[+]\033[0m",result))

    log.critical('\n→→→→→→→→→→ MFS Completed ←←←←←←←←←←')
    
    
    
class logFormat(logging.Formatter):
    """
    Custom logging formatter
    """

    crit_fmt = "%(msg)s" # no format
    err_fmt  = "\033[0;33m\033[1m[!]\033[0m %(msg)s" # bold yellow [!]
    warn_fmt = "\033[0;34m\033[1m[*]\033[0m %(msg)s" # bold blue [*]
    info_fmt = "\033[0;32m\033[1m[+]\033[0m %(msg)s" # bold green [+]
    dbg_fmt  = "\033[0;31m\033[1m[-]\033[0m %(msg)s" # bold red [-]


    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt)


    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._fmt = logFormat.dbg_fmt

        elif record.levelno == logging.INFO:
            self._fmt = logFormat.info_fmt

        elif record.levelno == logging.WARN:
            self._fmt = logFormat.warn_fmt

        elif record.levelno == logging.ERROR:
            self._fmt = logFormat.err_fmt

        elif record.levelno == logging.CRITICAL:
            self._fmt = logFormat.crit_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._fmt = format_orig

        return result


def ascii():
    """
     
    """
    print(r"""
     ┓     ┓  • 
┓┏┏┏┓┣┓┓┏┏┓┃┏┓┓╋
┗┻┛┗ ┗┛┛┗┣┛┗┗┛┗┗
         ┛      
     With Metasploit    
          """)


if __name__ == '__main__':
    # Define logger settings
    currentPath = path.dirname(path.abspath(__file__))
    logfile= "{}/webxploit.log".format(currentPath)
    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    log = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(logFormat())
    log.addHandler(handler)
    ascii()

    # Load config with default settings
    config = loadConfig(currentPath)

    # Define variables
    logsfolder = "{}/{}".format(currentPath, config.get('logsfolder'))
    projectName = None
    targets = []
    threads = None

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="auto Web exploit framework")
    parser.add_argument('-j', '--threads', nargs='?', help='Number of Threads', type=int)
    parser.add_argument('-p', '--project', nargs='?', help='Project Name', type=str)
    parser.add_argument('-f', '--folder', nargs='?', help='Report Path', type=str)
    parser.add_argument('-t', '--target', nargs='?', help='127.0.0.1 / exemple.com / targets.txt', type=str)
    parser.add_argument('files', metavar='TARGET_FILE', nargs='?', default='-', help='targets file')
    args = parser.parse_args()

    # Check if target file is accessible and load it
    if not path.isfile(args.files):
        if not args.target:
            exit('\n[?] Usage: python3 webxploit.py -h')
        else:
            targets.append(args.target)
    else:
        for target in fileinput.input(files=args.files if len(args.files) > 0 else ('-', )):
            targets.append(target)

    # Check if threads are specified.
    if args.threads is not None:
        threads = args.threads

    if args.project is None:
        projectName = str(int(time.time()))
    else:
        projectName = args.project


    # Check if threads are specified.
    if args.folder is not None:
        logsfolder = args.folder




    log.critical('\n→→→→→→→→→→ Starting MSF Exploit ←←←←←←←←←←')

    # Create current run directory
    try:
        currentDir = "{}/{}".format(logsfolder, projectName)
        makedirs(currentDir, exist_ok=True)
        log.warning('Saving MSF logs at: {}'.format(currentDir))
    except:
        exit('\033[0;31m\033[1m[!]\033[0m The folder could not be created.')

    # Run the script
    generateRcs(targets, threads, projectName, config, currentPath, logsfolder)
    runRcs(projectName, config, logsfolder)
    getSuccessful(projectName, config, logsfolder)
