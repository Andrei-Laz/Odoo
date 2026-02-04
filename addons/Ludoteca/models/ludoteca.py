# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LudotecaDesarrollador(models.Model):
    _name = 'ludoteca.desarrollador'
    _description = 'Desarrollador de videojuegos'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)
    pais = fields.Char(string='País')
    fundacion = fields.Integer(string='Año de fundación')
    
    videojuegos_ids = fields.One2many(
        comodel_name='ludoteca.videojuego',
        inverse_name='desarrollador_id',
        string='Videojuegos'
    )

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'El nombre del desarrollador debe ser único.')
    ]

class LudotecaPlataforma(models.Model):
    _name = 'ludoteca.plataforma'
    _description = 'Plataforma de videojuegos'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)
    fabricante = fields.Char(string='Fabricante')

    videojuegos_ids = fields.Many2many(
        comodel_name='ludoteca.videojuego',
        relation='ludoteca_plataforma_videojuego_rel',
        column1='plataforma_id',
        column2='videojuego_id',
        string='Videojuegos'
    )

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'El nombre de la plataforma debe ser único.')
    ]

class LudotecaGenero(models.Model):
    _name = 'ludoteca.genero'
    _description = 'Género de videojuegos'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')  # ← Campo Text
    
    videojuegos_ids = fields.Many2many(
        comodel_name='ludoteca.videojuego',
        relation='ludoteca_genero_videojuego_rel',
        column1='genero_id',
        column2='videojuego_id',
        string='Videojuegos'
    )

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'El nombre del género debe ser único.')
    ]


class LudotecaVideojuego(models.Model):
    _name = 'ludoteca.videojuego'
    _description = 'Videojuego'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Título', required=True)

    descripcion = fields.Text(string='Sinopsis')
    
    estado = fields.Selection(
        selection=[
            ('borrador', 'Borrador'),
            ('disponible', 'Disponible'),
            ('agotado', 'Agotado'),
            ('descatalogado', 'Descatalogado'),
        ],
        string='Estado',
        readonly=False,
        default='borrador',
        required=True
    )

    fecha_lanzamiento = fields.Date(
        string='Fecha de lanzamiento',
        default=lambda self: fields.Date.today()
    )
    
    precio = fields.Float(string='Precio (€)')
    calificacion = fields.Integer(string='Calificación (1-10)')
    
    desarrollador_id = fields.Many2one(
        comodel_name='ludoteca.desarrollador',
        string='Desarrollador'
    )
    
    plataforma_ids = fields.Many2many(
        comodel_name='ludoteca.plataforma',
        relation='ludoteca_plataforma_videojuego_rel',
        column1='videojuego_id',
        column2='plataforma_id',
        string='Plataformas'
    )
    
    genero_ids = fields.Many2many(
        comodel_name='ludoteca.genero',
        relation='ludoteca_genero_videojuego_rel',
        column1='videojuego_id',
        column2='genero_id',
        string='Géneros'
    )

    _sql_constraints = [
        ('nombre_plataforma_unique', 
         'UNIQUE(nombre)', 
         'El título del videojuego debe ser único en el catálogo.'),
        ('precio_positivo', 
         'CHECK(precio >= 0)', 
         'El precio no puede ser negativo.'),
        ('calificacion_valida', 
         'CHECK(calificacion >= 1 AND calificacion <= 10)', 
         'La calificación debe estar entre 1 y 10.')
    ]

    @api.constrains('fecha_lanzamiento')
    def _check_fecha_lanzamiento(self):
        """Validación de que la fecha de lanzamiento no sea futura"""
        for record in self:
            if record.fecha_lanzamiento and record.fecha_lanzamiento > fields.Date.today():
                raise ValidationError(
                    'La fecha de lanzamiento no puede ser posterior a hoy.\n'
                    f'Fecha introducida: {record.fecha_lanzamiento}'
                )