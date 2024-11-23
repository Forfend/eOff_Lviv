# Image parser for Lviv electricity schedule

# Build a Docker image

```
docker build --platform linux/amd64 -t forfend/schedule:latest .
```

# Push a Docker image

```
docker push forfend/schedule:latest
```

# Run a Docker container

```
docker run -d -p 80:5000 forfend/schedule:latest
```
