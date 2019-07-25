import numpy as np
from lenstronomy.SimulationAPI.sim_api import SimAPI


class Population():

    def __int__(self):
        pass

    def draw_source_model(self):
        """
        draws source model from population
        """
        source_center_x = (np.random.rand() - 0.5) * 2
        source_center_y = (np.random.rand() - 0.5) * 2
        kwargs_source_mag = [{'magnitude': 22, 'R_sersic': 0.3, 'n_sersic': 1, 'e1': -0.3, 'e2': -0.2, 'center_x': source_center_x, 'center_y': source_center_y}]
        source_model_list = ['SERSIC_ELLIPSE']
        return kwargs_source_mag, source_model_list

    def draw_lens_model(self):
        """
        draw lens model parameters
        return: lens model keyword argument list, lens model list
        """
        theta_E = np.random.uniform(0.9, 2.2)
        lens_e1 = (np.random.rand() - 0.5) * 0.8
        lens_e2 = (np.random.rand() - 0.5) * 0.8
        kwargs_lens = [
        {'theta_E': theta_E, 'e1': lens_e1, 'e2': lens_e2, 'center_x': 0, 'center_y': 0},  # SIE model
        {'e1': 0.03, 'e2': 0.01}  # SHEAR model
        ]
        lens_model_list = ['SIE', 'SHEAR']
        return kwargs_lens, lens_model_list

    def draw_physical_model(self):
        """
        draw physical model parameters
        :return: return lens model keyword argument list, lens model list
        """
        from astropy.cosmology import FlatLambdaCDM
        from lenstronomy.SimulationAPI.model_api import ModelAPI

        # redshift
        z_lens = np.random.uniform(0.1, 10.)
        z_source = np.random.uniform(0.1, 10.)
        z_source_convention = 3.

        # cosmology
        omega_m = np.random.uniform(1e-9, 1)
        H0 = 70.
        omega_bar = 0.0
        cosmo = FlatLambdaCDM(H0=H0, Om0=omega_m, Ob0=omega_bar)

        # Lens physical parameters: Alternative A
        sigma_v = np.random.uniform(10., 1000.)
        lens_e1 = (np.random.uniform() - 0.5) * 0.8
        lens_e2 = (np.random.uniform() - 0.5) * 0.8

        # Lens physical parameters: Alternative B
        mass_scale = 1.e13
        M200 = np.random.uniform(1., 100) * mass_scale
        concentration = np.random.uniform(1, 7)

        # Models
        lens_model_list = ['SIE', 'SHEAR']

        # kwargs: this is for single-plane lensing
        kwargs_model_lensing = {
                                'lens_model_list': lens_model_list,  # list of lens models to be used
                                'z_lens': z_lens,  # list of redshift of the deflections
                                'z_source': z_source, # redshift of the default source (if not further specified by 'source_redshift_list') and also serves as the redshift of lensed point sources
                                'z_source_convention': z_source_convention, # source redshfit to which the reduced deflections are computed, is the maximal redshift of the ray-tracing
                                'cosmo': cosmo  # astropy.cosmology instance
                                }
        # kwargs: mass
        kwargs_mass = [{'sigma_v': sigma_v, 'center_x': 0, 'center_y': 0, 'e1': lens_e1, 'e2': lens_e2},
                       {'M200': M200, 'concentration': concentration, 'center_x': 0, 'center_y': 0}]

        # Model API
        sim = ModelAPI(**kwargs_model_lensing)

        # convert from physical values to reduced lensing values
        kwargs_lens = sim.physical2lensing_conversion(kwargs_mass=kwargs_mass)


        return kwargs_lens, lens_model_list

    def draw_lens_light(self):
        """

        :return:
        """
        lens_light_model_list = ['SERSIC_ELLIPSE']
        kwargs_lens_light = [{'magnitude': 22, 'R_sersic': 0.3, 'n_sersic': 1, 'e1': -0.3, 'e2': -0.2, 'center_x': 0, 'center_y': 0}]
        return kwargs_lens_light, lens_light_model_list

    def draw_point_source(self, center_x, center_y):
        """

        :param center_x: center of point source in source plane
        :param center_y: center of point source in source plane
        :return:
        """
        point_source_model_list = ['SOURCE_POSITION']
        kwargs_ps = [{'magnitude': 21, 'ra_source': center_x, 'dec_source': center_y}]
        return kwargs_ps, point_source_model_list

    def _simple_draw(self, with_lens_light=False, with_quasar=False,  **kwargs):
        """

        :param with_lens_light:
        :param with_quasar:
        :param kwargs:
        :return:
        """

        # lens
        kwargs_lens, lens_model_list = self.draw_lens_model()
        kwargs_params = {'kwargs_lens': kwargs_lens}
        kwargs_model = {'lens_model_list': lens_model_list}

        # source
        kwargs_source, source_model_list = self.draw_source_model()
        kwargs_params['kwargs_source_mag'] = kwargs_source
        kwargs_model['source_light_model_list'] = source_model_list

        # for toggling with injection simulations
        if with_lens_light:
            kwargs_lens_light, lens_light_model_list = self.draw_lens_light()
            kwargs_params['kwargs_lens_light_mag'] = kwargs_lens_light
            kwargs_model['lens_light_model_list'] = lens_light_model_list
        # for toggling a quasar
        if with_quasar:
            kwargs_ps, point_source_model_list = self.draw_point_source(center_x=kwargs_source[0]['center_x'],
                                                                        center_y=kwargs_source[0]['center_y'])
            kwargs_params['kwargs_ps_mag'] = kwargs_ps
            kwargs_model['point_source_model_list'] = point_source_model_list

        return kwargs_params, kwargs_model


    def _complex_draw(self, **kwargs):
        """

        :param with_lens_light:
        :param with_quasar:
        :param kwargs:
        :return:
        """

        kwargs_lens, lens_model_list, kwargs_source, source_model_list = self.draw_physical_model()
        kwargs_params = {'kwargs_lens': kwargs_lens,
                         'kwargs_source_mag': kwargs_source}
        kwargs_model = {'lens_model_list': lens_model_list,
                        'source_light_model_list': source_model_list}

        # for toggling with injection simulations
        if with_lens_light:
            kwargs_lens_light, lens_light_model_list = self.draw_lens_light()
            kwargs_params['kwargs_lens_light_mag'] = kwargs_lens_light
            kwargs_model['lens_light_model_list'] = lens_light_model_list
        # for toggling a quasar
        if with_quasar:
            kwargs_ps, point_source_model_list = self.draw_point_source(center_x=kwargs_source[0]['center_x'],
                                                                        center_y=kwargs_source[0]['center_y'])
            kwargs_params['kwargs_ps_mag'] = kwargs_ps
            kwargs_model['point_source_model_list'] = point_source_model_list
        return kwargs_params, kwargs_model

        return kwargs_params, kwargs_model


    def draw_model(self, with_lens_light=False, with_quasar=False, mode='simple', **kwargs):
        """
        returns all keyword arguments of the model

        :param kwargs:
        :return: kwargs_params, kwargs_model
        """
        if mode == 'simple':
            return self._simple_draw(with_lens_light, with_quasar, **kwargs)
        if mode == 'complex':
            return self._complex_draw(**kwargs)
        else:
            raise ValueError('mode %s is not supported!' % mode)
