# AURORA-Partikelvideo QUER 3 min, 1920x1080, 30 fps, ohne Ton
# Roehre mit orangen Punkten -> Gesicht Cover I -> Wandlung (orange -> Nordlicht) -> Gesicht Cover II -> ruhiger Ausklang
# blender -b -P aurora_partikel.py -- still F1 [F2 ...]   |   anim [START END]
import bpy, math, sys
import numpy as np
args = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
MODE = args[0] if args else "still"
BASE = "C:/Tools/blender_proj/aurora_quer/"
FPS = 30; TOT = 5400
G0, GS, GD = 600, 700, 650        # Sammeln: Start, Streuung (je nach Punkt), Dauer
T0, TS, TD = 2700, 650, 700       # Wandlung I -> II
FY = -60.0
D = np.load(BASE + "data.npz"); N = len(D["d1"])
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE_NEXT'
sc.eevee.taa_render_samples = 24
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.fps = FPS; sc.frame_start, sc.frame_end = 1, TOT
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.compression = 25
sc.render.use_overwrite = False; sc.render.use_placeholder = False
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[1].default_value = 1.0
bg.inputs[0].default_value = (0.014, 0.0045, 0.002, 1); bg.inputs[0].keyframe_insert("default_value", frame=T0)
bg.inputs[0].default_value = (0.002, 0.005, 0.014, 1); bg.inputs[0].keyframe_insert("default_value", frame=T0+TS+TD)
bg.inputs[0].default_value = (0.014, 0.0045, 0.002, 1); bg.inputs[0].keyframe_insert("default_value", frame=1)

def bez(obj):
    ad = obj.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'
def lin(owner):
    ad = owner.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

# ---------- Roehre: orange -> tuerkis, wird zum Ende zart
def ring_material():
    m = bpy.data.materials.new("Roehre"); m.use_nodes = True
    n = m.node_tree.nodes; n.clear()
    e = n.new("ShaderNodeEmission")
    o = n.new("ShaderNodeOutputMaterial"); m.node_tree.links.new(e.outputs[0], o.inputs[0])
    for col, st, f in (((1.0, 0.33, 0.05, 1), 1.6, 1), ((1.0, 0.33, 0.05, 1), 1.2, T0), ((0.08, 0.95, 0.5, 1), 1.0, T0+TS+TD), ((0.08, 0.95, 0.5, 1), 0.7, TOT)):
        e.inputs[0].default_value = col; e.inputs[0].keyframe_insert("default_value", frame=f)
        e.inputs[1].default_value = st; e.inputs[1].keyframe_insert("default_value", frame=f)
    lin(m.node_tree)
    return m
RM = ring_material()
def join(objs, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join(); o = bpy.context.view_layer.objects.active; o.name = name; return o
rings = []
for i in list(range(0, 27)) + list(range(38, 62)):
    r = 3.3 + 0.2*math.sin(i*0.7) if i < 30 else 10.5 + 0.55*(i-38) + 0.3*math.sin(i*0.7)
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.03, major_segments=56, minor_segments=6,
                                     location=(0, -i*1.6, 0), rotation=(math.radians(90), 0, 0))
    o = bpy.context.object; o.data.materials.append(RM); rings.append(o)
join(rings, "Ringe")
lines = []
for k in range(24):
    a = k/24*2*math.pi
    for dp, cy in ((43, -20.0),):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=dp, location=(3.5*math.cos(a), cy, 3.5*math.sin(a)), rotation=(math.radians(90), 0, 0))
        o = bpy.context.object; o.data.materials.append(RM); lines.append(o)
join(lines, "Linien")

# ---------- Punkte
mesh = bpy.data.meshes.new("Punkte")
mesh.vertices.add(N); mesh.vertices.foreach_set("co", D["F1"].ravel()); mesh.update()
def attr(name, arr):
    arr = np.asarray(arr, np.float32)
    if name in ("col0", "col1"):
        a = mesh.attributes.new(name, 'FLOAT_COLOR', 'POINT')
        a.data.foreach_set("color", np.concatenate([arr, np.ones((N, 1), np.float32)], 1).ravel())
    elif arr.ndim == 1:
        a = mesh.attributes.new(name, 'FLOAT', 'POINT'); a.data.foreach_set("value", arr)
    else:
        a = mesh.attributes.new(name, 'FLOAT_VECTOR', 'POINT'); a.data.foreach_set("vector", arr.ravel())
