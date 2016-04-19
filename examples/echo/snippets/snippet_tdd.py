

for iis in xrange(len(svi)):
    au_in.next = int(svi[iis])
    yield au_fs.posedge
    svo[iis] = int(au_out)

# Only checking that the expected delay is non-zero
assert svo[plsi+BD] > 0,   '1 Echo failed svo[%d] == %d' % (plsi+BD, svo[plsi+BD])
assert svo[plsi+BD+1] < 0, '2 Echo failed svo[%d] == %d' % (plsi+BD+1, svo[plsi+BD+1])
        
