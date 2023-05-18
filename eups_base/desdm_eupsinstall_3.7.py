'''
Created on Oct 3, 2012

@author: Stefan C. Mueller
'''

#: Version of this script. 
#: Changes that modify the creates eups environment must
#: increase this version. Packages may fail to build if
#: created for a different version of the environment.
#: This variable is also exported in the generated shell
#: scripts.
DESDM_EUPSINSTALL_VERSION = "2018_Q3"
# Checks for Darwin version and install packages accordingly

import sys
try:
    from termcolor import colored as c
except:
    def c(line, color):
        return line

# Get Darwin version
def get_darwin_version():
    if sys.platform.startswith("darwin"):
        sout = os.popen('sw_vers -productVersion').read()
        version = "%s.%s" % tuple(sout.split(".")[0:2])
    else:
        raise RuntimeError("Cannot get darwin version for non OSX systems")
    return version

#DES LOGO
def noc(line,color):
    return line
def print_deslogo(color=True):
    char0=u"\u203E"
    char1=u"\u203E"
    char2=u"\u00B4"
    if sys.stdout.encoding != 'UTF-8':
        char0=' '
        char1='-'
        char2='`'
    if color:
        c2=c
    else:
        c2=noc
    L=[]
    if sys.stdout.encoding != 'UTF-8': L.append("     _______      ")
    L.append("""     \\"""+char0*6+"""\      """)
    L.append("  "+c2("//","red")+" / .    .\    ")
    L.append(" "+c2("//","red")+" /   .    _\   ")
    L.append(c2("//","red")+" /  .     / "+c2("//","red")+" ")
    L.append(c2("\\\\","red")+" \     . / "+c2("//","red")+"  ")
    L.append(c2(" \\\\","red")+" \_____/ "+c2("//","red")+"   ")
    L.append(c2("  \\\\_______//","red")+"    DARK ENERGY SURVEY")
    last=c2("""   `"""+char1*7+char2,"red") +"     DATA MANAGEMENT"
    L.append(last)

    print()
    for l in L: 
        print(l)


try:
    import subprocess as commands
    import sys
    import os
    import time
    import tempfile
    import errno
    import shutil
    import base64
    import datetime
except:
    pass # it will never get beyond checking the python version anyway


check_status = False

def flush(f):
    f.flush();
    time.sleep(0.05)

def check_start(title):
    global check_status
    if check_status:
        raise RuntimeError("Cannot start test. Other test is running.")
    check_status = True
    sys.stdout.write((title + "...").ljust(70))
    flush(sys.stdout)

def check_ok(*message_lines):
    check_end(True, *message_lines)

def check_error(*message_lines):
    check_end(False, *message_lines)

def check_warn(*message_lines):
    check_end("warn", *message_lines)
 
def check_end(isok, *message_lines):
    global check_status
    if not check_status:
        raise RuntimeError("Cannot end test. No test is running.")
    check_status = False
    if isok == True:
        sys.stdout.write("ok\n")
    elif isok == "warn":
        sys.stdout.write("warning\n")
    else:
        sys.stdout.write("error\n")
    
    msg = "\n".join(message_lines).strip("\n")
    if msg:
        msg = "  " + msg.replace("\n", "\n  ")
    if isok == True:
        if msg:
            sys.stdout.write(msg + "\n")
    else:
        if msg:
            sys.stderr.write(msg + "\n")
        else:
            sys.stderr.write("Test failed.\n")
    flush(sys.stdout)
    flush(sys.stderr)
    if isok == False:
        sys.exit(2)

def check_after():
    global check_status
    if check_status:
        raise RuntimeError("Check was not not finished.")
        
def ask_string(question, default, check=None):
   
    ask_again = True
    answer = None
    while(ask_again):
        ask_again = False
        sys.stdout.write("\n" + question + "\n")
        sys.stdout.write("[%s] : " % default)
        flush(sys.stdout)
        line = sys.stdin.readline()
        if line:
            line = line.strip()
            answer = None
            if not line:
                answer = default
            else:
                answer = line
            
            if check != None:
                message = check(answer)
                if message:
                    sys.stdout.write("\n")
                    flush(sys.stdout)
                    sys.stderr.write(message + "\n")
                    flush(sys.stderr)
                    ask_again = True
        else:
            sys.stdout.write("\n")
            flush(sys.stdout)
            sys.stderr.write("Reached end of input. Aborting.\n")
            sys.exit(2)
    return answer

