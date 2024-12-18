para subir archivos lo correcto es usar la ruta
@app.post("/upload-pdf/")
la cual permite hacer la carga dinamica de archivos pdf

estos archivos son embebbidos y almacenados en una nueva base de datos vectorial, llamada alternative_vector_store

A los archivos pdf, tb se le puede agregar data contextual, la cual es opcional y se usa como metadata

La metadata es id_curso, id_lección