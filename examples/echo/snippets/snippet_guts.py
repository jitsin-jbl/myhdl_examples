
if(rd_ptr != wr_ptr) :
    rd_ptr.next = wr_ptr
else:
    # Register the inputs
    _fs.next = au_fs
    _in.next = au_in
    
    if _fs:
        # Scale the echo (buffered) samples
        mem[wr_ptr].next = _in >> (ScaleShift + EchoShift)
        
        # Update pointers to delay buffer
        wr_ptr.next = (wr_ptr + 1) % C_BD
        rd_ptr.next = (wr_ptr + 1) % C_BD
        
        # Output register 1, scale back to 24 bits (shifts in hw)
        _out.next = mem[rd_ptr] << (ScaleShift)
            
    # Output register 2, 
    au_out.next = _in + (_out)