def ask_bool(question, default):
    ask_again = True
    while ask_again:
        ask_again = False
        sys.stdout.write("\n" + question + "\n")
        if default:
            sys.stdout.write("[yes] : ")
        else:
            sys.stdout.write("[no] : ")
        flush(sys.stdout)
        line = sys.stdin.readline()
        if line:
            line = line.strip().lower()
            if not line:
                answer = default
            else:
                if line == "y" or line == "yes":
                    answer = True
                elif line == "n" or line == "no":
                    answer = False
                else:
                    answer = None
                    ask_again = True
                    sys.stdout.write("\n")
                    flush(sys.stdout)
                    sys.stderr.write("Please answer with 'yes' or 'no'.\n")
                    flush(sys.stderr)
            if answer:
                return answer
        
def check_python_version():
    check_start("Checking python version")
    version = sys.version_info
    if version[0] < 3:
        check_error("Found python version %s." % sys.version,
                    "EUPS only works with python 3.",
                    "Please install python 3 or newer")
    if version[1] < 4:
        check_error("Found python version %s." % sys.version,
                    "EUPS needs at least python 3.4.",
                    "Please install python 3.4 or newer")
    check_ok()
    
def check_command(name, testcmd):
    check_start("Checking existence of '%s'" % name)
    status, output = commands.getstatusoutput(testcmd)
    if status != 0:
        check_error("%s might not be installed or is not working." % name,
                    "Running '%s' resulted in return code %s." % (testcmd, status),
                    "Output:",
                    output)
    else:
        check_ok()
        
def check_command_eups_fallback(name, testcmd):
    check_start("Checking existence of '%s'" % name)
    status, output = commands.getstatusoutput(testcmd)
    if status != 0:
        check_warn( "%s might not be installed or is not working." % name,
                    "Running '%s' resulted in return code %s." % (testcmd, status),
                    "Output:",
                    output)
        install = ask_bool("Would you like to install %s using EUPS?" % name, True)
        if not install:
            check_start("Checking existence of '%s'" % name) 
            check_error("No %s available." % name)
        return install
    else:
        check_ok()
        return False

def check_file(filename, envvars=[], dirs=[]):
    check_start("Checking if file %s exists." % filename)
    alldirs = dirs[:]
    for envvar in envvars:
        if envvar in os.environ:
            paths = os.environ[envvar]
            alldirs.extend(paths.split(":"))
    
    path = None
    for directory in alldirs:
        if os.path.isdir(directory):
            try:
                files = os.listdir(directory)
                if filename in files:
                    candidate = os.path.join(directory, filename)
                    if os.path.isfile(candidate):
                        path = candidate
                        break
            except:
                pass
    if path == None:
        check_error("File %s not found." % filename,
                    "Searched in the following directories:",
                    "\n".join(list(alldirs))
        )
    if not os.access(path, os.R_OK):
        check_error("File %s found at location %s." % (filename, path),
                    "But file cannot be read.")
    check_ok()
    return path
    
def detect_shell():
    check_start("Checking shell type")
    if not"SHELL" in os.environ:
        check_error("Unable to detect the shell which is in use.",
                    "Environment variable SHELL is not defined.")
    shellexe = os.environ["SHELL"]
    if "bash" in shellexe:
        shell = "bash"
    elif "csh" in shellexe:
        shell = "csh"
    else:
        check_error("Unsupported shell '%s'.",
                    "Support 'bash', 'tcsh' and 'csh'.",
                    "But none of those strings appears in SHELL='%s'" % shellexe)
    check_ok()
    return shell

def welcome():
    print_deslogo()
    print()
    print('\nWelcome to the EUPS installer\n')

def finalize():
    print('\n')
    line='''
    ********************************************************************************
    * Thanks for installing the DESDM EUPS.                                        *
    ********************************************************************************
    ''' 
    print(line)
    print()

    

