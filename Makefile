build_frontend:
	rm -rf ./turkers/chats/react/bundles/ && npm run build

run_frontend:
	npm start

run_django:
	python project/manage.py runserver

dev:
	make -j2 run_django run_frontend
