build_push:
	docker build -t kurdzik/own_api .
	docker push kurdzik/own_api

run:
	docker run -p 40074:5000 -e OPENAI_APIKEY=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 kurdzik/own_api

debug:
	docker build -t kurdzik/own_api .
	docker run -p 40074:5000 -e OPENAI_APIKEY=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 kurdzik/own_api