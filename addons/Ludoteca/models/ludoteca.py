# -*- coding: utf-8 -*-
from odoo import models, fields


# Modelo 1: Desarrollador (ej: Nintendo, Rockstar, etc.)
class LudotecaDesarrollador(models.Model):
    _name = 'ludoteca.desarrollador'
    _description = 'Desarrollador de videojuegos'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)
    pais = fields.Char(string='País')
    
    # RELACIÓN ONE2MANY: Un desarrollador tiene MUCHOS videojuegos
    # 'desarrollador_id' es el campo Many2one en el modelo videojuego
    videojuegos_ids = fields.One2many(
        comodel_name='ludoteca.videojuego', 
        inverse_name='desarrollador_id',
        string='Videojuegos'
    )


# Modelo 2: Videojuego
class LudotecaVideojuego(models.Model):
    _name = 'ludoteca.videojuego'
    _description = 'Videojuego'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Título', required=True)
    plataforma = fields.Char(string='Plataforma')
    genero = fields.Char(string='Género')
    fecha_lanzamiento = fields.Date(string='Fecha de lanzamiento')
    precio = fields.Float(string='Precio')
    
    # RELACIÓN MANY2ONE: Un videojuego tiene UN desarrollador
    desarrollador_id = fields.Many2one(
        comodel_name='ludoteca.desarrollador',
        string='Desarrollador'
    )