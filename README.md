# MLOps-MiniCapstone

Author: Borja Gomez (franciscodebo@gmail.com)  
MLOps-3  
Barcelona, May 2022
## Project description

This is the Mini-Capstone assigment for the cohort #3 of the MLOps program.
### How to use this service

All the commends are implemented using Makefile. Here you have the list of available commands:

* Build the image. Do this any time you commit code or add a new library:

```
make build
```

* Run the container associated to the image. The web server is running so every change at any file it will be refreshed.

Don't run locally. Run via de Docker container!

```
make run
```

* Stop the app

``` 
make stop
``` 

* Access the container in the console

```
make bash
```

* Access the logs

``` 
make logs
```

* Push the image to the public ECR at GCP and do a rolling update of the Kubernetes deployment with the new image.

```
make deploy
```

* Authenticate gcloud and docker 

```
make auth
```

* Create the infrastructure. Just need it to run once!

```
make create-infrastructure
```

 This project is based on the following references: 

* Resnet Image Classification Webapp (Abhishek Nagaraja - https://github.com/anagar20/Resnet-Image-Classification-Flask-App).
* CIFAR 100 transfer learning with ResNet50: https://www.kaggle.com/code/saileshnair/cifar-100-transfer-learning-resnet50/notebook