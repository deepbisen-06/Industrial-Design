INDUSTRIAL GRIPPER DESIGN - DEEP BISEN

Open report.pdf first. Fill remaining cover details before submission.
report_editable.docx is an editable text-and-figure companion; PDF is the formatted report.

cad_files/: individual STEP solids, coloured assembly STEP, dimensioned SVG drawing,
concept/assembly images, motion checks, and build_cad.py parametric source.
simulation_results/: actual computed 3D FE fields, result summary, boundary-condition,
stress and displacement plots, and solve_fea.py solver.

Reproduction (Python 3, from this directory):
  python -m pip install -r requirements.txt
  python cad_files/build_cad.py
  OPENBLAS_NUM_THREADS=1 python simulation_results/solve_fea.py
  MPLCONFIGDIR=/tmp/gripper-mpl python build_report.py
The CAD source and report source can be edited to change dimensions or cover details.
The FE geometry must be updated consistently if finger dimensions change.
An internet connection is required only to install packages.

All dimensions are mm. FE units are N, mm, MPa.
The third mesh contains 15,067 nodes / 77,760 tetrahedra.
NPZ fields are readable with numpy.load; stress components are
[sigma_x,sigma_y,sigma_z,tau_xy,tau_yz,tau_zx]. Strain shear entries are engineering shear.
Stress figures show nodal-averaged values; results.json reports unaveraged element maxima.

LIMITS: Actual static analysis is of the idealized prismatic finger, not every assembly
component. Root bores, bolts, pad compliance, contact, screw threads and base flexibility
are excluded from this solve. STEP is a neutral geometry format, not native GUI mates
or a GUI constraint tree. The dimensioned sketches and deterministic scripted parameters
specify the intended constraints. Motion states are analytic, not a dynamic simulation.
Motor and bearing details require final component selection. No manufactured test was run.
Mesh sensitivity is reported; peak clamp stress is not claimed fully converged.

The project is a documented academic design; verify course-specific acceptance of the
scripted CAD / custom numerical FEA workflow. Do not describe outputs as ANSYS or
SolidWorks results. The report transparently states the tools and modeling assumptions.
