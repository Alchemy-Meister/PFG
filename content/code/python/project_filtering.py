#Cuando se recibe una petición POST en la vista referente a los proyectos.
if request.method == 'POST':
    # Define el formulario para comprobar las validaciones.
    form = ProjectSearchForm(request.POST, extra=request.POST
        .get('member_field_count'))
    # Comprueba que el formulario es valido.
    if form.is_valid():
        # Obtiene los campos por los que está compuesto el formulario.
        query_string = form.cleaned_data['text']
        start_date = form.cleaned_data['start_date']
        start_range = form.cleaned_data['start_range']
        end_date = form.cleaned_data['end_date']
        end_range = form.cleaned_data['end_range']
        ...
        # Comprueba individualmente si el campo introducido no es nulo.
        if start_date:
            month_year = start_date.split('/')
            # Realiza el filtrado correspondiente a la base de datos.
            if start_range == '<=':
                projects = projects.filter(Q(start_year__lt=month_year[1]) |
                 (Q(start_year=month_year[1]) & 
                    Q(start_month__lte=month_year[0])))
            elif start_range == '<':
                projects = projects.filter(Q(start_year__lt=month_year[1]) |
                    (Q(start_year=month_year[1]) &
                        Q(start_month__lt=month_year[0])))
            elif start_range == '>=':
                projects = projects.filter(Q(start_year__gt=month_year[1]) |
                 (Q(start_year=month_year[1]) &
                    Q(start_month__gte=month_year[0])))
            elif start_range == '>':
                projects = projects.filter(Q(start_year__gt=month_year[1]) |
                 (Q(start_year=month_year[1]) &
                    Q(start_month__gt=month_year[0])))
            elif start_range == '==':
                projects = projects.filter(Q(start_year=month_year[1]) &
                    Q(start_month=month_year[0]))

        ...

        found = True

        #Para los campos dinámicos concatena condiciones a la consulta.
        if form_participants_name:
            participants_query = []
            for key, name in form_participants_name.iteritems():
                # Adquiere los identificadores de los miembros que se
                # han introducido en el formulario.
                person_id = Person.objects.filter(slug__contains=name)
                    .values('id')
                if person_id:
                    # Si existe y se ha introducido los roles en los que puede
                    # participar
                    if key in form_participants_role:
                        participant_roles_ids = []
                        for role in form_participants_role[key]:
                            participant_roles_ids.append(role['id'])
                        # Se filtra por nombre y rol.
                        participants_query.append(
                            Q(assignedperson__person=person_id) & 
                            Q(assignedperson__role__in=participant_roles_ids))
                    else:
                        # Si solo ha introducido el nombre, no se especifica
                        # el rol.
                        participants_query.append(
                            Q(assignedperson__person=person_id))
                else:
                    found = False
            # Se concatenan todas las condiciones a la consulta.
            projects = projects.filter(reduce(operator.or_, participants_query))
            .distinct()

        ...

else:
    # En caso de que no sea un POST se genera un formulario vacío
    form = ProjectSearchForm(extra=1)       

# Se procesan los datos adicionales.
projects_length = len(projects)

...

# Se genera el diccionario con los valores requeridos por el cliente.
return_dict = {
    'clean_index': clean_index,
    'form': form,
    'last_entry': last_entry,
    'project_type': project_type,
    'project_type_info': dict(items),
    'projects': projects,
    ...
}

#Se renderiza la pantalla de resultado de la búsqueda con los resultados 
# devueltos en el diccionario.
return render(request, "projects/index.html", return_dict)