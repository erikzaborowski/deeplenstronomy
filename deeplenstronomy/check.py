# A module to check for user errors in the main config file

from deeplenstronomy.utils import KeyPathDict 
import sys

class ConfigFileError(Exception): pass

class AllChecks():
    """
    Define new checks as methods starting with 'check_'
    Methods must return err_code, err_message where
    err_code == 0 means success and err_code != 0 means failure
    If failure, the err_message is printed and sys.exit() is called
    """
    
    def __init__(self, full_dict, config_dict):
        """
        Trigger the running of all checks
        """
        # convert to KeyPathDict objects for easier parsing
        kp_f = KeyPathDict(full_dict, keypath_separator='.')
        self.full = kp_f
        self.full_keypaths = kp_f.keypaths()
        kp_c = KeyPathDict(config_dict, keypath_separator='.')
        self.config = kp_c
        self.config_keypaths = kp_c.keypaths()

        # find all check functions
        self.checks = [x for x in dir(self) if x.find('check_') != -1]

        # run checks
        total_errs = []
        for check in self.checks:

            try:
                err_messages = eval('self.' + check + '()')
            except Exception:
                err_messages = ["CheckFunctionError: " + check] 

            total_errs += err_messages

        # report errors to user
        if len(total_errs) != 0:
            kind_output(total_errs)
            raise ConfigFileError

        return

    ### Helper methods
    @staticmethod
    def config_dict_format(*args):
        return "['" + "']['".join(list(args)) + "']"

    def config_lookup(self, lookup_str):
        return eval("self.config_dict" + lookup_str)
    
    ### Check functions
    def check_top_level_existence(self):
        errs = []
        for name in ['DATASET', 'SURVEY', 'IMAGE', 'COSMOLOGY', 'SPECIES', 'GEOMETRY']:
            if name not in self.full.keys():
                errs.append("Missing {0} section from config file".format(name))
        return errs

    def check_low_level_existence(self):
        errs = []
        param_names = {"DATASET.NAME",
                       "DATASET.PARAMETERS.SIZE",
                       "COSMOLOGY.PARAMETERS.H0",
                       "COSMOLOGY.PARAMETERS.Om0",
                       "IMAGE.PARAMETERS.exposure_time",
                       "IMAGE.PARAMETERS.numPix",
                       "IMAGE.PARAMETERS.pixel_scale",
                       "IMAGE.PARAMETERS.psf_type",
                       "IMAGE.PARAMETERS.read_noise",
                       "IMAGE.PARAMETERS.ccd_gain",
                       "SURVEY.PARAMETERS.BANDS",
                       "SURVEY.PARAMETERS.seeing",
                       "SURVEY.PARAMETERS.magnitude_zero_point",
                       "SURVEY.PARAMETERS.sky_brightness",
                       "SURVEY.PARAMETERS.num_exposures"}
        for param in param_names:
            try:
                config_obj = self.config_lookup(self.config_dict_format(param.split('.')))
            except KeyError:
                errs.append(param + "is missing from the Config File")

        return errs

    def check_not_allowed_to_be_drawn_from_a_distribution(self):
        errs = []
        param_names = {"DATASET.NAME",
                       "DATASET.PARAMETERS.SIZE",
                       "DATASET.PARAMETERS.OUTDIR",
                       "IMAGE.PARAMETERS.numPix",
                       "COSMOLOGY.PARAMETERS.H0",
                       "COSMOLOGY.PARAMETERS.Om0",
                       "COSMOLOGY.PARAMETERS.Tcmb0",
                       "COSMOLOGY.PARAMETERS.Neff",
                       "COSMOLOGY.PARAMETERS.m_nu",
                       "COSMOLOGY.PARAMETERS.Ob0"}
        for param in param_names:
            try:
                config_obj = self.config_lookup(self.config_dict_format(param.split('.')))
            except KeyError:
                # The checked parameter was not in the config dict
                continue
            
            if isinstance(config_obj, dict):
                errs.append(param + " cannot be drawn from a distribution")
        return errs

    def check_valid_geometry(self):
        errs = []

        # There must be at least one configuration
        if len(list(self.config_dict['GEOMETRY'].keys())) == 0:
            errs.append("GEOMETRY sections needs at least one CONFIGURATION")
        
        # Check keys
        detected_configurations, detected_noise_sources, fractions = [], [], []
        for k in self.config_dict['GEOMETRY'].keys():
            if not k.startswith('CONFIGURATION_'):
                errs.append('GEOMETRY.' + k + ' is an invalid Config File entry')

            # Configurations must be indexed with a valid integer
            try:
                val = int(k.split('_')[-1])
                if val < 1:
                    errs.append('GEOMETRY.' + k + ' is an invalid Config File entry')
                detected_configurations.append(val)
            except TypeError:
                errs.append('GEOMETRY.' + k + ' needs a valid integer index greater than zero')

            # Every configuration needs a FRACTION that is a valid float
            if "FRACTION" not in self.config_dict['GEOMETRY'][k].keys():
                errs.append("GEOMETRY." + k " .FRACTION is missing")
            else:
                try:
                    fraction = float(self.config_dict['GEOMETRY'][k]['FRACTION'])
                    fractions.append(fraction)
                except TypeError:
                    errs.append("GEOMETRY." + k " .FRACTION must be a float")

            # Configurations must have at least one plane
            if len(list(self.config_dict['GEOMETRY'][k].keys())) == 0:
                errs.append("CEOMETRY." + k + " must have at least one PLANE")

            detected_planes = []
            for config_k in self.config_dict['GEOMETRY'][k].keys():
                # check individual plane properties
                if config_k.startswith('PLANE_'):
                    # Plane index must be a valid integer
                    try:
                        val = int(config_k.split('_')[-1])
                        if val < 1:
                            errs.append('GEOMETRY.' + k + '.' + config_k + ' is an invalid Config File entry')
                        detected_planes.append(val)
                    except TypeError:
                        errs.append('GEOMETRY.' + k + '.' + config_k + ' needs a valid integer index greater than zero')

                    # Plane must have a redshift
                    if 'REDSHIFT' not in config_k in self.config_dict['GEOMETRY'][k][config_k]['PARAMETERS'].keys():
                        errs.append('REDSHIFT is missing from GEOMETRY.' + k + '.' + config_k)

                    detected_objects = []
                    for obj_k in self.config_dict['GEOMETRY'][k][config_k].keys():
                        # check individual object properties
                        if obj_k.startswith('OBJECT_'):
                            # Object index must be a valid integer
                            try:
                                val = int(obj_k.split('_')[-1])
                                if val < 1:
                                    errs.append('GEOMETRY.' + k + '.' + config_k + '.' + obj_k + ' is an invalid Config File entry')
                                detected_objects.append(val)
                            except TypeError:
                                errs.append('GEOMETRY.' + k + '.' + config_k + '.' + obj_k + ' needs a valid integer index greater than zero')

                            # Objects must have a value that appears in the species section
                            if not isinstance(self.config_dict['GEOMETRY'][k][config_k][obj_k], str):
                                errs.append('GEOMETRY.' + k + '.' + config_k + '.' + obj_k + ' must be a single name')

                            species_paths = [x for x in self.config if x.startswith('SPECIES') and x.find('.' + self.config_dict['GEOMETRY'][k][config_k][obj_k] + '.') != -1]
                            if len(species_paths) == 0:
                                errs.append('GEOMETRY.' + k + '.' + config_k + '.' + obj_k + ' is missing from the SPECIES section')
                                
                    # Objects must be indexed sequentially
                    if len(detected_objects) != max(detected_objects):
                        errs.append("OBJECTs in the GEOMETRY." + k + '.' + config_k + " section must be indexed as 1, 2, 3, ...")

                # check noise properties
                elif config_k.startswith('NOISE_SOURCE_'):
                    # index must be a valid integer
                    try:
                        val = int(obj_k.split('_')[-1])
                        if val < 1:
                            errs.append('GEOMETRY.' + k + '.' + config_k + ' is an invalid Config File entry')
                        detected_noise_sources.append(val)
                    except TypeError:
                        errs.append('GEOMETRY.' + k + '.' + config_k + ' needs a valid integer index greater than zero')

                    # Noise sources must have a single value that appears i the species section
                    if not isinstance(self.config_dict['GEOMETRY'][k][config_k], str):
                        errs.append('GEOMETRY.' + k + '.' + config_k + ' must be a single name')

                    species_paths = [x for x in self.config if x.startswith('SPECIES') and x.find('.' + self.config_dict['GEOMETRY'][k][config_k] + '.') != -1]
                    if len(species_paths) == 0:
                        errs.append('GEOMETRY.' + k + '.' + config_k + ' is missing from the SPECIES section')
                        
                # check timeseries properties
                elif config_k == 'TIMESERIES':
                    # Must have objects as keys
                    if "OBJECTS" not in self.config_dict['GEOMETRY'][k][config_k].keys():
                        errs.append("GEOMETRY." + k + ".TIMESERIES is missing the OBJECTS parameter")
                    else:
                        if not isinstance(self.config_dict['GEOMETRY'][k][config_k]["OBJECTS"], list):
                            errs.append("GEOMETRY." + k + ".TIMESERIES.OBJECTS must be a list")
                        else:
                            # listed objects must appear in species section, in the configuration, and have a model defined
                            for obj in self.config_dict['GEOMETRY'][k][config_k]['OBJECTS']:
                                species_paths = [x for x in self.config if x.startswith('SPECIES') and x.find('.' + obj + '.') != -1]
                                if len(species_paths) == 0:
                                    errs.append(obj + "in GEOMETRY." + k + ".TIMESERIES.OBJECTS is missing from the SPECIES section")
                                elif "MODEL" not in config_lookup(config_dict_format(species_paths[0].split('.'))).keys():
                                    errs.append("MODEL for " + obj + " in GEOMETRY." + k + ".TIMESERIES.OBJECTS is missing from the SPECIES section")
                                configuration_paths = [x for x in self.config if x.startswith('GEOMETRY.' + k + '.') and x.find('.' + obj + '.') != -1]
                                if len(configuration_paths) == 0:
                                    errs.append(obj + " in GEOMETRY." + k + ".TIMESERIES.OBJECTS is missing from GEOMETRY." + k)
                        
                    # Must have nites as keys
                    if "NITES" not in self.config_dict['GEOMETRY'][k][config_k].keys():
                        errs.append("GEOMETRY." + k + ".TIMESERIES is missing the NITES parameter")
                    else:
                        if not isinstance(self.config_dict['GEOMETRY'][k][config_k]["NITES"], list):
                            errs.append("GEOMETRY." + k + ".TIMESERIES.NITES must be a list")
                        else:
                            # listed nights must be numeric
                            try:
                                nites = [int(float(x)) for x in self.config_dict['GEOMETRY'][k][config_k]["NITES"]]
                                del nites
                            except TypeError:
                                errs.append("Listed NITES in GEOMETRY." + k + ".TIMESERIES.NITES must be numeric")
                        
                # unexpected entry
                else:
                    errs.append('GEOMETRY.' + k + '.' + config_k + ' is not a valid entry')
    
            # Planes must be indexed sequentially
            if len(detected_planes) != max(detected_planes):
                errs.append("PLANEs in the GEOMETRY." + k + " section must be indexed as 1, 2, 3, ...")

            # Noise sources must be indexed sequentially    
            if len(detected_noise_sources) != max(detected_noise_sources):
                errs.append("NOISE_SOURCEs in the GEOMETRY." + k + " section must be indexed as 1, 2, 3, ...")
                    
                    
        # Configurations must be indexed sequentially
        if len(detected_configurations) != max(detected_configurations):
            errs.append("CONFIGURATIONs in the GEOMETRY section must be indexed as 1, 2, 3, ...")

        # Fractions must sum to a number between 0.0 and 1.0
        if not (0.0 < sum(fractions) <= 1.0):
            errs.append("CONFIGURATION FRACTIONs must sum to a number between 0.0 and 1.0")
                
        return errs
    
    # End check functions

def kind_output(errs):
    """
    Print all detected errors in the configuration file to the screen
    """
    for err in errs:
        print(err)
    return


def run_checks(full_dict, config_dict):
    """
    Instantiate an AllChecks object to run checks

    :param full_dict: a Parser.full_dict object
    :param config_dict: a Parser.config_dict object
    """
    try:
        check_runner = AllChecks(full_dict, config_dict)
    except ConfigFileError:
        print("Fatal error(s) detected in config file. Please edit and rerun.")
        sys.exit()

        
