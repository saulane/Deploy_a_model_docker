# Tutorial on How to deploy a Deep Learning model using Docker

Pour build l'image docker et la lancer faire:

```bash
docker build -t yourname/yourapp:latest .
docker run -p 80:8000 yourname/yourapp:latest
```
Pour la build pour plusieurs platformes (Apple M1-M3 et Intel/Amd)

```bash
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t yourname/yourapp:latest .
```

Lorque que l'image est compilée pour plusieurs plateformes, c'est automatiquement la bonne plateforme qui est téléchargée en faisant un docker pull sur une autre machine
