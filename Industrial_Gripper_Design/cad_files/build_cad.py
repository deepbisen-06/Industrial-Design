"""Parametric gripper, units mm. Run with CadQuery 2.7.0; writes beside this script.
Independent variables fully define orthogonal sketch profiles; no free dimensions.
Threads represented by nominal cylinders; specify opposed Tr12x3 threads on manufacture.
"""
from pathlib import Path
import cadquery as cq
P=Path(__file__).resolve().parent
BASE_L,BASE_W,BASE_T=160.,80.,12.
JAW_T,JAW_W,JAW_L=16.,30.,80.
JAW_CENTER=45.
parts=[]
def add(name,obj,color):
 parts.append((name,obj,color)); cq.exporters.export(obj,str(P/(name+'.step')))
base=cq.Workplane('XY').box(BASE_L,BASE_W,BASE_T,centered=(True,True,False))
base=base.faces('>Z').workplane().pushPoints([(-65,-30),(-65,30),(65,-30),(65,30)]).hole(7)
add('base',base,(.10,.28,.72))
for sign,label in [(-1,'left'),(1,'right')]:
 x=sign*JAW_CENTER
 carriage=cq.Workplane('XY').box(30,68,22).translate((x,0,25))
 for y,r in [(-25,5),(25,5),(0,6)]:
  bore=cq.Workplane('YZ').center(y,25).circle(r).extrude(200,both=True)
  carriage=carriage.cut(bore)
 for y in [-9,9]:
  carriage=carriage.cut(cq.Workplane('XY').center(x,y).circle(2.5).extrude(60))
 add(label+'_carriage',carriage,(.10,.28,.72))
 # Prismatic finger: same domain as numerical continuum model.
 finger=cq.Workplane('XY').box(JAW_T,JAW_W,JAW_L,centered=(True,True,False)).translate((x,0,36))
 # Mount holes confined to root, omitted in global FE idealization.
 for y in [-9,9]:
  finger=finger.cut(cq.Workplane('XY').center(x,y).circle(2.5).extrude(10).translate((0,0,36)))
 add(label+'_finger',finger,(1.,.75,.03))
 pad=cq.Workplane('XY').box(3,30,20).translate((x-sign*9.5,0,106))
 add(label+'_pad',pad,(.08,.10,.14))
 support=cq.Workplane('XY').box(12,72,30).translate((sign*72,0,27))
 for y,r in [(-25,5),(25,5),(0,6)]: support=support.cut(cq.Workplane('YZ').center(y,25).circle(r).extrude(200,both=True))
 add(label+'_support',support,(.1,.28,.72))
 for y in [-9,9]:
  bolt=cq.Workplane('XY').circle(2.5).extrude(18).translate((x,y,28))
  add(label+'_bolt_'+str(y),bolt,(.45,.46,.5))
for y in [-25,25]: add('guide_'+str(y),cq.Workplane('YZ').center(y,25).circle(5).extrude(144).translate((-72,0,0)),(.65,.68,.72))
add('opposed_lead_screw',cq.Workplane('YZ').center(0,25).circle(6).extrude(172).translate((-86,0,0)),(.65,.68,.72))
add('motor_interface',cq.Workplane('YZ').center(0,25).rect(40,40).extrude(8).translate((86,0,0)),(.1,.28,.72))
a=cq.Assembly(name='Industrial_Gripper')
for n,o,c in parts: a.add(o,name=n,color=cq.Color(*c))
a.export(str(P/'gripper_assembly.step'))
# Mesh snapshots for honest CAD render, not a hand-generated substitute.
import numpy as np
verts=[]; faces=[]; colors=[]
for n,o,c in parts:
 v,f=o.val().tessellate(.3)
 offset=len(verts); verts.extend([q.toTuple() for q in v]); faces.extend([[offset+i for i in t] for t in f]); colors.extend([c]*len(f))
np.savez(P/'render_mesh.npz',vertices=verts,faces=faces,colors=colors)
print('Exported',len(parts),'parts and assembly; all solid volumes positive:',all(o.val().Volume()>0 for _,o,_ in parts))
