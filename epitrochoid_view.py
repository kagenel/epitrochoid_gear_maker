import adsk.core, adsk.fusion, adsk.cam, traceback
import math

i = 9   # 減速比
tp = i+1 # 外ピンの数(MAX)
tc = tp - 1 # 曲線板の歯数(最大の減速比)
e = 2 # 偏心距離
r = 30 # 外ピン配置半径
#i = tc / (tp - tc)    # 減速比

# 内ピン
rout = 2       # 内ピンの半径
r_cam = 3   # 入力軸の半径

rin = rout + e # 内ピンを通す穴の半径w
r_cam_mount = r_cam + e # 入力軸の円

rin_cam = r/2 + rout/2

r_pinOut_case = 3 # 外ピンの外装

division = 5*r # サンプリング点

# 単位変換 [mm] -> [cm]
e /= 10
r /= 10
rout /= 10
rin /= 10
r_cam /= 10
r_cam_mount /= 10
rin_cam /= 10
r_pinOut_case /= 10

# パラメータの決定
r2 = r / (1 + i)
r1 = i * r2
rd = e

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)

        # Create an object collection for the points.
        points = adsk.core.ObjectCollection.create() # 遊星歯車
 
        # Define the points the spline with fit through.
        draw_epitrochoid(points)

        # Create the spline.
        sketch.sketchCurves.sketchFittedSplines.add(points)

        
        draw_pinOut_case(sketch, 0.0)
        draw_pinOut_case(sketch, r_pinOut_case)

        draw_cam(sketch)
        draw_inRing(sketch)
        draw_camMount(sketch)
        draw_pinOut(sketch)

        draw_pinIn(sketch)
        draw_pinIn_cam(sketch)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def draw_epitrochoid(points):
    # エピコロイド曲線
    theta = [i*2*math.pi/division for i in range(division)]

    x = [(r1 + r2)*math.cos(th) - rd * math.cos((r1+r2)/r2*th) + e*math.cos(0) for th in theta]
    y = [(r1 + r2)*math.sin(th) - rd * math.sin((r1+r2)/r2*th) + e*math.sin(0) for th in theta]

    # エピトロコイド平行曲線
    dx = [(r1 + r2) * (-math.sin(th) + (rd/r2) * math.sin((r1+r2)/r2*th)) for th in theta]
    dy = [(r1 + r2) * (math.cos(th) - (rd/r2) * math.cos((r1+r2)/r2*th)) for th in theta]

    x2 = [x[i] + (rd/(math.sqrt(dx[i]**2 + dy[i]**2)) * -dy[i]) for i in range(division)]
    y2 = [y[i] + (rd/(math.sqrt(dx[i]**2 + dy[i]**2)) * dx[i]) for i in range(division)]

    for i in range(division):
        points.add(adsk.core.Point3D.create(x2[i], y2[i], 0))
    points.add(adsk.core.Point3D.create(x2[0], y2[0], 0))

# 出力リングを回すための穴
def draw_inRing(sketch):
    N = 6
    x_move = [(rin_cam)*math.cos(2*math.pi*k/N) for k in range(N)]
    y_move = [(rin_cam)*math.sin(2*math.pi*k/N) for k in range(N)]

    for i in range(N):
        # Draw a circle.
        sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(x_move[i] + e*math.cos(0), y_move[i] + e*math.sin(0), 0), rin)
    
# 偏心カム
def draw_camMount(sketch):
    point = adsk.core.Point3D.create(e*math.cos(0), e*math.sin(0), 0)
    sketch.sketchCurves.sketchCircles.addByCenterRadius(point, r_cam_mount)

# 入力軸
def draw_cam(sketch):
    point = adsk.core.Point3D.create(0, 0, 0)
    sketch.sketchCurves.sketchCircles.addByCenterRadius(point, r_cam)

# 外ピン
def draw_pinOut(sketch):
    x_move = [(r)*math.cos(2*math.pi*k/tp) for k in range(tp)]
    y_move = [(r)*math.sin(2*math.pi*k/tp) for k in range(tp)]

    for i in range(tp):
        sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(x_move[i], y_move[i], 0), rd)

# 外ピンのケース
def draw_pinOut_case(sketch, r_case):
    point = adsk.core.Point3D.create(0, 0, 0)
    sketch.sketchCurves.sketchCircles.addByCenterRadius(point, r+rd+r_case)

# 出力ピン
def draw_pinIn(sketch):
    N = 6
    x_move = [(rin_cam)*math.cos(2*math.pi*k/N) for k in range(N)]
    y_move = [(rin_cam)*math.sin(2*math.pi*k/N) for k in range(N)]

    for i in range(N):
        point = adsk.core.Point3D.create(x_move[i], y_move[i], 0)
        sketch.sketchCurves.sketchCircles.addByCenterRadius(point, rout)
    
# 出力カム
def draw_pinIn_cam(sketch):
    point = adsk.core.Point3D.create(0, 0, 0)
    sketch.sketchCurves.sketchCircles.addByCenterRadius(point, rout + rin_cam)
