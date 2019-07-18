import requests, json
from time import strftime


limit_reached = [True, 16]


def save(url):
	response = requests.get(url)
	if response.status_code == 200:
		with open("image.png", 'wb') as f:
			f.write(response.content)


def send_vk(author, token, group_id, album_id):
	global limit_reached
	if limit_reached[0] == True:
		if int(limit_reached[1]) < int(strftime("%d")):
			limit_reached[0] = False
	url = "https://api.vk.com/method/photos.getUploadServer?album_id=" + album_id + "&group_id=" + group_id + "&v=5.52" + "&access_token=" + token
	send_photo = requests.get(url)
	print(limit_reached)
	upload_url = json.loads(send_photo.text)['response']['upload_url']
	file = {'file1': open('image.png', 'rb')}
	add_photo_album = requests.post(upload_url, files=file)
	add_photo_album = json.loads(add_photo_album.text)
	confirm = requests.get("https://api.vk.com/method/photos.save?server=" + str(add_photo_album['server']) + "&photos_list=" + add_photo_album['photos_list'] + "&album_id=" + str(add_photo_album['aid']) + "&hash=" + add_photo_album['hash'] + "&v=5.52" + "&access_token=" + token + "&group_id=" + group_id)
	confirm = json.loads(confirm.text)
	if limit_reached[0] is False:
		send_post = requests.get("https://api.vk.com/method/wall.post?owner_id=-" + group_id + "&from_group=1&attachments=photo-" + group_id + "_" + str(confirm['response'][0]['id']) + "&access_token=" + token + "&v=5.52" + "&message=Success by " + author)
		send_post = json.loads(send_post.text)
		if 'error' in send_post:
			if send_post['error']['error_code'] == 214:
				limit_reached = [True,strftine("%d")]

def isImage(path):
	return path[path.rfind('.')+1:len(path)]
