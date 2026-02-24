# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


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

    videojuegos_count = fields.Integer(string='Nº Videojuegos', compute='_compute_videojuegos_count')

    def _compute_videojuegos_count(self):
        for rec in self:
            rec.videojuegos_count = len(rec.videojuegos_ids)

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
    descripcion = fields.Text(string='Descripción')
    
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
    _inherit = ['mail.thread', 'mail.activity.mixin']

    reference = fields.Char(string='Referencia', readonly=True, copy=False)

    nombre = fields.Char(string='Título', required=True, tracking=True)

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
    
    age = fields.Integer(string='Años desde lanzamiento', compute='_compute_age', store=True)
    
    precio = fields.Float(string='Precio (€)', tracking=True)
    is_expensive = fields.Boolean(string='Caros (>50€)', compute='_compute_is_expensive', store=True)
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

    work_log_ids = fields.One2many(
        comodel_name='ludoteca.worklog',
        inverse_name='task_id',
        string='Time Entries'
    )

    total_hours = fields.Float(
        string='Total Hours',
        compute='_compute_total_hours',
        store=True
    )

    progress = fields.Float(
        string='Progress (%)',
        compute='_compute_progress'
    )

    estimated_hours = fields.Float(
        string='Estimated Hours'
    )

    _sql_constraints = [
        ('unique_name_dev', 
         'UNIQUE(nombre, desarrollador_id)', 
         'El título del videojuego debe ser único por desarrollador.'),
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

    @api.depends('fecha_lanzamiento')
    def _compute_age(self):
        for rec in self:
            if rec.fecha_lanzamiento:
                today = date.today()
                rec.age = today.year - rec.fecha_lanzamiento.year - ((today.month, today.day) < (rec.fecha_lanzamiento.month, rec.fecha_lanzamiento.day))
            else:
                rec.age = 0

    @api.depends('precio')
    def _compute_is_expensive(self):
        for rec in self:
            rec.is_expensive = bool(rec.precio and rec.precio > 50)

    @api.depends('work_log_ids.hours')
    def _compute_total_hours(self):
        for record in self:
            record.total_hours = sum(log.hours for log in record.work_log_ids)

    @api.depends('total_hours', 'estimated_hours')
    def _compute_progress(self):
        for record in self:
            if record.estimated_hours and record.estimated_hours > 0:
                record.progress = min(100.0, (record.total_hours / record.estimated_hours) * 100)
            else:
                record.progress = 0.0

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if 'reference' not in vals or not vals.get('reference'):
                seq = self.env['ir.sequence'].next_by_code('ludoteca.videojuego')
                if seq:
                    vals['reference'] = seq
        return super().create(vals_list)

    def action_publish(self):
        """Cambia el estado del videojuego a 'disponible'"""
        for record in self:
            if record.estado == 'borrador':
                record.estado = 'disponible'
        return True

    def action_set_draft(self):
        """Vuelve a poner el videojuego en estado borrador"""
        for record in self:
            if record.estado in ['disponible', 'agotado']:
                record.estado = 'borrador'
        return True

    def action_set_out_of_stock(self):
        """Marca el videojuego como agotado"""
        for record in self:
            record.estado = 'agotado'
        return True

    def action_set_discontinued(self):
        """Marca el videojuego como descatalogado"""
        for record in self:
            record.estado = 'descatalogado'
        return True


class LudotecaWorkLog(models.Model):
    _name = 'ludoteca.worklog'
    _description = 'Time Entry'
    _rec_name = 'description'

    date = fields.Date(default=fields.Date.today, required=True)
    description = fields.Text(string='Description')
    hours = fields.Float(string='Hours', required=True)
    task_id = fields.Many2one('ludoteca.videojuego', string='Task', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    _sql_constraints = [
        ('hours_positive', 'CHECK(hours > 0)', 'Hours must be positive.')
    ]


class LudotecaTimeWizard(models.TransientModel):
    _name = 'ludoteca.time.wizard'
    _description = 'Quick Time Entry Wizard'

    hours = fields.Float(required=True, default=1.0)
    description = fields.Text()
    task_id = fields.Many2one('ludoteca.videojuego', required=True)

    def action_confirm(self):
        """Create work log and return to task form"""
        self.env['ludoteca.worklog'].create({
            'hours': self.hours,
            'description': self.description,
            'task_id': self.task_id.id,
            'date': fields.Date.today()
        })
        # Refresh the task form
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ludoteca.videojuego',
            'res_id': self.task_id.id,
            'view_mode': 'form',
            'target': 'current',
        }