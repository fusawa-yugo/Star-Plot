import requests
import json
import base64

def test_skeletal_points(image_path):
    url = "http://localhost:5050/skeletal-points"
    with open(image_path, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')
    data = {'image': encoded_image}
    response = requests.post(url, json=data)
    print("skeletal-points response:")
    print(response.status_code)
    print(response.json())
    return response.json()

def test_points_to_plot(image_path, nodes, edges):
    url = "http://localhost:5050/points-to-plot"
    with open(image_path, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')
    json_data = json.dumps({'nodes': nodes, 'edges': edges, 'image': encoded_image})
    response = requests.post(url, json=json.loads(json_data))
    print("points-to-plot response:")
    print(response.status_code)
    print(response.json())

# 使用例
if __name__ == "__main__":
    image_path = "./plot/input/images/0.jpg"  # テスト用画像のパス

    keypoints = test_skeletal_points(image_path)
    test_points_to_plot(image_path, keypoints["keypoints"], keypoints["skelton"])
