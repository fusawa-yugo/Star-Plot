import cv2
import sys
import os
import skvideo.io
from ultralytics import YOLO

def openfile(args):
	if args[1] == '0': cv2.VideoCapture(0)
	elif args[1] == '1': return cv2.VideoCapture(os.getcwd() + '/input/videos/' + args[2])
	elif args[1] == '2': return cv2.imread(os.getcwd() + '/input/images/' + args[2])

def calc_joint(n, data):
	if n == 17: return (data[5] + data[6]) / 2
	elif n == 18: return (data[11] + data[12]) / 2
	else: return data[n]

model = YOLO('yolov8n-pose.pt')
args = sys.argv
cap = openfile(args)
pose_dict = {
	0: 'Nose',
	1: 'L_eye',
	2: 'R_eye',
	3: 'L_ear',
	4: 'R_ear',
	5: 'L_shoulder',
	6: 'R_shoulder',
	7: 'L_elbow',
	8: 'R_elbow',
	9: 'L_wrist',
	10: 'R_wrist',
	11: 'L_waist',
	12: 'R_waist',
	13: 'L_knee',
	14: 'R_knee',
	15: 'L_ankle',
	16: 'R_ankle',
	17: 'chest',
	18: 'waist'
}
if args[1] == '2':
	results = model(cap)
	graph = [[0,1],[0,2],[0,5],[0,6],[1,9],[1,10],[2,3],[2,4],[5,7],[6,8],[9,11],[10,12]]
	#骨格点出力ファイルの準備
	resulttxt = os.getcwd() + '/result/img_txt/' + os.path.splitext(args[2])[0] + '.txt'
	f = open(resulttxt, 'a')
	f.write('')
	f.close()
	result_keypoint = open(resulttxt, 'w')
	result_keypoint.write(f'Joint_Graph: {graph}\n\n')
	
	# キャプチャした画像サイズを取得
	imageWidth = results[0].orig_shape[0]
	imageHeight = results[0].orig_shape[1]

	# 後のオブジェクト名出力などのため
	names = results[0].names
	classes = results[0].boxes.cls
	boxes = results[0].boxes
	keypoints = results[0].keypoints
	annotatedFrame = results[0].plot()

	# 検出したオブジェクトのバウンディングボックス座標とオブジェクト名を取得し、ターミナルに出力
	for box, cls in zip(boxes, classes):
		name = names[int(cls)]
		x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
		print(f"Object: {name} Coordinates: StartX={x1}, StartY={y1}, EndX={x2}, EndY={y2}")
		# バウンディングBOXの座標情報を書き込む
		cv2.putText(annotatedFrame, f"{x1} {y1} {x2} {y2}", (x1, y1 - 40), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0), 2, cv2.LINE_AA)
	#骨格点を出力
	n = 0
	result_keypoint.write('Body_Joint:\n')
	for keypoint in keypoints:
		n += 1
		ok = 1
		result_keypoint.write(f'	Person{n}:\n')
		for i in keypoint.data[0]:
			if i[2] < 0.5:
				n -= 1
				ok = 0
				break
		if ok == 1:
			body_joint = [17, 18, 0, 1, 2, 7, 8, 9, 10, 13, 14, 15, 16]
			t = 0
			for m in body_joint:
				node = calc_joint(m, keypoint.data[0])
				result_keypoint.write(f'		-{pose_dict[m]}: Index={t}, X={int(node[0])}, Y={int(node[1])}\n')
				t += 1
		#else: result_keypoint.write('Not detected properly\n')
	result_keypoint.close()
	'''
	for keypoint in keypoints[0]:
		result_keypoint.write(f"Keypoint X={int(keypoint[0])}, Y={int(keypoint[1])}, Score={keypoint[2]:.4} \n")
	'''

	# プレビューウィンドウに画像出力
	cv2.imshow("YOLOv8 Inference", annotatedFrame)
	resultimg = cv2.imwrite(os.getcwd() + '/result/images/result_' + args[2],annotatedFrame)
else:
	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	size = (width, height)
	frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
	fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
	resultvideo = cv2.VideoWriter(os.getcwd() + '/result/videos/result_' + args[2], fmt, frame_rate, size)
	while cap.isOpened():
		success, frame = cap.read()
		if success:
			# 推論を実行
			results = model(frame)

			# キャプチャした画像サイズを取得
			imageWidth = results[0].orig_shape[0]
			imageHeight = results[0].orig_shape[1]

			# 後のオブジェクト名出力などのため
			names = results[0].names
			classes = results[0].boxes.cls
			boxes = results[0].boxes
			annotatedFrame = results[0].plot()

			# 検出したオブジェクトのバウンディングボックス座標とオブジェクト名を取得し、ターミナルに出力
			for box, cls in zip(boxes, classes):
				name = names[int(cls)]
				x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
				print(f"Object: {name} Coordinates: StartX={x1}, StartY={y1}, EndX={x2}, EndY={y2}")
				# バウンディングBOXの座標情報を書き込む
				cv2.putText(annotatedFrame, f"{x1} {y1} {x2} {y2}", (x1, y1 - 40), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0), 2, cv2.LINE_AA)
			# プレビューウィンドウに画像出力
			cv2.imshow("YOLOv8 Inference", annotatedFrame)
			resultvideo.write(annotatedFrame)
			# アプリケーション終了
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break	
		else: 
			# キャプチャに失敗したら終了
			break		
	# 終了処理
	resultvideo.release()
	cap.release()
	cv2.destroyAllWindows()