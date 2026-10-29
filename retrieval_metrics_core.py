"""Metric calculations used in the Phase 1 image-retrieval extension.
No raw images, secrets, or fabricated experiment results in this file."""
import numpy as np

def retrieval_metrics(query_embeddings, gallery_embeddings, query_labels, gallery_labels, k=10):
    """Evaluate labeled cosine similarity, returning per-query metrics and ranked indices.
    Embeddings are L2-normalized within this function. The caller must use non-overlapping
    gallery and query splits and must not choose parameters using test outcomes.
    """
    q=np.asarray(query_embeddings,dtype=np.float32)
    g=np.asarray(gallery_embeddings,dtype=np.float32)
    qy=np.asarray(query_labels); gy=np.asarray(gallery_labels)
    if q.ndim!=2 or g.ndim!=2 or q.shape[1]!=g.shape[1] or len(q)!=len(qy) or len(g)!=len(gy):
        raise ValueError('Wrong shapes')
    if not(0<k<=len(g)):
        raise ValueError('Invalid k')
    q=q/np.maximum(np.linalg.norm(q,axis=1,keepdims=True),1e-12)
    g=g/np.maximum(np.linalg.norm(g,axis=1,keepdims=True),1e-12)
    sims=q@g.T
    ranks=np.argsort(-sims,axis=1,kind='stable')[:,:k]
    hits=(gy[ranks]==qy[:,None])
    positives=(gy[None,:]==qy[:,None]).sum(axis=1)
    if np.any(positives==0):raise ValueError('Query class absent from training gallery')
    kk=min(5,k)
    rr=np.where(hits.any(axis=1),1./(hits.argmax(axis=1)+1),0.)
    ap=((hits*np.cumsum(hits,axis=1)/np.arange(1,k+1)).sum(axis=1)/np.minimum(positives,k))
    return dict(precision_at_1=float(hits[:,0].mean()),precision_at_5=float(hits[:,:kk].mean()),
                hit_at_5=float(hits[:,:kk].any(axis=1).mean()),ap_at_k=float(ap.mean()),
                mrr_at_k=float(rr.mean())),ranks

if __name__=='__main__':
    q=np.array([[1.,0.],[0.,1.]],dtype=np.float32)
    g=np.array([[1.,0.],[0.,1.],[-1.,0.]],dtype=np.float32)
    m,inds=retrieval_metrics(q,g,np.array([0,1]),np.array([0,1,2]),k=3)
    assert m['precision_at_1']==1.0 and m['hit_at_5']==1.0 and m['ap_at_k']==1.0
    print('Toy-shape unit tests passed. No TrashNet results generated.')
