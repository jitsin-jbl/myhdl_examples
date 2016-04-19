pix_t median(pix_t window[N])
{
    pix_t t[N], z[N];
    int ii, k, stage;
  
    // copy locally
    for(ii=0; ii<N; ii++) z[ii] = window[ii];
  
    for(stage=1; stage<=N; stage++){
        k = (stage%2==1) ? 0 : 1;
        for(ii=k; ii<N-1; ii++){
          t[ii] = MIN(z[ii], z[ii+1]);
          t[ii+1] = MAX(z[ii], z[ii+1]);
          z[ii] = t[ii];
          z[ii+1] = t[ii+1];
        }
      }

    return z[N/2];
}