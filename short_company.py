def short_company(C, P, n, k):
    '''
    Input:  C | Tuple of s = |C| strings representing names of companies
            P | Tuple of s lists each of size nk representing prices
            n | Number of days of price information
            k | Number of prices in one day
    Output: c | Name of a company with highest shorting value
            S | List containing a longest subsequence of 
              | decreasing prices from c that doesn't skip days
    '''
    
    def decreasing(lst,n,k):
        a = len(lst)
        x=[]
        sub = [1 for i in range(n*k)]
        best=-1
        parents={}
        print (a==n*k-1)
        for i in reversed(range(n*k-1)):
            for j in range(i+1, min((i+2*k-i%k),n*k)):
                if lst[j] < lst[i] and sub[j]+1>sub[i]:
                    sub[i]=sub[j]+1
                    if sub[j]+1>sub[best]:
                        best=i
                    parents[i]=j
        while best in parents:
            x.append(lst[best])
            best=parents[best]
        x.append(lst[best])       
        return x
    
    
    
    seq=[]
    lengths=[]
    for i in range(len(P)):
        sequence=decreasing(P[i],n,k)
        seq.append(sequence)
        lengths.append(len(sequence))
    maxlst=max(lengths)
    for i in range(len(seq)):
        if len(seq[i])==maxlst:
            c=C[i]
            S=seq[i]
            print(c,S)
    return (c, S)
