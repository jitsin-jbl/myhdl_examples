#
# Copyright (c) 2008-2012 Christopher L. Felton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The following table is used to determine the number of BRAM blocks
# used for a device.
XBram = {'XC3S500E' :       # Spartan 3E device
         {'bpb'   : 2048*8, # bits per BRAM
          'total' : 20      # Total number of BRAM available
          },
         'XC6S'  :          # Spartan 6 device
         {'bpb'   : 2048*8, # bits per BRAM
          'total' : 32      # Total number of BRAM available
         }
        }
