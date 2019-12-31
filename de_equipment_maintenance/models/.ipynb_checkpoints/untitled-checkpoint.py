def action_view_maintenance1(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('de_equipment_maintenance.maintenance_order_list_view').read()[0]

        maintenance_orders = self.mapped('maintenance_order_ids')
        if len(maintenance_orders) > 1:
            action['domain'] = [('id', 'in', maintenance_orders.ids)]
        elif maintenance_orders:
            form_view = [(self.env.ref('de_equipment_maintenance.maintenance_order_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = maintenance_orders.id
        # Prepare the context.
        maintenance_order_id = maintenance_orders.filtered(lambda l: l.maintenance_request_id == self.id)
        if maintenance_order_id:
            maintenance_order_id = maintenance_order_id[0]
        else:
            maintenance_order_id = maintenance_orders[0]
        action['context'] = dict(self._context, default_maintenance_request_id=self.id)
        return action