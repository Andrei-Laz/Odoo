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
        'views/ludoteca_videojuego.xml'
    ],
}