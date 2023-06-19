aws dynamodb put-item \
	--table-name Assets2 \
	--item '{"AssetID": {"S": "PL00002"}, "PriceDate": {"S": "2023-01-02"}, "AssetPrice": {"N": "9.1"}}' \
	--return-consumed-capacity TOTAL