def requirements():
    eups_packages = []
    print("Some simple checks to see if the requirements are available...")
    check_python_version()
    shell = detect_shell()
    check_command("bash", "bash --version")
    check_command("curl", "curl --version")
    if check_command_eups_fallback("wget", "wget --help"):
        eups_packages.append(("wget", "1.16+1"))
        use_curl = True
    else:
        use_curl = False
    if check_command_eups_fallback("pkg-config", "pkg-config --help"):
        eups_packages.append(("pkgconfig", "0.28+4"))
    if check_command_eups_fallback("subversion", "svn --version"):
        eups_packages.append(("subversion", "1.6.18+1"))
    check_command("gcc", "gcc -v")
    check_command("gfortran", "gfortran -v")
    check_command("make", "make --version")
    check_command("tr", "echo 1 | tr 1 2")
    check_command("sed", "echo 1 | sed s/1/2/")
    check_file("zlib.h", [], ['/usr/include'])
    return {'shell':shell, 'eups_packages':eups_packages, 'use_curl':use_curl}
    
def check_install_dir(d, assume_exists=None):
    d = os.path.realpath(d)
    if os.path.exists(d):
        if not os.path.isdir(d):
            return "Cannot install into %s. It is not a directory." % d
        else:
            if not ask_bool("Directory %s already exists! Are you sure that you would like to use that directory?" % d, True):
                return "Please choose a different directory."
    else:
        parent = os.path.dirname(d)
        if not os.path.exists(parent) and (not assume_exists or parent != os.path.realpath(assume_exists)):
            if not ask_bool("Parent directory %s does not exist. Should it be created?" % parent, True):
                return "Please choose a different directory."

def ask_for_paths():

    eups_base = ask_string("Where should EUPS be installed?", 
            os.path.realpath(os.path.join(os.curdir, "eups")),
            check=check_install_dir)
    
    install_base = ask_string(
            "Where should the EUPS packages (the software components managed by EUPS)\nbe installed?", 
            os.path.realpath(os.path.join(eups_base, "packages")),
            check=lambda d:check_install_dir(d, assume_exists=eups_base))
    
    eups_base = os.path.realpath(eups_base)
    install_base = os.path.realpath(install_base)
    
    return {'eups':eups_base, 'install':install_base}

def check_script_exists(filepath):
    filepath = os.path.realpath(filepath)
    if not os.path.exists(filepath):
        return "File %s does not exist." % filepath
    if not os.path.isfile(filepath):
        return "Is not a file: %s" % filepath
    if not os.access(filepath, os.R_OK):
        return "The file %s is not readable." % filepath
    
def check_dir(path):
    path = os.path.realpath(path)
    if not os.path.exists(path):
        return "Directory %s does not exist." % path
    if not os.path.isdir(path):
        return "Is not a directory: %s" % path
    

def ask_for_compiler_cc():
    if sys.platform.startswith("darwin"):
        question = "Please select the CLANG C compiler that will be used to build packages:"
        error_message = "On OSX only CLANG compilers are supported."
        compiler_executable = "cc"
        look_for = "CLANG"
    else:
        question = "Please select the GCC compiler that will be used to build packages:"
        error_message = "On Linux only GNU compilers are supported."
        compiler_executable = "gcc"
        look_for = "GCC"  
    return ask_for_compiler(question, error_message, compiler_executable, look_for)


def ask_for_compiler_cxx():
    if sys.platform.startswith("darwin"):
        question = "Please select the CLANG C++ compiler that will be used to build packages:"
        error_message = "On OSX only CLANG compilers are supported."
        compiler_executable = "c++"
        look_for = "CLANG"
    else:
        question = "Please select the G++ compiler that will be used to build packages:"
        error_message = "On Linux only GNU compilers are supported."
        compiler_executable = "g++"
        look_for = "g++"  
    return ask_for_compiler(question, error_message, compiler_executable, look_for)

def ask_for_compiler_gfortran():
    question = "Please select the gfortran compiler that will be used to build packages:"
    error_message = "Only GNU compilers are supported."
    compiler_executable = "gfortran"
    look_for = "GNU Fortran"
    return ask_for_compiler(question, error_message, compiler_executable, look_for)


def ask_for_compiler(question, error_message, compiler_executable, look_for):
    compiler = check_file(compiler_executable, ["PATH"])
    
    def check_compiler(compiler):
        output = commands.getoutput("%s --version" % compiler)
        if look_for.lower() not in output.lower():
            return error_message
        else:
            return None
    
    compiler = ask_string(question, compiler, check_compiler)
    return compiler
    
    
