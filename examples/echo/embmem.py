

EmbeddedMemory = {
    'xilinx' : {'XC3S500E' :       # Spartan 3E device
                {'bpb'   : 2048*8, # bits per BRAM
                 'total' : 20      # Total number of BRAM available
                 },
                'XC6S'  :          # Spartan 6 device
                {'bpb'   : 2048*8, # bits per BRAM
                 'total' : 32      # Total number of BRAM available
                 }
                },

    'lattice' : {'ECP4-50'  :       # Lattice ECP4 Device
                 {'bpb'   : 2304*8, # bits per BRAM
                  'total' : 64      # Total number of BRAM available
                  }
                 },

    'altera' : {'EP4CE30' :        # Altera
                {'bpb'   : 1024*8, # bits per BRAM
                 'total' : 72      # Total number of BRAM available
                 },
                },
}
