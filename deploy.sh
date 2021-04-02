
docker build -t aakashveera/soil-predictor:latest -t aakashveera/soil-predictor:$GIT_SHA -f ./disease/Dockerfile ./disease
docker build -t aakashveera/disease-predictor:latest -t aakashveera/disease-predictor:$GIT_SHA -f ./soiltype/Dockerfile ./soiltype

docker push aakashveera/soil-predictor:$GIT_SHA
docker push aakashveera/disease-predictor:$GIT_SHA

docker push aakashveera/soil-predictor:latest
docker push aakashveera/disease-predictor:latest

kubectl apply -f k8s

kubectl set image deployments/soil-deployment soil-app=aakashveera/soil-predictor:$GIT_SHA
kubectl set image deployments/disease-deployment disease-app=aakashveera/disease-predictor:$GIT_SHA