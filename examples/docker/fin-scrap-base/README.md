# Base docker image

Purpose of this docker image is to install python dependencies required by lambda function. This includes `finscrap` python package.

# Important

Make sure python dependencies conflicts are resolved - see [../README.md](../README.md) for example command. Resolved dependencies are stored in `requirements.txt` file.

Pay attention to versioning, each time any layer changes in this docker image, `version.txt` file must be updated with new version.

# Using the image

See instructions in [../README.md](../README.md)
