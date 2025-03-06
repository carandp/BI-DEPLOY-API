# README initial

## Ejecución

Para correr el proyecto, clonar e ingresar a la carpeta app y ejecutar:
> uvicorn main:app --reload
<br>
Posteriormente dirigirse al navegador y buscar:
> http://127.0.0.1:8000

### JSONs de pruebas exitosas

{
  "ra": 185.5744857,
  "dec": 0.701402405,
  "u": 19.11034,
  "g": 17.62099,
  "r": 17.03464,
  "i": 16.82993,
  "z": 16.71711,
  "run": 756,
  "camcol": 5,
  "field": 466,
  "score": 0.8641446,
  "clean": 1,
  "class_name": "STAR",
  "mjd": 54140,
  "rowv": 0.002417854,
  "colv": 0.001363113
}
<br>
Resultado obtenido: -0.004058976020
Resultado esperado:  0.000008780529
<br><br>
{
  "ra": 160.0342636,
  "dec": -0.421625751,
  "u": 19.2634,
  "g": 17.67693,
  "r": 16.82551,
  "i": 16.42307,
  "z": 16.13864,
  "run": 756,
  "camcol": 2,
  "field": 295,
  "score": 0.870381,
  "clean": 1,
  "class_name": "GALAXY",
  "mjd": 51913,
  "rowv": 0.003937531,
  "colv": -0.00202776
}
<br>
Resultado obtenido: 0.0832401
Resultado esperado: 0.1330486
<br><br>

### JSON de error de ejecución

{
  "ra": 160.0342636,
  "dec": -0.421625751,
  "u": 19.2634,
  "g": 17.67693,
  "r": 16.82551,
  "i": 16.42307,
  "z": 16.13864,
  "run": 756,
  "camcol": 2,
  "field": 295,
  "score": 0.870381,
  "clean": 1,
  "class_name": "SUN",
  "mjd": 51913,
  "rowv": 0.003937531,
  "colv": -0.00202776
}
<br>
Resultado obtenido: 500, Internal server error
Las estrategias que podríamos usar para mitigar estos errores es verificar que la variable categórica "class_name" este entre ["STAR", "GALAXY", "QSO"]