def ask_for_icc(compiler):
    
    use_icc = ask_bool("Should those packages that support it be build with\n"
             "INTEL's ICC compiler and INTEL's MKL (Math Kernel Library), instead of\n"
             "%s, ATLAS and FFTW?\n"
             "ICC support is experimental.\n"
             "(ATLAS and FFTW are available as EUPS packages. ICC and MKL must be installed\n"
             " manually if they are to be used.)" % compiler, False)
    
    if not use_icc:
        return


    # Checks
    if not "PATH" in os.environ:
        check_error("PATH is not in the environment")
    if not "MKLROOT" in os.environ:
        check_error("MKLROOT is not in the environment.")

    # Definitions
    icc = check_file("icc", dirs=os.environ["PATH"].split(":"))
    exe = os.path.dirname(icc)
    mklroot = os.environ['MKLROOT']
    mkl_include = os.path.join(mklroot,'include')
    mkl_lib = os.path.join(mklroot,'lib')

    # More checks
    check_command("icc", "%s -v" % icc)
    if not os.path.isdir(mkl_include):
        check_error("%s does not exits in the system." % mkl_include)
    if not os.path.isdir(mkl_lib):
        check_error("%s does not exits in the system." % mkl_lib)
    
    return {'exe':exe,
            'mklroot':mklroot,
            'mkl_lib':mkl_lib,
            'mkl_include':mkl_include,
            }

def shellsetup(environment):
    sys.stdout.write("\n")
    sys.stdout.write("The installation will create a script that setup the environment for this EUPS\n")
    sys.stdout.write("installation. This script needs to be sourced before EUPS can be used.\n")
    
    bashrc = ask_bool("Should the setup script be sourced from ~/.bashrc ?", environment["shell"] == "bash")
    bashprofile = ask_bool("Should the setup script be sourced from ~/.bash_profile ?", environment["shell"] == "bash")
    cshrc = ask_bool("Should the setup script be sourced from ~/.cshrc ?", environment["shell"] == "csh")
    return {'bashrc':bashrc, 'bash_profile':bashprofile, 'cshrc':cshrc}
    
def yesno(boolean):
    if boolean:
        return "yes"
    else:
        return "no"
    
def last_check(environment, paths, compiler_cc, compiler_cxx, compiler_gfortran, icc, shellsetup):
    sys.stdout.write("\n\n---------------------------------------------------------------");
    msg = ""
    msg += "Before starting the installation, please review the settings:\n"
    msg += "\n"
    msg += "EUPS installation directory:         " + paths["eups"] + "\n"
    msg += "EUPS package installation directory: " + paths["install"] + "\n"
    msg += "\n"
    msg += "Primary C compiler:                  " + compiler_cc + "\n"
    msg += "Primary C++ compiler:                " + compiler_cxx + "\n"
    msg += "Primary fortran compiler:            " + compiler_gfortran + "\n"
    msg += "\n"
    eups_pkgs = environment['eups_packages']    
    if eups_pkgs:
        msg += "Installing the following EUPS packages by default:\n"
        for name,version in eups_pkgs:
            msg += "  %s %s\n" % (name,version)
        msg += "\n" 
    if not icc:
        msg += "Use only %s, %s, %s, ATLAS, and FFTW.\n" % (compiler_cc, compiler_cxx, compiler_gfortran)
    else:
        msg += "Use INTEL's ICC and MKL, if supported by the package:\n"
        msg += "  Executables:           ".ljust(70) + icc["exe"] + "\n"
        msg += "  MKLROOT:               ".ljust(70) + icc["mklroot"] + "\n"
        msg += "  MKL_INCLUDE:           ".ljust(70) + icc["mkl_include"] + "\n"
        msg += "  MKL_LIB:               ".ljust(70) + icc["mkl_lib"] + "\n"
    msg += "\n"
    msg += "Setup EUPS environment in\n"
    msg += "  .bashrc:       ".ljust(70) + yesno(shellsetup['bashrc']) + "\n"
    msg += "  .bash_profile: ".ljust(70) + yesno(shellsetup['bash_profile']) + "\n"
    msg += "  .cshrc:        ".ljust(70) + yesno(shellsetup['cshrc']) + "\n"
    msg += "\n"
    msg += "Are those settings correct?"
    if not ask_bool(msg, True):
        flush(sys.stdout)
        sys.stderr.write("Aborting installation. Nothing has been installed yet.\n")
        sys.exit(2)
    sys.stdout.write("---------------------------------------------------------------\n\n");
    
