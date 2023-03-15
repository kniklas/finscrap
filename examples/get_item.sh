export AWS_PROFILE=kamil-adm

aws dynamodb get-item \
	--table-name Assets2 \
	--key '{"AssetID": {"S": "PL00002"}, "PriceDate": {"S": "2023-01-02"}}' \
	--return-consumed-capacity TOTAL

# --key file://item2.json \
