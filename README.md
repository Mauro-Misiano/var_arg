# Monitor de Riesgo de Cartera

Este proyecto permite simular el comportamiento de una cartera de inversión y calcular el VaR y CVaR con modelos GARCH.

## Cómo correrlo

```bash
pip install -r requirements.txt
python app.py
```

## Cómo desplegarlo en Render

1. Subí este proyecto a un repositorio público de GitHub.
2. Andá a https://render.com y creá una nueva Web Service.
3. Elegí el repo, seleccioná Python y en Start Command poné:

```
gunicorn app:app
```

4. ¡Listo! Se generará una URL pública para usar tu app.