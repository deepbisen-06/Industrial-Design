"""Reproducible 3D linear elastic constant-strain tetrahedral analysis, N/mm/MPa.
Full 16x30x80 finger, clamped root. Uniform contact traction over inner
Contact face is x=0, y=0..30, z=60..80: 600 mm2.
300 N outward + 49.05 N downward. Root mounting holes omitted (global model).
"""
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
import json
P=Path(__file__).resolve().parent
E=200000.; nu=.3
D=np.zeros((6,6)); la=E*nu/((1+nu)*(1-2*nu)); mu=E/(2*(1+nu))
D[:3,:3]=la; D[np.arange(3),np.arange(3)]+=2*mu; D[3:,3:]=np.eye(3)*mu

def solve(nx,ny,nz,save=False):
 x=np.linspace(0,16,nx+1); y=np.linspace(0,30,ny+1); z=np.linspace(0,80,nz+1)
 nodes=np.array([[a,b,c] for a in x for b in y for c in z]); idx=lambda i,j,k:(i*(ny+1)+j)*(nz+1)+k
 tets=[]
 for i in range(nx):
  for j in range(ny):
   for k in range(nz):
    a,b,c,d,e,f,g,h=[idx(i+di,j+dj,k+dk) for di,dj,dk in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]]
    tets.extend([(a,b,c,g),(a,c,d,g),(a,d,h,g),(a,h,e,g),(a,e,f,g),(a,f,b,g)])
 tets=np.array(tets); rows=[]; cols=[]; vals=[]; Bs=[]; vols=[]
 for t in tets:
  C=np.column_stack((np.ones(4),nodes[t])); grad=np.linalg.inv(C)[1:,:]; vol=abs(np.linalg.det(C))/6
  B=np.zeros((6,12))
  for a in range(4):
   dx,dy,dz=grad[:,a]; q=3*a
   B[0,q]=dx;B[1,q+1]=dy;B[2,q+2]=dz
   B[3,q:q+3]=[dy,dx,0];B[4,q:q+3]=[0,dz,dy];B[5,q:q+3]=[dz,0,dx]
  dof=(3*t[:,None]+np.arange(3)).ravel(); ke=B.T@D@B*vol
  rows.extend(np.repeat(dof,12));cols.extend(np.tile(dof,12));vals.extend(ke.ravel()); Bs.append(B);vols.append(vol)
 nd=3*len(nodes); K=coo_matrix((vals,(rows,cols)),shape=(nd,nd)).tocsr(); F=np.zeros(nd)
 # Consistent nodal loads for rectangular surface quads (constant traction).
 for j in range(ny):
  for k in range(nz):
   if z[k]<60-1e-8:continue
   area=(y[j+1]-y[j])*(z[k+1]-z[k])
   for n in [idx(0,j,k),idx(0,j+1,k),idx(0,j,k+1),idx(0,j+1,k+1)]:
    F[3*n]+=-300*area/600/4; F[3*n+2]+=-49.05*area/600/4
 fixed=(3*np.where(nodes[:,2]==0)[0][:,None]+np.arange(3)).ravel(); free=np.setdiff1d(np.arange(nd),fixed)
 u=np.zeros(nd); u[free]=spsolve(K[free][:,free],F[free]); reaction=(K@u-F).reshape(-1,3).sum(axis=0)
 strain=np.array([B@u[(3*t[:,None]+np.arange(3)).ravel()] for B,t in zip(Bs,tets)]); stress=strain@D.T
 sx,sy,sz,txy,tyz,tzx=stress.T; vm=np.sqrt(.5*((sx-sy)**2+(sy-sz)**2+(sz-sx)**2)+3*(txy*txy+tyz*tyz+tzx*tzx))
 # Equivalent elastic strain = von Mises stress/E for isotropic elasticity.
 disp=np.linalg.norm(u.reshape(-1,3),axis=1)
 out=dict(mesh=[nx,ny,nz],nodes=len(nodes),elements=len(tets),max_displacement_mm=float(disp.max()),max_von_mises_MPa=float(vm.max()),max_equivalent_strain=float(vm.max()/E),yield_safety_factor=float(250/vm.max()),reaction_N=reaction.tolist(),force_N=F.reshape(-1,3).sum(axis=0).tolist(),free_residual_N=float(np.abs((K@u-F)[free]).max()))
 if save: np.savez(P/'fea_fields.npz',nodes=nodes,tets=tets,u=u.reshape(-1,3),stress=stress,strain=strain,von_mises=vm,displacement=disp)
 print(out,flush=True);return out
if __name__=='__main__':
 results=[solve(4,6,20),solve(8,12,40),solve(12,18,60,True)]
 (P/'results.json').write_text(json.dumps(results,indent=2))