def make_tmp_dir():
    try:
        check_start("Creating temporary directory")
        tmpdir = tempfile.mkdtemp(prefix="eupsinstall")
        check_ok()
        return tmpdir
    except BaseException as e:
        check_error(str(e))
        
def change_dir(tmpdir, nicename):
    check_start("Changing into %s" % nicename)
    try:
        os.chdir(tmpdir)
        check_ok()
    except BaseException as e:
        check_error(str(e))
    
def run_command(cmd, nicename):
    check_start(nicename)
    try:
        status, output = commands.getstatusoutput(cmd)
    except BaseException as e:
        check_error("Execution of '%c' failed. Got exception:",
                    str(e))
    if status != 0:
        check_error("Execution of '%s' failed. Got exit code %s." % (cmd, status),
                    "Output:",
                    output)
    check_ok()
    return output
    
def makedirs(path, nicename):
    check_start("Ensuring existence of the %s" % nicename)
    shutil.rmtree(path, ignore_errors=True)
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            check_error(str(exc))
    check_ok()
    
def deletedir(path, nicename):
    check_start("Deleting %s" % nicename)
    try:
        shutil.rmtree(path)
    except OSError as exc:
        check_error(str(exc))
    check_ok()
    
def getflavor(eups_install_path):
    check_start("Finding this machines default flavor")
    cmd = "source %s/setups.sh > /dev/null 2> /dev/null; eups flavor"
    try:
        status, output = commands.getstatusoutput(cmd)
    except BaseException as e:
        check_error("Execution of '%c' failed. Got exception:",
                    str(e))
    if status != 0:
        check_error("Execution of '%c' failed. Got exit code %s." % (cmd, status),
                    "Output:",
                    output)
    check_ok()
    
    
def mk_bashscript(eups_install_path, flavor, compiler_cc, compiler_cxx, compiler_gfortran, icc):
    check_start("Creating environment setup script for BASH")
    lines = [
             "#!/usr/bin/env bash",
             "#",
             "# Sets up the environment variables for this EUPS installation.",
             "# Generated on %s" % str(datetime.datetime.now()),
             "#",
             "# Version of the installer that created this script.",
             "export DESDM_EUPSINSTALL_VERSION=\"%s\"" % DESDM_EUPSINSTALL_VERSION,
             "#",
             "# This script first cleans up potential residual from other EUPS",
             "# installations and then sources the setup file that comes with EUPS.",
             '# It also sets some DESDM specific environment variables.',
             "#",
             "unset EUPS_DIR",
             "unset EUPS_PATH",
             "unset SETUP_EUPS",
             "#",
             "# Remove all other EUPS installations from PATH.",
             "# (Removes all entries from PATH that contain an executable named 'eups'.)",
             "export PATH=`for path in $(echo $PATH | tr ':' '\\n'); do if [ ! -x $path/eups ]; then echo $path; fi done | tr '\\n' ':' | sed 's/:*$//' | sed 's/^:*//'`",
             "#",
             "# Remove all other EUPS installations from PYTHONPATH.",
             "# (Removes all entries from PYTHONPATH that contain a directory named 'eups'.)",
             "export PYTHONPATH=`for path in $(echo $PYTHONPATH | tr ':' '\\n'); do if [ ! -d $path/eups ]; then echo $path; fi done | tr '\\n' ':' | sed 's/:*$//' | sed 's/^:*//'`",
             "#",
             "# EUPS setup/unsetup depend on a correctly set SHELL environment variable.",
             "export SHELL=`/usr/bin/env bash -c 'which bash'`",
             "#",
             "# Compilers to use",
             "export CC=%s" % compiler_cc,
             "export CXX=%s" % compiler_cxx,
             "export GFORTRAN=%s" % compiler_gfortran,
             "#",
             "export EUPS_PKGROOT=http://descmp1.cosmology.illinois.edu/eeups/webservice/repository",
             "export SVNROOT=https://dessvn.cosmology.illinois.edu/svn/desdm/devel",
             "source %s/bin/setups.sh" % eups_install_path,
    ]
    if icc != None:
        iline = [
                 "# ICC & MKL setup",
                 "# ---------------",
                 "export ICC_COMPILER=%s" % icc["exe"],
                 "export MKL_INCLUDE=%s"  % icc["mkl_include"],
                 "export MKL_LIB=%s"      % icc["mkl_lib"],
                ]
    else:
        iline = [
                    "# No ICC setup."
                ]

    script = "\n".join(lines) + "\n" + "\n".join(iline)
    scriptfile = os.path.join(eups_install_path, "desdm_eups_setup.sh")
    try:
        open(scriptfile, 'w').write(script)
    except BaseException as e:
        check_error(str(e))
    check_ok()
    
