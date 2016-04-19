
    @always_seq(clock.posedge, reset=reset)
    def rtl():
        # tap update loop
        xd[0].next = x
        for ii in range(1, len(h)):
            xd[ii].next = xd[ii-1]
            
	# sum-of-products loop
        sop = 0
        for ii in range(len(h)):
            c = h[ii]
            sop = sop + (c * xd[ii])

	# scale the sum of products to the 
        # output range (truncate)
        y.next = sop >> scale
