aws dynamodb create-table --table-name Assets1 --attribute-definitions \
	AttributeName=AssetID,AttributeType=S \
	AttributeName=PriceDate,AttributeType=S \
	--billing-mode PAY_PER_REQUEST \
	--key-schema AttributeName=AssetID,KeyType=HASH \
	AttributeName=PriceDate,KeyType=RANGE \
	--table-class STANDARD
