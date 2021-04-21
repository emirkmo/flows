from functools import wraps

import numpy as np

from astropy.modeling import fitting

from photutils.psf import EPSFFitter, BasicPSFPhotometry, DAOGroup, extract_stars

class BasicPSFPhotometry(BasicPSFPhotometry):

    def nstar(self, image, star_groups):

        if not type(self.fitter) is fitting.LevMarLSQFitter:

            return super().nstar(image, star_groups)

        def fitter(func):

            @wraps(func)
            def wrapper(group_psf, x, y, image):

                weights = self._weights[y, x]
                return func(group_psf, x, y, image, weights=weights)

            return wrapper

        self.fitter = fitter(self.fitter)
        res = super().nstar(image, star_groups)
        self.fitter = self.fitter.__wrapped__

        return res

    def __call__(self, image, init_guesses=None, weights=None):

        self._weights = weights if not weights is None else np.ones_like(image)

        # XXX because we have to check all kinds of "masks"
        self._weights[np.ma.array(image).mask] = 0
        self._weights[~np.isfinite(image)] = 0
        self._weights[~np.isfinite(self._weights)] = 0

        return super().__call__(image, init_guesses)
