[U,S,V] = svd(A);
T=S;
T(find(S~=0)) = 1./S(find(S~=0));
svdInvA = V * T' * U';