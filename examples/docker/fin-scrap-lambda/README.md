# Base docker image

Purpose of this docker image is to include lambda function code and required configuration. It is assumed that later, configuration file (with list of funds) will be passed to Lambda as parameter - see issue: #19

# Important

Make sure to use correct version of the base image, as `Dockerfile` is fixed to use specific (not latest) version!

Pay attention to versioning, each time any layer changes in this docker image, `version.txt` file must be updated with new version.

After uploading new image, change / update lambda function to use new version of the image.

# Using the image

See instructions in [../README.md](../README.md)
