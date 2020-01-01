# Startup Instructions

```bash
python app.py
```

```bash
APP_SETTINGS=config.ProductionConfig SECRET=v3rI_sEcUR3! python app.py
```

# Build and deploy

```bash
docker build -t review_sentiment:latest .
```

```bash
docker build --build-arg STAGE="config.ProductionConfig" --build-arg SECRET="v3rI_sEcUR3" -t review_sentiment:latest .
```

```bash
docker run -d -p 8080:5000 --name review_sentiment review_sentiment:latest
```

# Debug

```debug
docker logs review_sentiment 
```

```debug
docker run -it --entrypoint=bash review_sentiment
```