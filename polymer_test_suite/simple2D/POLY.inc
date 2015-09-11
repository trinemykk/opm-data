-- This reservoir simulation deck is made available under the Open Database
-- License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in
-- individual contents of the database are licensed under the Database Contents
-- License: http://opendatacommons.org/licenses/dbcl/1.0/

-- Copyright (C) 2015 Statoil
-- Copyright (C) 2015 SINTEF ICT, Applied Mathematics

NOECHO
PLYVISC
0    1.0
0.5  3.5
1.0  6.4
1.5  12.4
2.0  24.7
3.0  50.0 /


PLYROCK
--IPV  RRF  dens  AI  max ads
 0.05 1.3  2650   2 0.000020 /


PLYADS
-- conc  adsorb-conc
 0.000   0.000000
 0.250   0.000011
 0.500   0.000015
 0.750   0.000017
 1.000   0.000018
 1.250   0.000019
 1.500   0.000019
 1.750   0.000020
 2.000   0.000020
 3.000   0.000020 /

PLMIXPAR
 1.0  /

PLYMAX
 3.00  0  /

ECHO