for k in ("S0y", "vy", "col0", "col1", "d1", "d2", "b1", "b2", "drA", "drw", "drph", "sz", "tx", "S0", "F1", "F2"): attr(k, D[k])
obj = bpy.data.objects.new("Punkte", mesh); sc.collection.objects.link(obj)

# Material: Farbe orange->nordlicht je Punkt (Verzoegerung d2), Funkeln
m = bpy.data.materials.new("Punkt"); m.use_nodes = True
nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes; L = nt.links
def A(name):
    x = Nn.new("ShaderNodeAttribute"); x.attribute_name = name; x.attribute_type = 'INSTANCER'; return x
a0, a1, ad, atx = A("col0"), A("col1"), A("d2"), A("tx")
fv = Nn.new("ShaderNodeValue")
for v, f in ((1.0, 1), (float(TOT), TOT)):
    fv.outputs[0].default_value = v; fv.outputs[0].keyframe_insert("default_value", frame=f)
# t = clamp((frame - T0 - d2*TS)/TD)
s1 = Nn.new("ShaderNodeMath"); s1.operation = 'MULTIPLY'; s1.inputs[1].default_value = TS
s2 = Nn.new("ShaderNodeMath"); s2.operation = 'SUBTRACT'; s2.inputs[1].default_value = T0
s3 = Nn.new("ShaderNodeMath"); s3.operation = 'SUBTRACT'
s4 = Nn.new("ShaderNodeMath"); s4.operation = 'DIVIDE'; s4.inputs[1].default_value = TD; s4.use_clamp = True
L.new(ad.outputs["Fac"], s1.inputs[0]); L.new(fv.outputs[0], s2.inputs[0]); L.new(s2.outputs[0], s3.inputs[0]); L.new(s1.outputs[0], s3.inputs[1]); L.new(s3.outputs[0], s4.inputs[0])
mx = Nn.new("ShaderNodeMix"); mx.data_type = 'RGBA'
L.new(s4.outputs[0], mx.inputs[0]); L.new(a0.outputs["Color"], mx.inputs[6]); L.new(a1.outputs["Color"], mx.inputs[7])
f1 = Nn.new("ShaderNodeMath"); f1.operation = 'MULTIPLY'; f1.inputs[1].default_value = 0.11
f2 = Nn.new("ShaderNodeMath"); f2.operation = 'ADD'
f3 = Nn.new("ShaderNodeMath"); f3.operation = 'SINE'
f4 = Nn.new("ShaderNodeMath"); f4.operation = 'MULTIPLY_ADD'; f4.inputs[1].default_value = 0.22; f4.inputs[2].default_value = 0.95
L.new(fv.outputs[0], f1.inputs[0]); L.new(f1.outputs[0], f2.inputs[0]); L.new(atx.outputs["Fac"], f2.inputs[1])
L.new(f2.outputs[0], f3.inputs[0]); L.new(f3.outputs[0], f4.inputs[0])
em = Nn.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.8
sm = Nn.new("ShaderNodeMath"); sm.operation = 'MULTIPLY'; sm.inputs[1].default_value = 1.15
L.new(f4.outputs[0], sm.inputs[0]); L.new(sm.outputs[0], em.inputs[1])
oo = Nn.new("ShaderNodeOutputMaterial")
hs = Nn.new("ShaderNodeHueSaturation")
sat = Nn.new("ShaderNodeMath"); sat.operation = 'SINE'
satm = Nn.new("ShaderNodeMath"); satm.operation = 'MULTIPLY_ADD'; satm.inputs[1].default_value = 1.3; satm.inputs[2].default_value = 1.0
tp = Nn.new("ShaderNodeMath"); tp.operation = 'MULTIPLY'; tp.inputs[1].default_value = math.pi
L.new(s4.outputs[0], tp.inputs[0]); L.new(tp.outputs[0], sat.inputs[0]); L.new(sat.outputs[0], satm.inputs[0]); L.new(satm.outputs[0], hs.inputs["Saturation"])
L.new(mx.outputs[2], hs.inputs["Color"]); L.new(hs.outputs[0], em.inputs[0]); L.new(em.outputs[0], oo.inputs[0])
lin(m.node_tree)

