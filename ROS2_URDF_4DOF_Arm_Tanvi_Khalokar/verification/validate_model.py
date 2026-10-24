"""Static model/FK checks only; this does not launch ROS2 or verify live TF."""
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
import json, ast
from urdf_parser_py.urdf import URDF
R=Path(__file__).resolve().parents[1];P=R/'arm_description';f=P/'urdf/industrial_arm.urdf'
model=URDF.from_xml_file(str(f));assert model.get_root()=='world'
x=ET.parse(f).getroot();links={a.get('name'):a for a in x.findall('link')};joints=x.findall('joint')
assert len(links)==7 and len(joints)==6
assert len([j for j in joints if j.get('type')=='revolute'])==4
children=[j.find('child').get('link') for j in joints];assert len(set(children))==len(children)
assert set(children)==set(links)-{'world'}
for n,l in links.items():
 if n=='world':continue
 assert l.find('visual/geometry') is not None and l.find('collision/geometry') is not None
 inert=l.find('inertial');assert float(inert.find('mass').get('value'))>0
 a=inert.find('inertia');I=np.array([[float(a.get('ixx')),float(a.get('ixy')),float(a.get('ixz'))],[float(a.get('ixy')),float(a.get('iyy')),float(a.get('iyz'))],[float(a.get('ixz')),float(a.get('iyz')),float(a.get('izz'))]])
 eig=np.linalg.eigvalsh(I);assert np.all(eig>0);assert 2*eig.max()<=eig.sum()+1e-12
for j in joints:
 assert j.find('parent').get('link') in links and j.find('child').get('link') in links
 if j.get('type')=='revolute':
  axis=np.fromstring(j.find('axis').get('xyz'),sep=' ');assert np.isclose(np.linalg.norm(axis),1)
  lim=j.find('limit');assert float(lim.get('lower'))<float(lim.get('upper'));assert float(lim.get('effort'))>0 and float(lim.get('velocity'))>0
# This model deliberately uses only zero-RPY joint origins.
def transforms(q):
 T={'world':np.eye(4)};remaining=list(joints)
 while remaining:
  progress=False
  for j in remaining[:]:
   parent=j.find('parent').get('link');child=j.find('child').get('link')
   if parent not in T:continue
   org=j.find('origin');assert org.get('rpy')=='0 0 0'
   H=np.eye(4);H[:3,3]=np.fromstring(org.get('xyz'),sep=' ')
   if j.get('type')=='revolute':
    angle=q.get(j.get('name'),0);lim=j.find('limit');assert float(lim.get('lower'))-1e-12<=angle<=float(lim.get('upper'))+1e-12
    a=np.fromstring(j.find('axis').get('xyz'),sep=' ');K=np.array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]])
    H[:3,:3]=np.eye(3)+np.sin(angle)*K+(1-np.cos(angle))*(K@K)
   T[child]=T[parent]@H;remaining.remove(j);progress=True
  assert progress,'Cycle or disconnected chain'
 return T
poses=[('home',{},[0,0,.87]),('shoulder_90',{'joint2_shoulder':np.pi/2},[.67,0,.2]),('elbow_90',{'joint3_elbow':np.pi/2},[.37,0,.5]),('yaw_shoulder_90',{'joint1_base_yaw':np.pi/2,'joint2_shoulder':np.pi/2},[0,.67,.2])]
results=[]
for name,q,expect in poses:
 T=transforms(q);tip=T['tool_link'][:3,3];assert np.allclose(tip,expect,atol=1e-10)
 results.append({'pose':name,'tool_frame_xyz_m':tip.round(6).tolist(),'angles_rad':q})
try:transforms({'joint2_shoulder':2.0})
except AssertionError:pass
else:raise AssertionError('Out-of-limit angle accepted')
ast.parse((P/'launch/display.launch.py').read_text())
import yaml
conf=yaml.safe_load((P/'rviz/arm.rviz').read_text());assert conf['Visualization Manager']['Global Options']['Fixed Frame']=='world'
(R/'evidence/fk_results.json').write_text(json.dumps(results,indent=2))
print('PASS: urdf_parser_py parsed model, root=world; 7 links, 6 joints, 4 actuated revolute DOF.')
print('PASS: unique parents/children, complete connected tree; visual/collision geometry and positive physical inertias.')
print('PASS: joint axes/limits; 4 analytic FK target poses; out-of-limit rejection.')
print('PASS: launch Python syntax and RViz YAML structure; runtime ROS2 imports not tested.')
print('NOT RUN: check_urdf (C++), colcon build, RViz2, live /joint_states, /tf and /tf_static.')
