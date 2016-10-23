manage:
	@docker-compose run --rm web python ./manage.py \
		$(filter-out $@,$(MAKECMDGOALS))

reset-db:
	docker-compose exec postgres.local createdb wikisual -U postgres

setup-geodb:
	if [ ! -f ./geodb/GeoLite2-City.mmdb ]; then \
		mkdir -p ./geodb && \
		wget -P $(PWD)/geodb/ http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz && \
		gunzip ./geodb/GeoLite2-City.mmdb.gz; \
	fi

%:
	@:
