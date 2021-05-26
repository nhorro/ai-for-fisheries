Minuta 

Observaciones generales:
	- Tiempo ejecución de cada bloque
	- Para más adelante:
		- Otras métricas por bloque: accesos a disco, uso de RAM, etc.

P1) Modelo de ML para hallar patrones:
	- Se trabaja sobre el video separado en train/val/test etiquetado "a mano", etiquetado "simplista".
	- Ingeniería de features
	- Algoritmo de ML sencillo (RF o similar)	

P2) Métricas:
	De los bloques:
		- Podemos tener mAP / extender a tiempo.
			- Comentario, menor prioridad: otras métricas para seguimiento.
		- Problema: ¿Etiquetado de datos?
			- Hoy: tenemos 1 video no etiquetado. Mencionar en informe de avance. 
	Del proceso (clasificación de actividades)
		- 

P3) Iteración sobre lo implementado para mejorar proceso
	Trabajo por bloques:
	P3.1) Mejorar YOLOv4 (priorizar esta aproximación)
		- Data augmentation. ¿Cómo encararlo?
			- Reentrenar con substracción de fondo
			- PCA?
	- Plan B (ver después):
		- c/ Ensemble
			- Face detector?
		- estimación de poses c/ landmarks 

	P3.2) DeepSORT:
		- Entrenamiento del extractor:
			- Formulación teórica
			- Colab con datos disponibles.	