def mk_cshscript(eups_install_path, flavor, compiler_cc, compiler_cxx, compiler_gfortran, icc):
    base64.b32encode("for path in $(echo $PATH | tr ':' '\\n'); do if [ ! -x $path/eups ]; then echo $path; fi done | tr '\\n' ':' | sed 's/:*$//' | sed 's/^:*//'".encode())
    
    check_start("Creating environment setup script for CSH")
    lines = [
             "#!/usr/bin/env csh",
             "#",
             "# Sets up the environment variables for this EUPS installation.",
             "# Generated on %s" % str(datetime.datetime.now()),
             "#",
             "# Version of the installer that created this script.",
             "setenv DESDM_EUPSINSTALL_VERSION \"%s\"" % DESDM_EUPSINSTALL_VERSION,
             "#",
             "# This script first cleans up potential residual from other EUPS",
             "# installations and then sources the setup file that comes with EUPS.",
             '# It also sets some DESDM specific environment variables.',
             "#",
             "unsetenv EUPS_DIR",
             "unsetenv EUPS_PATH",
             "unsetenv SETUP_EUPS",
             "#",
             "# Remove all other EUPS installations from PATH.",
             "# (Removes all entries from PATH that contain an executable named 'eups'.)",
             "setenv PATH `bash -c 'for path in $(echo $PATH | tr \":\" \"\\n\"); do if [ ! -x $path/eups ]; then echo $path; fi done | tr \"\\n\" \":\" | sed \"s/:*$//\" | sed \"s/^:*//\"'`",
             "#",
             "# Remove all other EUPS installations from PYTHONPATH.",
             "# (Removes all entries from PYTHONPATH that contain a directory named 'eups'.)",
             "setenv PYTHONPATH `bash -c 'for path in $(echo $PYTHONPATH | tr \":\" \"\\n\"); do if [ ! -x $path/eups ]; then echo $path; fi done | tr \"\\n\" \":\" | sed \"s/:*$//\" | sed \"s/^:*//\"'`",
             "#",
             "# EUPS setup/unsetup depend on a correctly set SHELL environment variable.",
             "setenv SHELL `/usr/bin/env bash -c 'which csh'`",
             "#",
             "# Compiler to use",
             "setenv CC %s" % compiler_cc,
             "setenv CXX %s" % compiler_cxx,
             "setenv GFORTRAN %s" % compiler_gfortran,
             "#",
             "setenv EUPS_PKGROOT http://descmp1.cosmology.illinois.edu/eeups/webservice/repository",
             "setenv SVNROOT https://dessvn.cosmology.illinois.edu/svn/desdm/devel",
             "source %s/bin/setups.csh" % eups_install_path,
    ]
    if icc != None:
        iline = [
                 "# ICC & MKL setup",
                 "# ---------------",
                 "setenv ICC_COMPILER %s" % icc["exe"],
                 "setenv MKL_INCLUDE %s"  % icc["mkl_include"],
                 "setenv MKL_LIB %s"      % icc["mkl_lib"],
                ]
    else:
        iline = [
                    "# No ICC setup."
                ]

    script = "\n".join(lines) + "\n" + "\n".join(iline)
    scriptfile = os.path.join(eups_install_path, "desdm_eups_setup.csh")
    try:
        open(scriptfile, 'w').write(script)
    except BaseException as e:
        check_error(str(e))
    check_ok()
 
def append_setup(shell, scriptfile, product, version):
    check_start("Appending setup command to %s script" % shell)
    script = "\n\nsetup %s %s\n" % (product, version)
    try:
        f = open(scriptfile, 'a+')
        f.write(script)
        check_ok()
    except BaseException as e:
        check_error(str(e))
    finally:
        f.close()
 
def register_login_script(script, source, nicename):
    check_start("Adding source command to %s" % nicename)
    try:
        f = open(script, "a+");
        f.write("\n")
        f.write("\n")
        f.write("# EUPS Environment Setup\n")
        f.write("source %s\n\n" % source)
        f.close()
    except BaseException as e:
        check_error(str(e))
    check_ok()
    
