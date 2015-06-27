def get_pubmodified_date(self, record):
      
      # Comienza el método creando un array bidimensional donde se almacenarán
      # todas las IDs de las tablas que está relacionada la publicación, siendo
      # estas: Publication, Language, Tag, La tabla del tipo de publicación 
      # y Person.
      
      ids = [[] for i in xrange(5)]
      # Se almacena el ID de la publicación.
      ids[0].append(record.id)
      dc_type_id = None
      dc_type = self.get_parent_type(record.child_type, record.id)
      if dc_type is not None:
        # Se almacena el ID del tipo de publicación.
        ids[1].append(dc_type.publication_ptr_id)
      # Se almacena el ID del lenguaje, en caso de Null se selecciona 1 por
      # defecto.
      ids[2].append(record.language_id)
      if ids[2][0] is None:
        ids[2][0] = 1
      # Busca todos los IDs de los autores de la publicación y se almacenan
      authors = self.search_all_records_author(record.id)
      for author in authors:
        ids[3].append(author.author_id)
      tags = self.search_all_tags(record.id)
      # Almacena todos los IDs relacionados con la publicación.
      for tag in tags:
        ids[4].append(tag.tag_id)
      
      # Se definen las tablas en la que se va a realizar la búsqueda.
      tables = []
      tables.append(self.table_names.get('publication'))
      tables.append('publications_' + record.child_type.lower())
      tables.append(self.table_names.get('language'))
      tables.append(self.table_names.get('author'))
      tables.append(self.table_names.get('tag'))

      # Define la consulta para que devuelva la fecha de registro del log
      # ordenados en descendiente.
      logs_query = sql.select([self._djangoLog.c.action_time],
        from_obj=[self._djangoLog]).order_by(sql.desc(
          self._djangoLog.c.action_time))
      where_clauses = []

      for index in range(len(tables)):
        # Busca el ID que Djnago otorga a la tabla.
        content_type = self.search_content_type(self.get_app_label(
          tables[index]), self.get_model_id(tables[index]))
        if content_type is not None:
          for j_index in range(len(ids[index])):
            # Añade una condición para que busque los el ID que Django otorga
            # a la tabla y el propio ID del recurso relacionado con la
            # publicación.
            where_clauses.append(sql.and_(
              self._djangoLog.c.content_type_id == content_type.id, 
              self._djangoLog.c.object_id == unicode(ids[index][j_index])))
      logs_query.append_whereclause(sql.or_(*where_clauses))
      # ejecuta la consulta y devuelve la fecha más reciente.
      row = logs_query.execute().fetchone()
      if row is not None:
        # devuelve la fecha excluyendo la información regional.
        return row[0].replace(tzinfo=None)
      else:
        # si no se ha encontrado información, devuelve por defecto el 1 de
        # Enero del año de creación de la publicación.
        return datetime.datetime(record.year, 1, 1)