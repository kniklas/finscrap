update:
	zip -g packages.zip get_data.py
	aws lambda update-function-code --function-name get-data --zip-file fileb://packages.zip

create:
	aws lambda create-function --function-name get-data2 --runtime python3.9 --role arn:aws:iam::${AWS_ACCOUNT}:role/lambda-apigateway-role --handler get_data.lambda_handler --zip-file fileb://packages2.zip
