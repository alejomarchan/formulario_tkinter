def EleccionTema(root, val_boton):
    """Funcion permite el cambio de los temas del Widget de la ventana
            Parameters
            ----------
            root : object
                Es el objeto instanciado de la ventana Tkinteer
            val_boton : int
                Es el valor escogido en el Radio Button de la ventana
            """
    if val_boton == 1:
        root.config(bg ="navy")
    elif val_boton == 2:
        root.config(bg ="green3")
    else :
        root.config(bg ="deep pink")