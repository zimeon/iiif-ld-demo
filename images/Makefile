all: fcr/info.json fcv/info.json 1r/info.json 1v2r/info.json 2v/info.json 3r/info.json 3v/info.json bcr/info.json bcv/info.json

fcr/info.json: src/fcr.jpg
	iiif_static.py --dst=. --prefix=http://localhost:8001 --extra="full/90," src/fcr.jpg --write-html=. --include-osd

fcv/info.json: src/fcv.jpg
	iiif_static.py --dst=. --prefix=http://localhost:8001 --extra="full/90," src/fcv.jpg --write-html=.

1r/info.json: src/1r.jpg
	iiif_static.py --dst=. --prefix=http://localhost:8001 --extra="full/90," src/1r.jpg --write-html=.

1v2r/info.json: src/1v2r.jpg
	iiif_static.py --dst=. --prefix=http://localhost:8001 --extra="full/90," src/1v2r.jpg --write-html=.

2v/info.json: src/2v.jpg
	iiif_static.py --dst=. --prefix=http://localhost:8001 --extra="full/90," src/2v.jpg --write-html=.

3r/info.json: src/3r.jpg
	iiif_static.py --dst=. --prefix=http://localhost:8001 --extra="full/90," src/3r.jpg --write-html=.

3v/info.json: src/3v.jpg
	iiif_static.py --dst=. --prefix=http://localhost:8001 --extra="full/90," src/3v.jpg --write-html=.

bcr/info.json: src/bcr.jpg
	iiif_static.py --dst=. --prefix=http://localhost:8001 --extra="full/90," src/bcr.jpg --write-html=.

bcv/info.json: src/bcv.jpg
	iiif_static.py --dst=. --prefix=http://localhost:8001 --extra="full/90," src/bcv.jpg --write-html=.

server: all
	python ../cors_server.py 8001