def main():
    welcome()
    environment = requirements()
    paths = ask_for_paths()
    compiler_cc = ask_for_compiler_cc()
    compiler_cxx = ask_for_compiler_cxx()
    compiler_gfortran = ask_for_compiler_gfortran()
    icc = ask_for_icc(compiler_cc)
    shell = shellsetup(environment)
    last_check(environment, paths, compiler_cc, compiler_cxx, compiler_gfortran, icc, shell)
    
    eups_install_path = os.path.join(paths["eups"], "1.2.31")
    package_path = paths["install"]
    
    tmpdir = make_tmp_dir()
    change_dir(tmpdir, "temporary directory")
    if environment['use_curl']:
        run_command("curl -O http://descmp1.cosmology.illinois.edu/eeups/webservice/resources/eups/eups-.tar.gz", "Downloading EUPS")
    else:
        run_command("wget http://descmp1.cosmology.illinois.edu/eeups/webservice/resources/eups/eups-1.2.31.tar.gz", "Downloading EUPS")
    run_command("tar xzf eups-1.2.31.tar.gz", "Unpacking EUPS")
    change_dir(os.path.join(tmpdir, "eups-1.2.31"), "unpacked directory")
    makedirs(paths["eups"], "EUPS installation directory")
    makedirs(eups_install_path, "EUPS version installation directory")
    makedirs(package_path, "EUPS installation directory for packages")
    run_command("./configure --prefix=%s --with-eups_dir=%s --with-eups=%s" %(eups_install_path, eups_install_path, package_path),
                "Configuring EUPS")
    run_command("make", "Building EUPS")
    run_command("make install", "Installing EUPS")
    change_dir(paths["eups"], "EUPS directory")
    deletedir(tmpdir, "temporary directory")
    run_command("ln -s 1.2.31 default", "Creating symlink 1.2.31 -> default")
    run_command("bash -c \"source %s/bin/setups.sh; eups flavor\"" % eups_install_path, 
                "Checking if we can run EUPS.")
    flavor = run_command("bash -c \"source %s/bin/setups.sh > /dev/null 2> /dev/null; eups flavor\"" % eups_install_path, 
                 "Extracting this machine's flavor")
    mk_bashscript(eups_install_path, flavor, compiler_cc, compiler_cxx, compiler_gfortran, icc)
    mk_cshscript(eups_install_path, flavor, compiler_cc, compiler_cxx, compiler_gfortran, icc)
    for name,version in environment['eups_packages']:
        run_command("bash -c \"source 1.2.31/desdm_eups_setup.sh; eups distrib install %s %s\"" % (name, version),
            "Installing %s %s" % (name,version))
        append_setup("BASH", "1.2.31/desdm_eups_setup.sh", name,version)
        append_setup("CSH", "1.2.31/desdm_eups_setup.csh", name,version)
    run_command("ln -s 1.2.31/desdm_eups_setup.sh .", "Creating symlink for bash setup script.")
    run_command("ln -s 1.2.31/desdm_eups_setup.csh .", "Creating symlink for csh setup script.")
    if shell['bashrc']:
        register_login_script(
                              os.path.join(os.getenv('HOME'), ".bashrc"), 
                              os.path.join(paths["eups"], "desdm_eups_setup.sh"),
                              "~/.bashrc")
    if shell['bash_profile']:
        register_login_script(
                              os.path.join(os.getenv('HOME'), ".bash_profile"), 
                              os.path.join(paths["eups"], "desdm_eups_setup.sh"),
                              "~/.bash_profile")
    if shell['cshrc']:
        register_login_script(
                              os.path.join(os.getenv('HOME'), ".cshrc"), 
                              os.path.join(paths["eups"], "desdm_eups_setup.csh"),
                              "~/.cshrc")
        
    sys.stdout.write("\n")
    sys.stdout.write("Installation completed.\n")
    sys.stdout.write("\n")
    
    if environment["shell"] == "bash":
        sys.stdout.write("Run the following command to setup the environment variables:\n")
        sys.stdout.write("  source %s\n" % os.path.join(paths["eups"], "desdm_eups_setup.sh"))
    elif environment["shell"] == "csh":
        sys.stdout.write("Run the following command to setup the environment variables:\n")
        sys.stdout.write("  source %s\n" % os.path.join(paths["eups"], "desdm_eups_setup.csh"))
    sys.stdout.write("\n")
    finalize()
if __name__ == '__main__':
    main()