# Geometry Nodes
g = bpy.data.node_groups.new("Partikel", 'GeometryNodeTree')
g.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
g.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
G = g.nodes; GL = g.links
def node(t, **kw):
    n = G.new(t)
    for k, v in kw.items(): setattr(n, k, v)
    return n
def put(sock, v):
    if isinstance(v, bpy.types.NodeSocket): GL.new(v, sock)
    else: sock.default_value = v
def M(op, a, b=None, c=None, clamp=False):
    n = node("ShaderNodeMath", operation=op, use_clamp=clamp)
    put(n.inputs[0], a)
    if b is not None: put(n.inputs[1], b)
    if c is not None: put(n.inputs[2], c)
    return n.outputs[0]
def V(op, a, b=None, scale=None):
    n = node("ShaderNodeVectorMath", operation=op)
    put(n.inputs[0], a)
    if b is not None: put(n.inputs[1], b)
    if scale is not None: put(n.inputs[3], scale)
    return n.outputs[0]
def NA(name, vec=False):
    n = node("GeometryNodeInputNamedAttribute", data_type='FLOAT_VECTOR' if vec else 'FLOAT'); n.inputs["Name"].default_value = name
    return n.outputs["Attribute"]
def MR(val, lo, hi, kind):
    n = node("ShaderNodeMapRange", interpolation_type=kind, clamp=True)
    put(n.inputs["Value"], val); put(n.inputs["From Min"], lo); put(n.inputs["From Max"], hi)
    return n.outputs["Result"]
def MIXV(f, a, b):
    n = node("ShaderNodeMix", data_type='VECTOR'); put(n.inputs[0], f); put(n.inputs[4], a); put(n.inputs[5], b)
    return n.outputs[1]
gi = node("NodeGroupInput"); go = node("NodeGroupOutput")
fr = node("GeometryNodeInputSceneTime").outputs["Frame"]
d1, d2, sz = NA("d1"), NA("d2"), NA("sz")
s0, f1v, f2v = NA("S0", True), NA("F1", True), NA("F2", True)
frv = node("ShaderNodeCombineXYZ"); [GL.new(fr, frv.inputs[i]) for i in range(3)]
drift = V('MULTIPLY', NA("drA", True), V('SINE', V('ADD', V('MULTIPLY', NA("drw", True), frv.outputs[0]), NA("drph", True))))
# Roehre: Punkte stroemen langsam auf die Kamera zu, bis sie zu ihrem Gesicht aufbrechen
tg0 = M('ADD', M('MULTIPLY', d1, GS), G0)
s0y, vyv = NA("S0y"), NA("vy")
wrapped = M('WRAP', M('SUBTRACT', s0y, M('MULTIPLY', M('MULTIPLY', M('MINIMUM', fr, tg0), 0.11), vyv)), 6.0, -64.0)
cy = node("ShaderNodeCombineXYZ"); put(cy.inputs[1], M('SUBTRACT', wrapped, s0y))
streamed = V('ADD', V('ADD', s0, cy.outputs[0]), V('MULTIPLY', drift, (3.0, 1.0, 3.0)))
tc1 = MR(fr, tg0, M('ADD', tg0, GD), 'SMOOTHERSTEP')
posA = V('ADD', MIXV(tc1, streamed, f1v), V('SCALE', NA("b1", True), scale=M('SINE', M('MULTIPLY', tc1, math.pi))))
tg1 = M('ADD', M('MULTIPLY', d2, TS), T0)
tc2 = MR(fr, tg1, M('ADD', tg1, TD), 'SMOOTHERSTEP')
posB = V('ADD', MIXV(tc2, posA, f2v), V('SCALE', NA("b2", True), scale=M('SINE', M('MULTIPLY', tc2, math.pi))))
alive = V('SCALE', drift, scale=M('MULTIPLY', tc1, 0.025))
pos = V('ADD', posB, alive)
psep = node("ShaderNodeSeparateXYZ"); GL.new(pos, psep.inputs[0]); pos_y = psep.outputs[1]
sp = node("GeometryNodeSetPosition"); GL.new(gi.outputs[0], sp.inputs["Geometry"]); GL.new(pos, sp.inputs["Position"])
ico = node("GeometryNodeMeshIcoSphere"); ico.inputs["Radius"].default_value = 0.0105; ico.inputs["Subdivisions"].default_value = 1
iop = node("GeometryNodeInstanceOnPoints"); GL.new(sp.outputs[0], iop.inputs["Points"]); GL.new(ico.outputs["Mesh"], iop.inputs["Instance"])
oi = node("GeometryNodeObjectInfo", transform_space='ORIGINAL'); camy = node("ShaderNodeSeparateXYZ"); GL.new(oi.outputs["Location"], camy.inputs[0])
near = MR(M('SUBTRACT', camy.outputs[1], pos_y), 2.0, 9.0, 'LINEAR')
szf = M('MULTIPLY', M('MULTIPLY', sz, M('ADD', 0.5, M('MULTIPLY', tc1, 0.5))), near)
cs = node("ShaderNodeCombineXYZ"); [GL.new(szf, cs.inputs[i]) for i in range(3)]
GL.new(cs.outputs[0], iop.inputs["Scale"])
smt = node("GeometryNodeSetMaterial"); smt.inputs["Material"].default_value = m
GL.new(iop.outputs["Instances"], smt.inputs["Geometry"]); GL.new(smt.outputs[0], go.inputs[0])
obj.modifiers.new("P", 'NODES').node_group = g

