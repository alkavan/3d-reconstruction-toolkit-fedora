"""
This script is for an easy use of OpenMVG and OpenMVS

usage: MvgMvs_Pipeline.py [-h] [--steps STEPS [STEPS ...]] [--preset PRESET]
                          [--0 0 [0 ...]] [--1 1 [1 ...]] [--2 2 [2 ...]]
                          [--3 3 [3 ...]] [--4 4 [4 ...]] [--5 5 [5 ...]]
                          [--6 6 [6 ...]] [--7 7 [7 ...]] [--8 8 [8 ...]]
                          [--9 9 [9 ...]] [--10 10 [10 ...]] [--11 11 [11 ...]]
                          [--12 12 [12 ...]] [--13 13 [13 ...]]
                          [--14 14 [14 ...]] [--15 15 [15 ...]]
                          [--16 16 [16 ...]] [--17 17 [17 ...]]
                          input_dir output_dir

Photogrammetry reconstruction with these steps:
    0. Intrinsics analysis             openMVG_main_SfMInit_ImageListing
    1. Compute features                openMVG_main_ComputeFeatures
    2. Compute pairs                   openMVG_main_PairGenerator
    3. Compute matches                 openMVG_main_ComputeMatches
    4. Filter matches                  openMVG_main_GeometricFilter
    5. Incremental reconstruction      openMVG_main_IncrementalSfM
    6. Global reconstruction           openMVG_main_GlobalSfM
    7. Colorize Structure              openMVG_main_ComputeSfM_DataColor
    8. Structure from Known Poses      openMVG_main_ComputeStructureFromKnownPoses
    9. Colorized robust triangulation  openMVG_main_ComputeSfM_DataColor
    10. Control Points Registration    ui_openMVG_control_points_registration
    11. Export to openMVS              openMVG_main_openMVG2openMVS
    12. Densify point-cloud            DensifyPointCloud
    13. Reconstruct the mesh           ReconstructMesh
    14. Refine the mesh                RefineMesh
    15. Texture the mesh               TextureMesh
    16. Estimate disparity-maps        DensifyPointCloud
    17. Fuse disparity-maps            DensifyPointCloud

positional arguments:
  input_dir                 the directory wich contains the pictures set.
  output_dir                the directory wich will contain the resulting files.

optional arguments:
  -h, --help                show this help message and exit
  --steps STEPS [STEPS ...] steps to process
  --preset PRESET           steps list preset in
                            SEQUENTIAL = [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15]
                            GLOBAL = [0, 1, 2, 3, 4, 6, 11, 12, 13, 14, 15]
                            MVG_SEQ = [0, 1, 2, 3, 4, 5, 7, 8, 9]
                            MVG_GLOBAL = [0, 1, 2, 3, 4, 6, 7, 8, 9]
                            MVS = [12, 13, 14, 15]
                            MVS_SGM = [16, 17]
                            default : SEQUENTIAL

Passthrough:
  Option to be passed to command lines (remove - in front of option names)
  e.g. --1 p ULTRA to use the ULTRA preset in openMVG_main_ComputeFeatures
"""

import os
import subprocess
import sys
from argparse import ArgumentParser, RawTextHelpFormatter


# add this script's directory to PATH
os.environ['PATH'] += ':' + os.path.dirname(os.path.abspath(__file__))

# add current directory to PATH
os.environ['PATH'] += ':' + os.getcwd()


