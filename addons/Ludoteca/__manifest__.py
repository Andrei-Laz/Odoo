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
    'depends': ['base', 'mail'],
    'data': [
    'security/groups.xml',
    'security/ir.model.access.csv',
    'data/sequence_data.xml',
    'views/ludoteca_search_views.xml',
    'views/ludoteca_wizard.xml',
    'views/ludoteca_videojuego.xml',
    'views/ludoteca_advanced_views.xml',
    'reports/ludoteca_report.xml',
    ],
    'images': ['static/description/icon.png']
}