# ---------- Kamera (Hochformat): Flug durch die Roehre, dann sanftes Wandern um das Gesicht
cam = bpy.data.cameras.new("C"); cam.lens = 35; cam.sensor_fit = 'HORIZONTAL'; cam.sensor_width = 36; cam.clip_start = 0.05; cam.clip_end = 400
co = bpy.data.objects.new("C", cam); sc.collection.objects.link(co); sc.camera = co
oi.inputs["Object"].default_value = co
tgt = bpy.data.objects.new("T", None); sc.collection.objects.link(tgt); tgt.location = (0, FY, 0)
tcn = co.constraints.new('TRACK_TO'); tcn.target = tgt; tcn.track_axis = 'TRACK_NEGATIVE_Z'; tcn.up_axis = 'UP_Y'
for (x, y, z, f) in ((0, 2.5, 0, 1), (0.3, -9, 0.2, 900), (-0.2, -24, -0.1, 1700), (0, -43, 0, 2500), (0.8, -43, 0.3, 3500),
                     (-0.7, -44, -0.2, 4400), (0.4, -43, 0.2, 5000), (0, -42, 0, TOT)):
    co.location = (x, y, z); co.keyframe_insert("location", frame=f)
bez(co)

# ---------- Glow
sc.use_nodes = True
t_ = sc.node_tree; t_.nodes.clear()
rl = t_.nodes.new("CompositorNodeRLayers"); gl = t_.nodes.new("CompositorNodeGlare")
gl.glare_type = 'FOG_GLOW'; gl.quality = 'MEDIUM'; gl.threshold = 1.2; gl.size = 7
cp = t_.nodes.new("CompositorNodeComposite")
t_.links.new(rl.outputs[0], gl.inputs[0]); t_.links.new(gl.outputs[0], cp.inputs[0])

if MODE == "still":
    for f in args[1:]:
        sc.frame_set(int(f)); sc.render.filepath = BASE + "stills/s_%05d.png" % int(f)
        sc.render.use_overwrite = True
        bpy.ops.render.render(write_still=True)
else:
    if len(args) >= 3: sc.frame_start, sc.frame_end = int(args[1]), int(args[2])
    sc.render.filepath = BASE + "frames/f_"
    bpy.ops.render.render(animation=True)