def where_is(file):
    try:
        ret = subprocess.run(['which', file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
        return os.path.split(ret.stdout.decode())[0]
    except subprocess.CalledProcessError:
        return None


def find(file):
    """
        As whereis look only for executable on linux, this find look for all file type
    """
    for d in os.environ['PATH'].split(':'):
        if os.path.isfile(os.path.join(d, file)):
            return d
    return None


# Try to find openMVG and openMVS binaries in PATH
OPENMVG_BIN = where_is("openMVG_main_SfMInit_ImageListing")
OPENMVS_BIN = where_is("ReconstructMesh")

# Try to find openMVG camera sensor database
CAMERA_SENSOR_DB_FILE = "sensor_width_camera_database.txt"
CAMERA_SENSOR_DB_DIRECTORY = find(CAMERA_SENSOR_DB_FILE)

# Ask user for openMVG and openMVS directories if not found
if not OPENMVG_BIN:
    OPENMVG_BIN = input("openMVG binary folder?\n")
if not OPENMVS_BIN:
    OPENMVS_BIN = input("openMVS binary folder?\n")
if not CAMERA_SENSOR_DB_DIRECTORY:
    CAMERA_SENSOR_DB_DIRECTORY = input("openMVG camera database (%s) folder?\n" % CAMERA_SENSOR_DB_FILE)


PRESET = {'SEQUENTIAL': [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15],
          'GLOBAL': [0, 1, 2, 3, 4, 6, 11, 12, 13, 14, 15],
          'MVG_SEQ': [0, 1, 2, 3, 4, 5, 7, 8, 9, 11],
          'MVG_GLOBAL': [0, 1, 2, 3, 4, 6, 7, 8, 9, 11],
          'MVS': [12, 13, 14, 15],
          'MVS_SGM': [16, 17]}

PRESET_DEFAULT = "SEQUENTIAL"

# HELPERS for terminal colors
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
NO_EFFECT, BOLD, UNDERLINE, BLINK, INVERSE, HIDDEN = (0, 1, 4, 5, 7, 8)


# from Python cookbook, #475186
def has_colours(stream):
    """
        Return stream colours capability
    """
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False  # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except Exception:
        # guess false in case of error
        return False


HAS_COLOURS = has_colours(sys.stdout)


def printout(text, colour=WHITE, background=BLACK, effect=NO_EFFECT):
    """
        print() with colour
    """
    if HAS_COLOURS:
        seq = "\x1b[%d;%d;%dm" % (effect, 30+colour, 40+background) + text + "\x1b[0m"
        sys.stdout.write(seq+'\r\n')
    else:
        sys.stdout.write(text+'\r\n')


# OBJECTS to store config and data in
class ConfContainer:
    """
        Container for all the config variables
    """
    def __init__(self):
        pass


class AStep:
    """ Represents a process step to be run """
    def __init__(self, info, cmd, opt):
        self.info = info
        self.cmd = cmd
        self.opt = opt


class StepsStore:
    """ List of steps with facilities to configure them """
    def __init__(self):
        self.steps_data = [
            ["Intrinsics analysis",          # 0
             os.path.join(OPENMVG_BIN, "openMVG_main_SfMInit_ImageListing"),
             ["-i", "%input_dir%", "-o", "%matches_dir%", "-d", "%camera_file_params%"]],
            ["Compute features",             # 1
             os.path.join(OPENMVG_BIN, "openMVG_main_ComputeFeatures"),
             ["-i", "%matches_dir%/sfm_data.json", "-o", "%matches_dir%", "-m", "SIFT"]],
            ["Compute pairs",                # 2
             os.path.join(OPENMVG_BIN, "openMVG_main_PairGenerator"),
             ["-i", "%matches_dir%/sfm_data.json", "-o", "%matches_dir%/pairs.bin"]],
            ["Compute matches",              # 3
             os.path.join(OPENMVG_BIN, "openMVG_main_ComputeMatches"),
             ["-i", "%matches_dir%/sfm_data.json", "-p", "%matches_dir%/pairs.bin", "-o", "%matches_dir%/matches.putative.bin", "-n", "AUTO"]],
            ["Filter matches",               # 4
             os.path.join(OPENMVG_BIN, "openMVG_main_GeometricFilter"),
             ["-i", "%matches_dir%/sfm_data.json", "-m", "%matches_dir%/matches.putative.bin", "-o", "%matches_dir%/matches.f.bin"]],
            ["Incremental reconstruction",   # 5
             os.path.join(OPENMVG_BIN, "openMVG_main_SfM"),
             ["-i", "%matches_dir%/sfm_data.json", "-m", "%matches_dir%", "-o", "%reconstruction_dir%", "-s", "INCREMENTAL"]],
            ["Global reconstruction",        # 6
             os.path.join(OPENMVG_BIN, "openMVG_main_SfM"),
             ["-i", "%matches_dir%/sfm_data.json", "-m", "%matches_dir%", "-o", "%reconstruction_dir%", "-s", "GLOBAL", "-M", "%matches_dir%/matches.e.bin"]],
            ["Colorize Structure",           # 7
             os.path.join(OPENMVG_BIN, "openMVG_main_ComputeSfM_DataColor"),
             ["-i", "%reconstruction_dir%/sfm_data.bin", "-o", "%reconstruction_dir%/colorized.ply"]],
            ["Structure from Known Poses",   # 8
             os.path.join(OPENMVG_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),
             ["-i", "%reconstruction_dir%/sfm_data.bin", "-m", "%matches_dir%", "-f", "%matches_dir%/matches.f.bin", "-o", "%reconstruction_dir%/robust.bin"]],
            ["Colorized robust triangulation",  # 9
             os.path.join(OPENMVG_BIN, "openMVG_main_ComputeSfM_DataColor"),
             ["-i", "%reconstruction_dir%/robust.bin", "-o", "%reconstruction_dir%/robust_colorized.ply"]],
            ["Control Points Registration",  # 10
             os.path.join(OPENMVG_BIN, "ui_openMVG_control_points_registration"),
             ["-i", "%reconstruction_dir%/sfm_data.bin"]],
            ["Export to openMVS",            # 11
             os.path.join(OPENMVG_BIN, "openMVG_main_openMVG2openMVS"),
             ["-i", "%reconstruction_dir%/sfm_data.bin", "-o", "\"%mvs_dir%/scene.mvs\"", "-d", "\"%mvs_dir%/images\""]],
            ["Densify point cloud",          # 12
             os.path.join(OPENMVS_BIN, "DensifyPointCloud"),
             ["scene.mvs", "--dense-config-file", "Densify.ini", "--resolution-level", "1", "--number-views", "8", "-w", "\"%mvs_dir%\""]],
            ["Reconstruct the mesh",         # 13
             os.path.join(OPENMVS_BIN, "ReconstructMesh"),
             ["scene_dense.mvs", "-w", "\"%mvs_dir%\""]],
            ["Refine the mesh",              # 14
             os.path.join(OPENMVS_BIN, "RefineMesh"),
             ["scene_dense_mesh.mvs", "--scales", "1", "--gradient-step", "25.05", "-w", "\"%mvs_dir%\""]],
            ["Texture the mesh",             # 15
             os.path.join(OPENMVS_BIN, "TextureMesh"),
             ["scene_dense_mesh_refine.mvs", "--decimate", "0.5", "-w", "\"%mvs_dir%\""]],
            ["Estimate disparity-maps",      # 16
             os.path.join(OPENMVS_BIN, "DensifyPointCloud"),
             ["scene.mvs", "--dense-config-file", "Densify.ini", "--fusion-mode", "-1", "-w", "\"%mvs_dir%\""]],
            ["Fuse disparity-maps",          # 17
             os.path.join(OPENMVS_BIN, "DensifyPointCloud"),
             ["scene.mvs", "--dense-config-file", "Densify.ini", "--fusion-mode", "-2", "-w", "\"%mvs_dir%\""]]
            ]

    def __getitem__(self, indice):
        return AStep(*self.steps_data[indice])

    def length(self):
        return len(self.steps_data)

    def apply_conf(self, conf):
        """ replace each %var% per conf.var value in steps data """
        for s in self.steps_data:
            o2 = []
            for o in s[2]:
                co = o.replace("%input_dir%", conf.input_dir)
                co = co.replace("%output_dir%", conf.output_dir)
                co = co.replace("%matches_dir%", conf.matches_dir)
                co = co.replace("%reconstruction_dir%", conf.reconstruction_dir)
                co = co.replace("%mvs_dir%", conf.mvs_dir)
                co = co.replace("%camera_file_params%", conf.camera_file_params)
                o2.append(co)
            s[2] = o2


def mkdir_ine(dirname):
    """Create the folder if not presents"""
    if not os.path.exists(dirname):
        os.mkdir(dirname)


def create_program(steps: StepsStore) -> ArgumentParser:
    parser = ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="Photogrammetry reconstruction with these steps: \r\n" +
                    "\r\n".join(("\t%i. %s\t %s" % (t, steps[t].info, steps[t].cmd) for t in range(steps.length())))
    )
    parser.add_argument('input_dir',
                        help="the directory wich contains the pictures set.")
    parser.add_argument('output_dir',
                        help="the directory wich will contain the resulting files.")
    parser.add_argument('--steps', type=int, nargs="+",
                        help="steps to process")
    parser.add_argument('--preset',
                        help="steps list preset in \r\n" +
                             " \r\n".join([k + " = " + str(PRESET[k]) for k in PRESET]) +
                             " \r\ndefault : " + PRESET_DEFAULT)

    group = parser.add_argument_group('Passthrough',
                                      description="Option to be passed to command lines"
                                                  " (remove - in front of option names)\r\n"
                                                  "e.g. --1 p ULTRA to use the ULTRA preset"
                                                  " in openMVG_main_ComputeFeatures")
    for n in range(steps.length()):
        group.add_argument('--' + str(n), nargs='+')

    return parser


if __name__ == '__main__':
    config = ConfContainer()
    steps = StepsStore()
    debug = False

    program = create_program(StepsStore())
    program.parse_args(namespace=config)  # store args in the ConfContainer

    # Absolute path for input and ouput dirs
    config.input_dir = os.path.abspath(config.input_dir)
    config.output_dir = os.path.abspath(config.output_dir)

    if not os.path.exists(config.input_dir):
        sys.exit("%s: path not found" % config.input_dir)

    config.reconstruction_dir = os.path.join(config.output_dir, "sfm")
    config.matches_dir = os.path.join(config.reconstruction_dir, "matches")
    config.mvs_dir = os.path.join(config.output_dir, "mvs")
    config.camera_file_params = os.path.join(CAMERA_SENSOR_DB_DIRECTORY, CAMERA_SENSOR_DB_FILE)

    mkdir_ine(config.output_dir)
    mkdir_ine(config.reconstruction_dir)
    mkdir_ine(config.matches_dir)
    mkdir_ine(config.mvs_dir)

    # Update directories in steps commandlines
    steps.apply_conf(config)

    # PRESET
    if config.steps and config.preset:
        sys.exit("Steps and preset arguments can't be set together.")
    elif config.preset:
        try:
            config.steps = PRESET[config.preset]
        except KeyError:
            sys.exit("Unkown preset %s, choose %s" % (config.preset, ' or '.join([s for s in PRESET])))
    elif not config.steps:
        config.steps = PRESET[PRESET_DEFAULT]

    # WALK
    print("# Using input dir:  %s" % config.input_dir)
    print("#      output dir:  %s" % config.output_dir)
    print("# Steps:  %s" % str(config.steps))

    if 4 in config.steps:    # GeometricFilter
        if 6 in config.steps:  # GlobalReconstruction
            # Set the geometric_model of ComputeMatches to Essential
            steps[4].opt = steps[4].opt.replace("/matches.f.bin", "/matches.e.bin")
            steps[4].opt.extend(["-g", "e"])

    for cstep in config.steps:
        printout("#%i. %s" % (cstep, steps[cstep].info), effect=INVERSE)

        # Retrieve "passthrough" commandline options
        opt = getattr(config, str(cstep))
        if opt:
            # add - sign to short options and -- to long ones
            for o in range(0, len(opt), 2):
                if len(opt[o]) > 1:
                    opt[o] = '-' + opt[o]
                opt[o] = '-' + opt[o]
        else:
            opt = []

        # Remove STEPS[cstep].opt options now defined in opt
        for anOpt in steps[cstep].opt:
            if anOpt in opt:
                idx = steps[cstep].opt.index(anOpt)
                if debug:
                    print('#\tRemove ' + str(anOpt) + ' from defaults options at id ' + str(idx))
                del steps[cstep].opt[idx:idx+2]

        # create a commandline for the current step
        cmdline = [steps[cstep].cmd] + steps[cstep].opt + opt
        print('Cmd: ' + ' '.join(cmdline))

        if not debug:
            # Launch the current step
            try:
                pStep = subprocess.Popen(cmdline)
                pStep.wait()
                if pStep.returncode != 0:
                    break
            except KeyboardInterrupt:
                sys.exit('\r\nProcess canceled by user, all files remains')
        else:
            print('\t'.join(cmdline))

    printout("# Pipeline end #", effect=INVERSE)
