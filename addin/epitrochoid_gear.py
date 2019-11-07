import adsk.core, adsk.fusion, adsk.cam, traceback
import math

i = 9   # 減速比
tp = i+1 # 外ピンの数(MAX)
tc = tp - 1 # 曲線板の歯数(最大の減速比)
e = 2 # 偏心距離
r = 25 # 外ピン配置半径
#i = tc / (tp - tc)    # 減速比

# 内ピン
rout = 4       # 内ピンの半径
r_cam = 2   # 入力軸の半径

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
        points_inRings = [adsk.core.ObjectCollection.create() for i in range(6)] # 出力リングを回すための穴
        points_cam = adsk.core.ObjectCollection.create() # 入力軸
        points_cam_mount = adsk.core.ObjectCollection.create() # 偏心カム
        points_pinOuts = [adsk.core.ObjectCollection.create() for i in range(tp)]  # 外ピン
        points_pinOut_case = [adsk.core.ObjectCollection.create() for i in range(2)] # 外ピンのケース

        points_pinIns = [adsk.core.ObjectCollection.create() for i in range(6)] # 出力ピン
        points_pinIn_cam =  adsk.core.ObjectCollection.create() # 出力カム        
        
        # Define the points the spline with fit through.
        draw_epitrochoid(points)
        for i in range(6):
            draw_inRing(points_inRings[i], i, 6, 20)
        draw_cam(points_cam, 10)
        draw_camMount(points_cam_mount, 10)
        for i in range(tp):
            draw_pinOut(points_pinOuts[i], i, 20)
        draw_pinOut_case(points_pinOut_case[0], 0.0, 100)
        draw_pinOut_case(points_pinOut_case[1], r_pinOut_case, 100)

        for i in range(6):
            draw_pinIn(points_pinIns[i], i, 6, 20)
        draw_pinIn_cam(points_pinIn_cam, 20)

        # Create the spline.
        sketch.sketchCurves.sketchFittedSplines.add(points)
        for i in range(6):
            sketch.sketchCurves.sketchFittedSplines.add(points_inRings[i])
        sketch.sketchCurves.sketchFittedSplines.add(points_cam)
        sketch.sketchCurves.sketchFittedSplines.add(points_cam_mount)
        for i in range(tp):
            sketch.sketchCurves.sketchFittedSplines.add(points_pinOuts[i])
        sketch.sketchCurves.sketchFittedSplines.add(points_pinOut_case[0])
        sketch.sketchCurves.sketchFittedSplines.add(points_pinOut_case[1])

        for i in range(6):
            sketch.sketchCurves.sketchFittedSplines.add(points_pinIns[i])
        sketch.sketchCurves.sketchFittedSplines.add(points_pinIn_cam)

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

def draw_inRing(points, n, N, D):
    theta = [i*2*math.pi/D for i in range(D)]
    x_move = [(rin_cam)*math.cos(2*math.pi*k/N) for k in range(N)]
    y_move = [(rin_cam)*math.sin(2*math.pi*k/N) for k in range(N)]

    x = [rin*math.cos(th) + x_move[n] + e*math.cos(0) for th in theta]
    y = [rin*math.sin(th) + y_move[n] + e*math.sin(0) for th in theta]

    for i in range(D):
        points.add(adsk.core.Point3D.create(x[i], y[i], 0))
    points.add(adsk.core.Point3D.create(x[0], y[0], 0))

def draw_camMount(points, D):
    theta = [i*2*math.pi/D for i in range(D)]
    x = [r_cam_mount*math.cos(th) + e*math.cos(0) for th in theta]
    y = [r_cam_mount*math.sin(th) + e*math.sin(0) for th in theta]

    for i in range(D):
        points.add(adsk.core.Point3D.create(x[i], y[i], 0))
    points.add(adsk.core.Point3D.create(x[0], y[0], 0))

def draw_cam(points, D):
    theta = [i*2*math.pi/D for i in range(D)]

    x = [r_cam*math.cos(th) for th in theta]
    y = [r_cam*math.sin(th) for th in theta]

    for i in range(D):
        points.add(adsk.core.Point3D.create(x[i], y[i], 0))
    points.add(adsk.core.Point3D.create(x[0], y[0], 0))

def draw_pinOut(points, n, D):
    theta = [i*2*math.pi/D for i in range(D)]
    x_move = [(r)*math.cos(2*math.pi*k/tp) for k in range(tp)]
    y_move = [(r)*math.sin(2*math.pi*k/tp) for k in range(tp)]

    x = [rd*math.cos(th) + x_move[n] for th in theta]
    y = [rd*math.sin(th) + y_move[n] for th in theta]

    for i in range(D):
        points.add(adsk.core.Point3D.create(x[i], y[i], 0))
    points.add(adsk.core.Point3D.create(x[0], y[0], 0))

def draw_pinOut_case(points, r_case, D):
    theta = [i*2*math.pi/D for i in range(D)]

    x = [(r+rd+r_case)*math.cos(th) for th in theta]
    y = [(r+rd+r_case)*math.sin(th) for th in theta]

    for i in range(D):
        points.add(adsk.core.Point3D.create(x[i], y[i], 0))
    points.add(adsk.core.Point3D.create(x[0], y[0], 0))

def draw_pinIn(points, n, N, D):
    theta = [i*2*math.pi/D for i in range(D)]
    x_move = [(rin_cam)*math.cos(2*math.pi*k/N) for k in range(N)]
    y_move = [(rin_cam)*math.sin(2*math.pi*k/N) for k in range(N)]

    x = [rout*math.cos(th) + x_move[n] for th in theta]
    y = [rout*math.sin(th) + y_move[n] for th in theta]

    for i in range(D):
        points.add(adsk.core.Point3D.create(x[i], y[i], 0))
    points.add(adsk.core.Point3D.create(x[0], y[0], 0))

def draw_pinIn_cam(points, D):
    theta = [i*2*math.pi/D for i in range(D)]

    x = [(rout + rin_cam)*math.cos(th) for th in theta]
    y = [(rout + rin_cam)*math.sin(th) for th in theta]

    for i in range(D):
        points.add(adsk.core.Point3D.create(x[i], y[i], 0))
    points.add(adsk.core.Point3D.create(x[0], y[0], 0))
