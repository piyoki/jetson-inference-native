# Jetson Inference Native

```bash
docker run --name jetson-inference-native -d \
  -e TZ=Asia/Shanghai \
  -p 5000:5000 \
  --runtime nvidia \
  hikariai/jetson-inference-native
```

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"network": "resnet-18", "url": "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/171633971"}' \
     http://localhost:5000/inference
```

```bash
docker logs jetson-inference-native --follow
```
