build_push:
	docker build -t kurdzik/own_api .
	docker push kurdzik/own_api

run:
	docker run -p 40074:5000 -e OPENAI_APIKEY="" kurdzik/own_api

	
debug:
	docker build -t kurdzik/own_api .
	docker run -p 40074:5000 -e OPENAI_APIKEY="" kurdzik/own_api