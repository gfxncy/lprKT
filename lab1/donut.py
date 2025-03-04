import gmsh
import sys

gmsh.initialize()
gmsh.model.add("donut")


lc = 0.04
R = 2.0
r = 0.3
W = 0.04

pi = 3.14

p0 = gmsh.model.geo.addPoint(0, 0, 0, lc)
p1 = gmsh.model.geo.addPoint(R-r, 0, 0, lc)
p2 = gmsh.model.geo.addPoint(R, 0, 0, lc)
p3 = gmsh.model.geo.addPoint(R, 0, r, lc)
p4 = gmsh.model.geo.addPoint(R + r, 0, 0, lc)
p5 = gmsh.model.geo.addPoint(R, 0, -r, lc)
arc1 = gmsh.model.geo.addCircleArc(p1, p2, p3)
arc2 = gmsh.model.geo.addCircleArc(p3, p2, p4)
arc3 = gmsh.model.geo.addCircleArc(p4, p2, p5)
arc4 = gmsh.model.geo.addCircleArc(p5, p2, p1)

c_loop_1 = gmsh.model.geo.addCurveLoop([arc1, arc2, arc3, arc4])
oval = gmsh.model.geo.copy([(1, arc1), (1, arc2), (1, arc3), (1, arc4)])
gmsh.model.geo.dilate(oval, R, 0, 0, 1-W/r, 1-W/r, 1-W/r)

c_loop_2 = gmsh.model.geo.addCurveLoop([oval[0][1], oval[1][1], oval[2][1], oval[3][1]])
s1 = gmsh.model.geo.addPlaneSurface([c_loop_1, -c_loop_2])

gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)


rot1 = gmsh.model.geo.revolve([(2, s1)], 0, 0, 0, 0, 0, 1, pi /2)
rot2 = gmsh.model.geo.revolve([(2, rot1[0][1])], 0, 0, 0, 0, 0, 1, pi / 2)
rot3 = gmsh.model.geo.revolve([(2, rot2[0][1])], 0, 0, 0, 0, 0, 1, pi / 2)
rot4 = gmsh.model.geo.revolve([(2, rot3[0][1])], 0, 0, 0, 0, 0, 1, pi / 2)

gmsh.model.geo.addPhysicalGroup(3, [rot1[1][1], rot2[1][1], rot3[1][1], rot4[1][1]], 1)
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(3)




gmsh.write("donut.msh")


if '-nopopup' not in sys.argv:
    gmsh.fltk.run()
    

gmsh.finalize()