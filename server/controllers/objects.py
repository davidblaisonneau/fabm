def index():        
    objects = SQLTABLE(db(db.objects).select(),
        columns=["objects.title",
                "objects.type",
                "objects.available",
                "objects.owner",
                "objects.details",
                "objects.history"],
        headers={"objects.title": "Titre",
                "objects.type": "Type",
                "objects.available": "Disponible",
                "objects.details": "Description",
                "objects.history": "Histique"})
    form = crud.create(db.objects)
    return dict(form=form, objects=objects)
