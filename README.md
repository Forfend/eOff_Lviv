# Image parser for Lviv electricity schedule

# Build a Docker image

```
docker build --platform linux/amd64 -t forfend/schedule:latest .
```

# Run a Docker container

```
docker run -p 80:5000 forfend/schedule:latest
```
