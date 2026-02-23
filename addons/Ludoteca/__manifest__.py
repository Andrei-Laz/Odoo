# -*- coding: utf-8 -*-
{
    'name': "Ludoteca",
    'summary': "Videogame management system",
    'description': """
Gestor de videojuegos
==============
    """,  
    'application': True,
    'author': "Andrei",
    'website': "http://apuntesfpinformatica.es",
    'category': 'Productivity',
    'version': '0.1',
    'depends': ['base'],
    'data': [
    'security/groups.xml',
    'security/ir.model.access.csv',
    'views/ludoteca_videojuego.xml',
    'views/ludoteca_search_views.xml',
    'views/ludoteca_advanced_views.xml',
    ],
    'images': ['static/description/icon.png']
}